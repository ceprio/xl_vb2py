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
WIDTH = 100


def get_connection(filename):
    """Get a connection to the database"""
    return sqlite3.connect(filename)


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
        (id integer primary key, date text, name text, total integer, failed integer, duration float)
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


def create_tests(filename):
    """Create the initial tests"""
    print('Creating tests')
    with get_connection(filename) as conn:
        #
        # Remove old
        conn.execute('DELETE FROM tests')
        #
        # Go through all files
        files = glob.glob(utils.relativePath('test_at_scale', 'test*.py'))
        total_count = 0
        for file in files:
            count = 0
            print('Adding {} '.format(file).ljust(WIDTH, '.'), end='')
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


def matching_tests(conn, test_folder, test_filename, include_inactive=False):
    """Return a list of matching tests"""
    active_clause = 'AND active' if not include_inactive else ''
    cursor = conn.execute('''
    SELECT id, path, filename FROM tests 
    WHERE path LIKE ?
    AND filename LIKE ? 
    ''' + active_clause, [test_folder, test_filename])
    return cursor.fetchall()


def run_file(conn, list_of_tests, name):
    """Perform a single test on a file"""
    tester = file_tester.FileTester()
    success = failure = 0
    beginning_time = time.time()
    #
    # Create a new test run
    cur = conn.execute("INSERT INTO runs ('date', 'name') VALUES(current_date, ?)", [name])
    run_id = cur.lastrowid
    #
    for item in list_of_tests:
        test_id, folder, filename = item
        print('Test {}/{} '.format(folder, filename).ljust(WIDTH, '.'), end='')
        start_time = time.time()
        with Suppress():
            try:
                tester._testFile(os.path.join(folder, filename))
            except Exception as err:
                result = ' {}FAILED [{:.1f}s] {}'.format(C.FAIL, time.time() - start_time, C.ENDC)
                failure += 1
            else:
                result = ' {}DONE [{:.1f}s] {}'.format(C.OKGREEN, time.time() - start_time, C.ENDC)
                success += 1
        #
        print(result)
    #
    conn.execute('UPDATE runs SET total=?, failed=?, duration=? WHERE id=?', (
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
        print('Setting {}/{} to {}{}{}'.format(
            folder, filename, C.OKBLUE, active, C.ENDC))
        conn.execute('UPDATE tests SET active = ? WHERE id = ?', (active, test_id))
    #
    print('\nComplete')


def show_matching(conn, list_of_tests):
    """Show which files match"""
    for item in list_of_tests:
        test_id, folder, filename = item
        print('{}/{}'.format(folder, filename))
    #
    print('\nTotal {} tests\n'.format(len(list_of_tests)))


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
    parser.add_argument('--run-file', required=False, default=False, action='store_true',
                        help='run a test on a file or file pattern')
    parser.add_argument('--disable', required=False, default=False, action='store_true',
                        help='disable the given tests')
    parser.add_argument('--enable', required=False, default=False, action='store_true',
                        help='enable the given tests')
    parser.add_argument('--show', required=False, default=False, action='store_true',
                        help='just show the matching tests')

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
    if args.create_tests:
        create_tests(db_filename)
    #
    # Manipulation
    with get_connection(db_filename) as connection:
        tests = matching_tests(connection, args.folder, args.filename, include_inactive=args.enable)
        if args.run_file:
            run_file(connection, tests, args.run_name)
        if args.disable:
            set_active(connection, tests, False)
        if args.enable:
            set_active(connection, tests, True)
        if args.show:
            show_matching(connection, tests)