"""Database driven testing"""

import argparse
import sys
import os
import sqlite3
import glob
import re
import time
import datetime

sys.path.append('..')
from vb2py import utils
from vb2py.test_at_scale import file_tester

C = utils.TextColours
WIDTH = 90


#
# Allow use of datetimes
def adapt_datetime(ts):
    return time.mktime(ts.timetuple())


sqlite3.register_adapter(datetime.datetime, adapt_datetime)


def get_connection(filename):
    """Get a connection to the database"""
    return sqlite3.connect(filename)


def np(filename):
    """Return a shortened version of a filename"""
    return filename[len(file_tester.BASE_FOLDER):]


def create_database(filename):
    """Create the database"""
    print('Creating new database as {} ...'.format(filename), end='')
    #
    # Remove old if needed
    if os.path.exists(filename):
        os.remove(filename)
    #
    conn = get_connection(filename)
    #
    conn.execute('''
        CREATE TABLE tests
        (id integer primary key, path text, filename text, active bool)
    ''')
    #
    conn.execute('''
        CREATE TABLE runs
        (id integer primary key, date text, name text unique, total integer, failed integer, duration float)
    ''')
    #
    conn.execute('''
        CREATE TABLE groups
        (id integer primary key, name text unique)
    ''')
    #
    conn.execute('''
        CREATE TABLE group_entries
        (group_id integer not null, test_id integer not null,
            FOREIGN KEY (group_id) REFERENCES groups (id) ON DELETE CASCADE,
            FOREIGN KEY (test_id) REFERENCES tests (id) ON DELETE CASCADE,
            UNIQUE (group_id, test_id)
        )
    ''')
    #
    conn.execute('''
        CREATE TABLE results
        (test_id integer not null, run_id integer not null, result bool, duration float, 
            FOREIGN KEY (test_id) REFERENCES tests (id),
            FOREIGN KEY (run_id) REFERENCES runs (id)
        )
    ''')
    conn.close()
    print('{} DONE{}\n'.format(C.OKGREEN, C.ENDC))


def create_tests(conn):
    """Create the initial tests"""
    print('Creating tests')
    #
    # Remove old
    conn.execute('DELETE FROM tests')
    #
    # Go through all files
    files = glob.glob(utils.relativePath('test_at_scale', 'test*.py'))
    total_count = 0
    for file in files:
        count = 0
        print('Adding {} '.format(np(file)).ljust(WIDTH, '.'), end='')
        with open(file, 'r') as f:
            file_text = f.read()
            for test_file in re.findall("_testFile\('(.*?)'", file_text):
                folder, filename = os.path.split(test_file)
                count += 1
                conn.execute('''
                INSERT INTO tests ('path', 'filename', 'active') 
                VALUES (?, ?, 1)
                ''', (folder, filename))
        total_count += count
        print('{} DONE [{} tests]{}'.format(C.OKGREEN, count, C.ENDC))
    #
    print('\nCompleted {} tests\n'.format(total_count))


def matching_tests(conn, args):
    """Return a list of matching tests"""
    #
    # Get files based on tests
    if args.last_test or args.last_failed or args.last_passed or args.previous_run:
        if args.previous_run:
            cur = conn.execute('SELECT id, date, name FROM runs WHERE name like ?', [args.previous_run])
        else:
            cur = conn.execute('SELECT id, date, name FROM runs ORDER BY date desc')
        matches = cur.fetchone()
        if not matches:
            print('{}No matching tests{}\n'.format(C.FAIL, C.ENDC))
            return []
        #
        run_id, timestamp, name = matches
        #
        # A clause to filter the tests down
        if args.last_failed:
            success_clause = 'AND results.result = 0'
        elif args.last_passed:
            success_clause = 'AND results.result = 1'
        else:
            success_clause = ''
        #
        print('Selecting test {}"{}"{} run at {}{}{}'.format(
            C.OKBLUE,
            name,
            C.ENDC,
            C.OKBLUE,
            datetime.datetime.fromtimestamp(int(float(timestamp))),
            C.ENDC
        ))
        cur = conn.execute('''SELECT tests.id, tests.path, tests.filename FROM tests 
            INNER JOIN results ON tests.id = results.test_id
            WHERE results.run_id = ?
            AND path LIKE ?
            AND filename LIKE ?
            {}
        '''.format(success_clause), [run_id, args.folder, args.filename])
        files = cur.fetchall()
    elif args.group:
        cur = conn.execute('''
            SELECT t.id, t.path, t.filename FROM group_entries 
            INNER JOIN groups g on group_entries.group_id = g.id
            INNER JOIN tests t on group_entries.test_id = t.id
            WHERE g.name = ?
        ''', [args.group])
        files = cur.fetchall()
    elif args.never_run:
        cursor = conn.execute('''
            select id, path, filename from tests
            WHERE path like ?
            AND filename like ?
            AND active
            EXCEPT 
            SELECT tests.id, path, filename FROM tests INNER JOIN results r ON tests.id = r.test_id      
        ''', [args.folder, args.filename])
        files = cursor.fetchall()
    else:
        #
        # Get files based on folders and files
        active_clause = 'AND active' if not args.enable else ''
        cursor = conn.execute('''
        SELECT id, path, filename FROM tests 
        WHERE path LIKE ?
        AND filename LIKE ? 
        ''' + active_clause, [args.folder, args.filename])
        files = cursor.fetchall()
    #
    if args.failed_last_time:
        files = [item for item in files if get_last_result(conn, item[0]) == 0]
    #
    return files


