# -*- coding: latin-1 -*-

"""Test the conversion server"""

from testframework import *
import vb2py.conversionserver
import vb2py.parserclasses
import vb2py.config
import vb2py.converter
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
        Config["General", "ReportPartialConversion"] == "Yes"
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
        self.assertRaises(vb2py.conversionserver.ConversionError, self.c, vb, returnpartial=False)

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
        self.assertEqual(data['status'], 'OK')
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

    def testUnicodeCharacters(self):
        """testUnicodeCharacters: should be able to handle unicode characters"""
        vb2py.conversionserver.app.config['TESTING'] = True
        client = vb2py.conversionserver.app.test_client()
        result = client.post('/single_class_module', data={'text': u'a="�"', 'style': 'vb'})
        data = json.loads(result.data)
        self.assertEqual(data['status'], 'OK')
        d = {}
        exec(data['result'], globals(), d)
        obj = d['MyClass']()
        self.assertEqual(2, len(obj.a))

    def testCanSendClassName(self):
        """testCanSendClassName: should be able to send class name"""
        vb2py.conversionserver.app.config['TESTING'] = True
        client = vb2py.conversionserver.app.test_client()
        #
        code = """
        A = 10
        """
        #
        result = client.post('/single_class_module', data={'text': code, 'style': 'vb', 'class_name': 'TheName'})
        data = json.loads(result.data)
        self.assertEqual(data['status'], 'OK')
        d = {}
        exec(data['result'], globals(), d)
        obj = d['TheName']()
        self.assertEqual(10, obj.A)

    def testDetectsParserFailure(self):
        """testDetectsParserFailure: should detect parser failure"""
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

        End Sub        
        '''
        client = vb2py.conversionserver.app.test_client()
        result = client.post('/single_code_module', data={'text': code, 'style': 'vb'})
        data = json.loads(result.data)
        self.assertEqual(True, data['parsing_failed'])
        self.assertEqual(7, data['parsing_stopped_vb'])
        self.assertEqual(10, data['parsing_stopped_py'])

    def testParserInSubFailure(self):
        """testParserInSubFailure: can get to failing line in subroutine"""
        code = '''
        Sub doIt(X)
            A = 
        End Sub       
        '''
        client = vb2py.conversionserver.app.test_client()
        result = client.post('/single_code_module', data={'text': code, 'style': 'vb'})
        data = json.loads(result.data)
        self.assertEqual(True, data['parsing_failed'])
        self.assertEqual(2, data['parsing_stopped_vb'])

    def testParserInBlockFailure(self):
        """testParserInBlockFailure: can get to failing line in subroutine and block"""
        code = '''
        Sub doIt(X)
            If X > 10 Then
                A =
            End If 
        End Sub       
        '''
        client = vb2py.conversionserver.app.test_client()
        result = client.post('/single_code_module', data={'text': code, 'style': 'vb'})
        data = json.loads(result.data)
        self.assertEqual(True, data['parsing_failed'])
        self.assertEqual(3, data['parsing_stopped_vb'])

    def testWhileBlockFailure(self):
        """testWhileBlockFailure: can get to failing line in while block"""
        code = '''
        Sub doIt(X)
            While A > 10
                A =
            End While
        End Sub       
        '''
        client = vb2py.conversionserver.app.test_client()
        result = client.post('/single_code_module', data={'text': code, 'style': 'vb'})
        data = json.loads(result.data)
        self.assertEqual(True, data['parsing_failed'])
        self.assertEqual(3, data['parsing_stopped_vb'])

    def testDoBlockFailure(self):
        """testDoBlockFailure: can get to failing line in do block"""
        code = '''
        Sub doIt(X)
            Do
                A = A + 
            Loop Until A = 10
        End Sub          
        '''
        client = vb2py.conversionserver.app.test_client()
        result = client.post('/single_code_module', data={'text': code, 'style': 'vb'})
        data = json.loads(result.data)
        self.assertEqual(True, data['parsing_failed'])
        self.assertEqual(3, data['parsing_stopped_vb'])

    def testWithBlockFailure(self):
        """testWithBlockFailure: can get to failing line in with block"""
        code = '''
        Sub doIt(X)
            With This.A
                This.A = 
            End With
        End Sub   
        '''
        client = vb2py.conversionserver.app.test_client()
        result = client.post('/single_code_module', data={'text': code, 'style': 'vb'})
        data = json.loads(result.data)
        self.assertEqual(True, data['parsing_failed'])
        self.assertEqual(3, data['parsing_stopped_vb'])

    def testParserInBlockStartFailure(self):
        """testParserInBlockStartFailure: can get to failing line in subroutine at start"""
        code = '''
        Sub doIt(X
            If X > 10 Then
                A =
            End If 
        End Sub       
        '''
        client = vb2py.conversionserver.app.test_client()
        result = client.post('/single_code_module', data={'text': code, 'style': 'vb'})
        data = json.loads(result.data)
        self.assertEqual(True, data['parsing_failed'])
        self.assertEqual(1, data['parsing_stopped_vb'])

    def testParserInElseBlockFailure(self):
        """testParserInElseBlockFailure: can get to failing line in else"""
        code = '''
        Sub doIt(X)
            If X > 10 Then
                A = 12
            Else
                A =
            End If 
        End Sub       
        '''
        client = vb2py.conversionserver.app.test_client()
        result = client.post('/single_code_module', data={'text': code, 'style': 'vb'})
        data = json.loads(result.data)
        self.assertEqual(True, data['parsing_failed'])
        self.assertEqual(5, data['parsing_stopped_vb'])

    def testParserDirectiveFailure(self):
        """testDirectiveFailure: can get to failing line in directives"""
        code = '''
        Sub doIt(X)
            #If Win32 Then
                If X > 10 Then
                    A = 12
                Else
                    A =
                End If
            #End If 
        End Sub       
        '''
        client = vb2py.conversionserver.app.test_client()
        result = client.post('/single_code_module', data={'text': code, 'style': 'vb'})
        data = json.loads(result.data)
        self.assertEqual(True, data['parsing_failed'])
        self.assertEqual(6, data['parsing_stopped_vb'])

    def testParserWithFailure(self):
        """testWithFailure: can get to failing line in with"""
        code = '''
        Sub doIt(X)
            With Obj
                .X = 10
                If X > 10 Then
                    A = 12
                Else
                    A =
                End If
            End Onj
        End Sub       
        '''
        client = vb2py.conversionserver.app.test_client()
        result = client.post('/single_code_module', data={'text': code, 'style': 'vb'})
        data = json.loads(result.data)
        self.assertEqual(True, data['parsing_failed'])
        self.assertEqual(7, data['parsing_stopped_vb'])

    def testStripsOutForm(self):
        """testStripsOutForm: should strip out form section"""
        code = '''
VERSION 5.00
Begin VB.Form frmColors 
   BackColor       =   &H0000FF00&
   Caption         =   "Colorful form"
   ClientHeight    =   5715
   ClientLeft      =   60
   ClientTop       =   450
   ClientWidth     =   9195
   LinkTopic       =   "Form1"
   ScaleHeight     =   5715
   ScaleWidth      =   9195
   StartUpPosition =   3  'Windows Default
   Begin VB.ComboBox Combo1 
      BackColor       =   &H00C00000&
      ForeColor       =   &H00FFFFFF&
      Height          =   315
      ItemData        =   "frmColors.frx":0000
      Left            =   840
      List            =   "frmColors.frx":0013
      TabIndex        =   3
      Text            =   "Combo1"
      ToolTipText     =   "So should this"
      Top             =   2040
      Width           =   1935
   End
   Begin VB.ListBox List1 
      BackColor       =   &H00C0C000&
      ForeColor       =   &H000080FF&
      Height          =   2010
      ItemData        =   "frmColors.frx":0033
      Left            =   3480
      List            =   "frmColors.frx":0046
      TabIndex        =   2
      ToolTipText     =   "Do you see the tip"
      Top             =   360
      Width           =   2175
   End
   Begin VB.TextBox Text1 
      BackColor       =   &H000000FF&
      ForeColor       =   &H00FF00FF&
      Height          =   375
      Left            =   720
      TabIndex        =   1
      Text            =   "Text1"
      ToolTipText     =   "This should have a tip"
      Top             =   1200
      Width           =   2415
   End
   Begin VB.CommandButton Command1 
      BackColor       =   &H000000FF&
      Caption         =   "Command1"
      Height          =   855
      Left            =   720
      TabIndex        =   0
      ToolTipText     =   "Another tip"
      Top             =   240
      Width           =   1455
   End
   Begin VB.Label Label2 
      Caption         =   "Should see color + tooltips"
      Height          =   615
      Left            =   720
      TabIndex        =   5
      Top             =   3720
      Width           =   2895
   End
   Begin VB.Label Label1 
      BackColor       =   &H0000C0C0&
      Caption         =   "Can you hear me now?"
      ForeColor       =   &H00FFFF00&
      Height          =   375
      Left            =   1680
      TabIndex        =   4
      ToolTipText     =   "Am I tipped?"
      Top             =   2760
      Width           =   2655
   End
End

A = 1
        '''
        client = vb2py.conversionserver.app.test_client()
        result = client.post('/single_code_module', data={'text': code, 'style': 'vb'})
        data = json.loads(result.data)
        self.assertEqual(False, data['parsing_failed'])
        self.assertEqual(data['status'], 'OK')
        d = {}
        exec(data['result'], globals(), d)
        self.assertEqual(1, d['A'])

    def testStripsOutFormAndRetainsError(self):
        """testStripsOutFormAndRetainsError: should strip out form section and have correct line"""
        code = '''
VERSION 5.00
Begin VB.Form frmColors 
   BackColor       =   &H0000FF00&
   Caption         =   "Colorful form"
   ClientHeight    =   5715
   ClientLeft      =   60
   ClientTop       =   450
   ClientWidth     =   9195
   LinkTopic       =   "Form1"
   ScaleHeight     =   5715
   ScaleWidth      =   9195
   StartUpPosition =   3  'Windows Default
   Begin VB.ComboBox Combo1 
      BackColor       =   &H00C00000&
      ForeColor       =   &H00FFFFFF&
      Height          =   315
      ItemData        =   "frmColors.frx":0000
      Left            =   840
      List            =   "frmColors.frx":0013
      TabIndex        =   3
      Text            =   "Combo1"
      ToolTipText     =   "So should this"
      Top             =   2040
      Width           =   1935
   End
   Begin VB.ListBox List1 
      BackColor       =   &H00C0C000&
      ForeColor       =   &H000080FF&
      Height          =   2010
      ItemData        =   "frmColors.frx":0033
      Left            =   3480
      List            =   "frmColors.frx":0046
      TabIndex        =   2
      ToolTipText     =   "Do you see the tip"
      Top             =   360
      Width           =   2175
   End
   Begin VB.TextBox Text1 
      BackColor       =   &H000000FF&
      ForeColor       =   &H00FF00FF&
      Height          =   375
      Left            =   720
      TabIndex        =   1
      Text            =   "Text1"
      ToolTipText     =   "This should have a tip"
      Top             =   1200
      Width           =   2415
   End
   Begin VB.CommandButton Command1 
      BackColor       =   &H000000FF&
      Caption         =   "Command1"
      Height          =   855
      Left            =   720
      TabIndex        =   0
      ToolTipText     =   "Another tip"
      Top             =   240
      Width           =   1455
   End
   Begin VB.Label Label2 
      Caption         =   "Should see color + tooltips"
      Height          =   615
      Left            =   720
      TabIndex        =   5
      Top             =   3720
      Width           =   2895
   End
   Begin VB.Label Label1 
      BackColor       =   &H0000C0C0&
      Caption         =   "Can you hear me now?"
      ForeColor       =   &H00FFFF00&
      Height          =   375
      Left            =   1680
      TabIndex        =   4
      ToolTipText     =   "Am I tipped?"
      Top             =   2760
      Width           =   2655
   End
End

A = 1
B =
        '''
        client = vb2py.conversionserver.app.test_client()
        result = client.post('/single_code_module', data={'text': code, 'style': 'vb'})
        data = json.loads(result.data)
        self.assertEqual(True, data['parsing_failed'])
        self.assertEqual(data['status'], 'OK')
        self.assertEqual(81, data['parsing_stopped_vb'])
        self.assertEqual(6, data['parsing_stopped_py'])

    def testCanDetectVBDotNet(self):
        """testCanDetectVBDotNet: can detect a dot net module"""
        code = '''
        Public Class Test
            DoIt()
        End Class
        '''
        client = vb2py.conversionserver.app.test_client()
        result = client.post('/single_class_module', data={'text': code, 'style': 'vb', 'dialect': 'detect'})
        data = json.loads(result.data)
        self.assertEqual(False, data['parsing_failed'])
        self.assertEqual(data['status'], 'OK')
        self.assertEqual(data['language'], 'VB.NET')

    def testDotNetUsesRightGrammar(self):
        """testDotNetUsesRightGrammar: when detecting .Net should use the right dialect"""
        code = '''
        Public Class Mine
            Public Function Test()
                Return 10
            End Function
        End Class
        '''
        client = vb2py.conversionserver.app.test_client()
        result = client.post('/single_class_module', data={'text': code, 'style': 'vb'})
        data = json.loads(result.data)
        self.assertIn("return Integer(10)", data['result'])

    def testDotNetRetainsClassName(self):
        """testDotNetRetainsClassName: dot net module should respect the coded class name"""
        code = '''
        Public Class Bob
            a = 1
        End Class
        '''
        client = vb2py.conversionserver.app.test_client()
        result = client.post('/single_class_module', data={'text': code, 'style': 'vb', 'class_name': 'Fred'})
        data = json.loads(result.data)
        d = {}
        exec(data['result'], globals(), d)
        self.assertEqual(d['Bob'].a, 1)

    def testCanDetectVB6Module(self):
        """testCanDetectVB6Module: should be able to detect VB6"""
        code = '''
        Sub doIt(X)
            With Obj
                .X = 10
                If X > 10 Then
                    A = 12
                Else
                    A = 10
                End If
            End With
        End Sub  
        '''
        client = vb2py.conversionserver.app.test_client()
        result = client.post('/single_class_module', data={'text': code, 'style': 'vb'})
        data = json.loads(result.data)
        self.assertEqual(False, data['parsing_failed'])
        self.assertEqual(data['status'], 'OK')
        self.assertEqual(data['language'], 'VB6')

    def testCanForceDialect(self):
        """testCanForceDialect: should be able to force dialect"""
        code = 'A = 10'
        client = vb2py.conversionserver.app.test_client()
        result = client.post('/single_class_module', data={'text': code, 'style': 'vb'})
        data = json.loads(result.data)
        self.assertEqual(False, data['parsing_failed'])
        self.assertEqual(data['status'], 'OK')
        self.assertEqual(data['language'], 'VB6')
        self.assertIn('A = 10', data['result'])
        #
        result = client.post('/single_class_module', data={'text': code, 'style': 'vb', 'dialect': 'VB6'})
        data = json.loads(result.data)
        self.assertEqual(False, data['parsing_failed'])
        self.assertEqual(data['status'], 'OK')
        self.assertEqual(data['language'], 'VB6')
        self.assertIn('A = 10', data['result'])
        #
        result = client.post('/single_class_module', data={'text': code, 'style': 'vb', 'dialect': 'VB.NET'})
        data = json.loads(result.data)
        self.assertEqual(False, data['parsing_failed'])
        self.assertEqual(data['status'], 'OK')
        self.assertEqual(data['language'], 'VB.NET')
        self.assertIn('A = Integer(10)', data['result'])

    def testDotNetClassNames(self):
        """testDotNetClassNames: can manually and automatically set .NET class names"""
        #
        # Manually set the name
        code = "A = 1"
        client = vb2py.conversionserver.app.test_client()
        result = client.post('/single_class_module', data={'text': code, 'style': 'vb', 'dialect': 'VB.NET', 'class_name': 'TEST'})
        data = json.loads(result.data)
        self.assertIn('class TEST', data['result'])
        #
        # Automatically overrides is
        code = "class OTHER\nA = 1\nEnd Class"
        client = vb2py.conversionserver.app.test_client()
        result = client.post('/single_class_module', data={'text': code, 'style': 'vb', 'dialect': 'VB.NET', 'class_name': 'TEST'})
        data = json.loads(result.data)
        self.assertNotIn('class TEST', data['result'])
        self.assertIn('class OTHER', data['result'])

    def testCanGetVersionNumber(self):
        """testCanGetVersionNumber: should return the version number used"""
        code = '''
        Sub doIt(X)
            With Obj
                .X = 10
                If X > 10 Then
                    A = 12
                Else
                    A = 10
                End If
            End With
        End Sub  
        '''
        client = vb2py.conversionserver.app.test_client()
        result = client.post('/single_class_module', data={'text': code, 'style': 'vb'})
        data = json.loads(result.data)
        self.assertEqual(data['version'], vb2py.converter.__version__)

    def testCanDoQuickFailMode(self):
        """testCanDoQuickFailMode: can do conversion without error lines"""
        code = '''
        Sub doIt(X)
            If X > 10 Then
                A =
            End If 
        End Sub       
        '''
        client = vb2py.conversionserver.app.test_client()
        result = client.post('/single_code_module', data={'text': code, 'style': 'vb', 'failure-mode': 'quick'})
        data = json.loads(result.data)
        self.assertEqual(True, data['parsing_failed'])
        self.assertEqual(0, data['parsing_stopped_vb'])

    def testCanDoFailSafeMode(self):
        """testCanDoFailSafeMode: should be able to do fail safe mode"""
        code = '''
        Sub doIt(X)
            If X > 10 Then
                A =
            End If 
            B =
            For I error = 1 To 3
              C = 10
            Next
        End Sub       
        '''
        client = vb2py.conversionserver.app.test_client()
        result = client.post('/single_code_module', data={'text': code, 'style': 'vb', 'failure-mode': 'fail-safe'})
        data = json.loads(result.data)
        self.assertEqual(True, data['parsing_failed'])
        self.assertEqual([3, 5, 6, 8], data['parsing_stopped_vb'])

    
if __name__ == '__main__':
    main()
