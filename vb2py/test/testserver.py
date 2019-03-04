"""Test the conversion server"""

from testframework import *
import vb2py.conversionserver
import vb2py.parserclasses
import vb2py.config
import os
import urllib
import threading
import json
import vb2py.utils
from flask import request
import pytest
from vb2py.vbfunctions import Integer


PATH = vb2py.utils.rootPath()
Config = vb2py.config.VB2PYConfig()


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
        result = client.post('/single_code_module', data={'text': 'a=10\nb=20\nc=a+b', 'style': 'vb'})
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
        result = client.post('/single_code_module', data={'textNOTTHERE': 'a='})
        data = json.loads(result.data)
        self.assertEqual(data['status'], 'FAILED')
        self.assertIn('text', data['result'].lower())

    def testJSONERROR(self):
        """testJSONERROR: server JSON error should work OK"""
        vb2py.conversionserver.app.config['TESTING'] = True
        client = vb2py.conversionserver.app.test_client()
        result = client.post('/single_code_module', data={'text': 'a=', 'style': 'vb'})
        data = json.loads(result.data)
        self.assertEqual(data['status'], 'ERROR')
        self.assertIn('parsing', data['result'].lower())

    def testCanDoClassModule(self):
        """testCanDoClassModule: should be able to do a class module"""
        vb2py.conversionserver.app.config['TESTING'] = True
        client = vb2py.conversionserver.app.test_client()
        result = client.post('/single_class_module', data={'text': 'a=10', 'style': 'vb'})
        data = json.loads(result.data)
        self.assertEqual(data['status'], 'OK')
        d = {}
        exec(data['result'], globals(), d)
        obj = d['MyClass']()
        self.assertEqual(10, obj.a)

    def testCanDoPythonicConversion(self):
        """testCanDoPythonicConversion: should be able to do pythonic conversion"""
        Config.setLocalOveride("General", "RespectPrivateStatus", "Yes")
        vb2py.conversionserver.app.config['TESTING'] = True
        client = vb2py.conversionserver.app.test_client()

        code = '''
        Private a as Integer
        b = 20
        
        Sub doIt(X)
            ' Do something
        End Sub
        
        
        '''
        py = self.c(code, container=vb2py.parserclasses.VBClassModule(), style='pythonic')
        d = {'Integer': Integer}
        exec(py, globals(), d)
        obj = d['MyClass']()
        self.assertTrue(hasattr(obj, 'a'))
        self.assertTrue(hasattr(obj, 'doIt'))
        #
        # Now try non-pythonic
        py = self.c(code, container=vb2py.parserclasses.VBClassModule(), style='vb')
        d = {'Integer': Integer}
        exec(py, globals(), d)
        obj = d['MyClass']()
        self.assertFalse(hasattr(obj, 'a'))
        self.assertFalse(hasattr(obj, 'doIt'))

    def testClearServerHistory(self):
        """testClearServerHistory: history of the server should be removed"""
        code = '''
        
        Sub doIt(X)
            Select Case A
                Case 1
                    B = 10
            End Select
        End Sub
        Sub doIt2(X)
            Select Case A
                Case 1
                    B = 10
            End Select
        End Sub        
        
        '''
        py1 = self.c(code)
        py2 = self.c(code)
        #
        self.assertIn('_select', py1)
        self.assertIn('_select1', py1)
        self.assertIn('_select', py2)
        self.assertIn('_select1', py2)
        self.assertNotIn('_select2', py2)


if __name__ == '__main__':
    main()