def get_last_result(conn, test_id):
    """Return the last test result"""
    cur = conn.execute('''select result from results
        inner join runs r on results.run_id = r.id
        where test_id = ?
        order by date desc 
    ''', [test_id])
    result = cur.fetchone()
    if not result:
        return None
    else:
        return result[0]


def run_file(conn, list_of_tests, name):
    """Perform a single test on a file"""
    tester = file_tester.FileTester()
    success = failure = 0
    beginning_time = time.time()
    #
    # Create a new test run
    cur = conn.execute("INSERT INTO runs ('date', 'name') VALUES(?, ?)", [datetime.datetime.now(), name])
    run_id = cur.lastrowid
    #
    for item in list_of_tests:
        test_id, folder, filename = item
        print('Test {} '.format(np(os.path.join(folder, filename))).ljust(WIDTH - 10, '.') +
              get_last_tests(conn, test_id), end='')
        start_time = time.time()
        with Suppress():
            try:
                tester._testFile(os.path.join(folder, filename))
            except Exception as err:
                report = ' {}FAILED [{:.1f}s] {}'.format(C.FAIL, time.time() - start_time, C.ENDC)
                failure += 1
                result = 0
            else:
                report = ' {}DONE [{:.1f}s] {}'.format(C.OKGREEN, time.time() - start_time, C.ENDC)
                success += 1
                result = 1
            conn.execute('''
                INSERT INTO results 
                (test_id, run_id, result, duration)
                VALUES (?, ?, ?, ?)
                ''', [test_id, run_id, result, time.time() - start_time])
        #
        print(report)
    #
    cur = conn.execute('UPDATE runs SET total=?, failed=?, duration=? WHERE id=?', (
        success + failure, failure, time.time() - beginning_time, run_id))
    #
    if not failure:
        print('\n{}Completed {} test{}'.format(C.OKGREEN, success, C.ENDC))
    else:
        print('\n{}Completed {} test with {} failures{}'.format(C.FAIL, success + failure, failure, C.ENDC))


def set_active(conn, list_of_tests, active):
    """Set whether tests are active or not"""
    for item in list_of_tests:
        test_id, folder, filename = item
        print('Setting {} to {}{}{}'.format(
            np(os.path.join(folder, filename)), C.OKBLUE, active, C.ENDC))
        conn.execute('UPDATE tests SET active = ? WHERE id = ?', (active, test_id))
    #
    print('\nComplete')


def get_last_tests(conn, test_id):
    """Return the last tests run on this"""
    cur = conn.execute('''
        SELECT result FROM results INNER JOIN runs ON results.run_id = runs.id
        WHERE test_id = ?
        ORDER BY runs.date desc LIMIT 10
        ''', [test_id])
    results = [' '] * 10
    for item in reversed(cur.fetchall()):
        if item[0]:
            results.append('{}*{}'.format(C.OKGREEN, C.ENDC))
        else:
            results.append('{}!{}'.format(C.FAIL, C.ENDC))
    return ''.join(results[-10:])


def show_matching(conn, list_of_tests):
    """Show which files match"""
    for item in list_of_tests:
        test_id, folder, filename = item
        last_tests = get_last_tests(conn, test_id)
        print('{} '.format(np(os.path.join(folder, filename))).ljust(WIDTH, '.') + last_tests)
    #
    print('\nTotal {} tests\n'.format(len(list_of_tests)))


