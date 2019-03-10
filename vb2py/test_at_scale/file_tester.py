"""Base class for testing file translation"""

import unittest
import os
import json
import argparse
import sys
import subprocess
import re


sys.path.append('../..')

import vb2py.parserclasses
import vb2py.conversionserver


#
# Private data hiding may obscure some of the testing so we turn it off
import vb2py.config
Config = vb2py.config.VB2PYConfig()
Config.setLocalOveride("General", "RespectPrivateStatus", "No")
Config.setLocalOveride("General", "ReportPartialConversion", "No")


BASE_FOLDER = '/Users/paul/Workspace/sandbox/vb2py-git-files'


class FileTester(unittest.TestCase):
    """Base class for file testing"""

    def _testFile(self, filename):
        """Try to parse a file"""
        #
        # Get the text
        with open(filename, 'r') as f:
            vb_code = f.read()
        #
        # Get the container
        container_lookup = {
            ".bas": (vb2py.parserclasses.VBCodeModule, 'code'),
            ".cls": (vb2py.parserclasses.VBClassModule, 'class'),
            ".frm": (vb2py.parserclasses.VBFormModule, 'form'),
        }
        extension = os.path.splitext(filename)[1]
        container_class, url_part = container_lookup[extension.lower()]
        container = container_class()
        #
        client = vb2py.conversionserver.app.test_client()
        result = client.post(
            ('/single_%s_module' % url_part),
            data={
                'text': vb_code, 'style': 'vb'
            }
        )
        data = json.loads(result.data)
        if data['parsing_failed']:
            msg = 'Parsing %s failed: %s' % (
                filename,
                vb_code.splitlines()[data['parsing_stopped_vb']]
            )
            self.fail(msg)


if __name__ == '__main__':
    #
    # Arguments
    parser = argparse.ArgumentParser(description='Clone repo and create tests')
    parser.add_argument('repos', type=str, nargs='+',
                        help='repo to clone and create tests for')
    args = parser.parse_args()
    #
    # Create a repo
    for repo in args.repos:
        name_match = re.match('https://github.com/(.*?)/', repo)
        if not name_match:
            print 'Repo format not recognized: %s' % repo
            sys.exit(1)
        #
        name = name_match.groups()[0]
        folder_name = os.path.join(BASE_FOLDER, name)
        #
        # Clone if it is not there
        if os.path.isdir(folder_name):
            print 'Folder exists. Skipping clone'
        else:
            print 'Cloning repository %s as %s' % (repo, name)
            subprocess.call(['git', 'clone', repo, folder_name])
        #
        # Now try to find all the files
        filenames = []
        for subdir, dirs, files in os.walk(folder_name):
            for filename in files:
                filepath = os.path.join(subdir, filename)
                extn = os.path.splitext(filepath)[1]
                if extn.lower() in ['.frm', '.bas', '.cls']:
                    print 'Creating tests for %s' % filepath
                    filenames.append(filepath)
        #
        # Now create the test file
        file_start_text = '''
import unittest
from . import file_tester


class Test_%s(file_tester.FileTester):
'''
        test_fragment = '''
\tdef test%s(self):
\t\tself._testFile('%s')
'''
        file_end_text = '''

if __name__ == '__main__':
\tunittest.main()
'''
        file_text = '%s%s%s' % (
            (file_start_text % name),
            ''.join((test_fragment % (idx, filename)) for idx, filename in enumerate(filenames)),
            file_end_text,
        )
        #
        # Write the file
        test_file_name = 'test%s.py' % name
        with open(test_file_name, 'w') as f:
            f.write(file_text)
        #
        print 'Complete\n'