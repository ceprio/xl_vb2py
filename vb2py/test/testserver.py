"""Test the conversion server"""

from testframework import *
import vb2py.conversionserver
import os
import urllib
import threading
import json
import vb2py.utils
from flask import request
import pytest


PATH = vb2py.utils.rootPath()


class TestServer(unittest.TestCase):
    """Test of the Server class"""

    def setUp(self):
        """Set up the tests"""
        self.c = vb2py.conversionserver.ConversionHandler.convertSingleFile

    def tearDown(self):
        """Tear down the tests"""

    def testCanCreateServer(self):
        """testCanCreateServer: should be able to create server"""

    def testCanConvertALine(self):
        """testCanConvertALine: should be able to convert a line"""
        vb = 'a = 10'
        py = self.c(vb)
        d = {}
        exec(py, globals(), d)
        self.assertEqual(d['a'], 10)

    def testCanConvertMultipleLines(self):
        """testCanConvertMultipleLines: should be able to convert multiple lines"""
        vb = 'a = 10\nb = 20\nc = a + b'
        py = self.c(vb)
        d = {}
        exec(py, globals(), d)
        self.assertEqual(d['a'], 10)
        self.assertEqual(d['b'], 20)
        self.assertEqual(d['c'], 30)

    def testCanReportAnError(self):
        """testCanReportAnError: should be able to report an error"""
        vb = 'a = '
        self.assertRaises(vb2py.conversionserver.ConversionError, self.c, vb)

    def _getResult(self, url):
        """Return a result from a URL"""
        try:
            f = urllib.urlopen('http://localhost:8123/%s' % url)
            result = f.read()
        finally:
            f.close()
        return result

    def testCanStartServer(self):
        """testCanStartServer: should be able to start the server"""
        vb2py.conversionserver.app.config['TESTING'] = True
        client = vb2py.conversionserver.app.test_client()
        result = client.post('/test')
        data = json.loads(result.data)
        self.assertEqual(data, {'status': 'OK'})

    def testJSONOK(self):
        """testJSONOK: server JSON should return OK"""
        vb2py.conversionserver.app.config['TESTING'] = True
        client = vb2py.conversionserver.app.test_client()
        result = client.post('/single_module', data={'text': 'a=10\nb=20\nc=a+b'})
        data = json.loads(result.data)
        self.assertEqual(data['status'], 'OK')
        py = data['result']
        d = {}
        exec(py, globals(), d)
        self.assertEqual(d['a'], 10)
        self.assertEqual(d['b'], 20)
        self.assertEqual(d['c'], 30)

    def testJSONFAIL(self):
        """testJSONFAIL: server JSON failure should work OK"""
        vb2py.conversionserver.app.config['TESTING'] = True
        client = vb2py.conversionserver.app.test_client()
        result = client.post('/single_module', data={'textNOTTHERE': 'a='})
        data = json.loads(result.data)
        self.assertEqual(data['status'], 'FAILED')
        self.assertIn('text', data['result'].lower())

    def testJSONERROR(self):
        """testJSONERROR: server JSON error should work OK"""
        vb2py.conversionserver.app.config['TESTING'] = True
        client = vb2py.conversionserver.app.test_client()
        result = client.post('/single_module', data={'text': 'a='})
        data = json.loads(result.data)
        self.assertEqual(data['status'], 'ERROR')
        self.assertIn('parsing', data['result'].lower())


if __name__ == '__main__':
    main()