def create_group(conn, list_of_tests, new_group_name):
    """Create a new group"""
    try:
        cur = conn.execute('INSERT INTO groups (name) VALUES(?)', [new_group_name])
    except sqlite3.IntegrityError:
        print('\n{}Group "{}" already exists{}\n'.format(C.FAIL, new_group_name, C.ENDC))
        return
    #
    group_id = cur.lastrowid
    print('\nCreated group {}"{}"{}'.format(C.OKBLUE, new_group_name, C.ENDC))
    #
    for item in list_of_tests:
        test_id, folder, filename = item
        conn.execute('INSERT INTO group_entries (group_id, test_id) VALUES(?, ?)', [group_id, test_id])
        print('Added {} to group'.format(np(os.path.join(folder, filename))))
    #
    print('\nAdded {} tests'.format(len(list_of_tests)))


def add_to_group(conn, list_of_tests, group_name):
    """Add to an existing group"""
    cur = conn.execute('SELECT id FROM groups WHERE name = ?', [group_name])
    result = cur.fetchone()
    if not result:
        print('\n{}Group "{}" does not exist{}\n'.format(C.FAIL, group_name, C.ENDC))
        return
    #
    group_id = result[0]
    print('\nAdding to group {}"{}"{}'.format(C.OKBLUE, group_name, C.ENDC))
    #
    count = 0
    for item in list_of_tests:
        test_id, folder, filename = item
        try:
            conn.execute('INSERT INTO group_entries (group_id, test_id) VALUES(?, ?)', [group_id, test_id])
        except sqlite3.IntegrityError:
            print('{}{} already in group{}'.format(C.FAIL, np(os.path.join(folder, filename)), C.ENDC))
        else:
            print('Added {} to group'.format(np(os.path.join(folder, filename))))
            count += 1
    #
    print('\nAdded {} tests'.format(count))


def delete_group(conn, list_of_tests, group_name):
    """Delete an existing group"""
    cur = conn.execute('SELECT id FROM groups WHERE name = ?', [group_name])
    result = cur.fetchone()
    if not result:
        print('\n{}Group "{}" does not exist{}\n'.format(C.FAIL, group_name, C.ENDC))
        return
    group_id = result[0]
    conn.execute('DELETE FROM groups WHERE name = ?', [group_name])
    conn.execute('DELETE FROM group_entries WHERE group_id = ?', [group_id])
    print('\nGroup {}"{}"{} deleted'.format(C.OKBLUE, group_name, C.ENDC))


def show_groups(conn):
    """Show all the groups"""
    cur = conn.execute('''
        select name, count(group_id) from groups
        inner join group_entries ge on groups.id = ge.group_id
        group by name, group_id
    ''')
    print('\nList of groups\n')
    total_groups = cur.fetchall()
    for item in total_groups:
        name, count = item
        print(' - {} {}{} tests {}'.format(name, C.OKBLUE, count, C.ENDC))
    print('\nNumber of groups = {}\n'.format(len(total_groups)))


def create_test_groups(conn):
    """Create groups for all the folders"""
    print('\nCreating all test groups\n')
    cur = conn.execute('select distinct(path) from tests')
    folders = set()
    count = 0
    for item in cur.fetchall():
        root_path = item[0][len(file_tester.BASE_FOLDER) + 1:].split('/')[0]
        if root_path not in folders:
            folders.add(root_path)
            try:
                conn.execute('INSERT INTO groups (name) VALUES(?)', [root_path])
            except sqlite3.IntegrityError:
                print('{}Group "{}" already exists {}'.format(C.FAIL, root_path, C.ENDC))
            else:
                print('Created group {}"{}"{}'.format(C.OKBLUE, root_path, C.ENDC))
                count += 1
    #
    print('\nCreated {} groups\n'.format(count))


class Suppress:
    def __init__(self, *, suppress_stdout=True, suppress_stderr=True):
        self.suppress_stdout = suppress_stdout
        self.suppress_stderr = suppress_stderr
        self.original_stdout = None
        self.original_stderr = None

    def __enter__(self):
        import sys, os
        devnull = open(os.devnull, "w")
        sys.stdout.flush()

        # Suppress streams
        if self.suppress_stdout:
            self.original_stdout = sys.stdout
            sys.stdout = devnull

        if self.suppress_stderr:
            self.original_stderr = sys.stderr
            sys.stderr = devnull

    def __exit__(self, *args, **kwargs):
        import sys
        # Restore streams
        if self.suppress_stdout:
            sys.stdout = self.original_stdout

        if self.suppress_stderr:
            sys.stderr = self.original_stderr


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Database driven tester')
    #
    # The database itself
    parser.add_argument('--db-file', required=False, default='testing.db', type=str,
                        dest='db_file', action='store',
                        help='the database name to use')
    parser.add_argument('--db-path', required=False, default='test_at_scale', type=str,
                        dest='db_path', action='store',
                        help='the database path, relative to vb2py')
    #
    # Which tests to act on
    parser.add_argument('--filename', required=False, type=str,
                        dest='filename', action='store', default='%',
                        help='a filename to act on')
    parser.add_argument('--folder', required=False, type=str,
                        dest='folder', action='store', default='%',
                        help='a folder to act on')
    parser.add_argument('--last-test', required=False, default=False, action='store_true',
                        dest='last_test',
                        help='the last tests run')
    parser.add_argument('--last-failed', required=False, default=False, action='store_true',
                        dest='last_failed',
                        help='the last tests run that failed')
    parser.add_argument('--last-passed', required=False, default=False, action='store_true',
                        dest='last_passed',
                        help='the last tests run that passed')
    parser.add_argument('--previous-run', required=False, type=str,
                        dest='previous_run', action='store', default='',
                        help='a previous run to act on')
    parser.add_argument('--never-run', required=False, default=False, action='store_true',
                        dest='never_run',
                        help='a test that has never been run')
    parser.add_argument('--failed-last-time', required=False, default=False, action='store_true',
                        dest='failed_last_time',
                        help='a test that failed last time it was run')
    parser.add_argument('--group', required=False, type=str,
                        dest='group', action='store', default='',
                        help='a named group to act on')
    #
    # Parameters
    parser.add_argument('--run-name', required=False, type=str,
                        dest='run_name', action='store', default='Test {}'.format(
                            datetime.datetime.now().strftime('%H:%M %d-%m-%Y')),
                        help='a folder to act on')
    #
    # The commands
    parser.add_argument('--create', required=False, default=False, action='store_true',
                        help='create the database')
    parser.add_argument('--create-tests', required=False, default=False, action='store_true',
                        dest='create_tests',
                        help='create the test cases')
    parser.add_argument('--create-test-groups', required=False, default=False, action='store_true',
                        dest='create_test_groups',
                        help='create the groups for the test cases')
    parser.add_argument('--run-file', required=False, default=False, action='store_true',
                        help='run a test on a file or file pattern')
    parser.add_argument('--disable', required=False, default=False, action='store_true',
                        help='disable the given tests')
    parser.add_argument('--enable', required=False, default=False, action='store_true',
                        help='enable the given tests')

    parser.add_argument('--create-group', required=False, type=str,
                        dest='create_group', action='store', default='',
                        help='a group to create')
    parser.add_argument('--add-to-group', required=False, type=str,
                        dest='add_to_group', action='store', default='',
                        help='a group to add files to')
    parser.add_argument('--delete-group', required=False, type=str,
                        dest='delete_group', action='store', default='',
                        help='a group to delete')

    parser.add_argument('--show', required=False, default=False, action='store_true',
                        help='just show the matching tests')
    parser.add_argument('--show-groups', required=False, default=False, action='store_true',
                        help='show the groups')

    args = parser.parse_args()
    print('\n{}{}Database testing application\n{}'.format(
        C.HEADER, C.OKBLUE, C.ENDC
    ))
    #
    db_filename = utils.relativePath(args.db_path, args.db_file)
    #
    # Database population
    if args.create:
        create_database(db_filename)
    #
    # Manipulation
    with get_connection(db_filename) as connection:
        if args.create_tests:
            create_tests(connection)
        if args.create_test_groups:
            create_test_groups(connection)
        #
        tests = matching_tests(connection, args)
        if args.run_file:
            run_file(connection, tests, args.run_name)
        if args.disable:
            set_active(connection, tests, False)
        if args.enable:
            set_active(connection, tests, True)
        if args.show:
            show_matching(connection, tests)
        if args.create_group:
            create_group(connection, tests, args.create_group)
        if args.add_to_group:
            add_to_group(connection, tests, args.add_to_group)
        if args.delete_group:
            delete_group(connection, tests, args.delete_group)
        if args.show_groups:
            show_groups(connection)