"""Test of the different grammar modes and settings"""

import re
import unittest
import vb2py.utils
import vb2py.vbparser
import vb2py.parserclasses


class TestGrammarModes(unittest.TestCase):

    def tearDown(self):
        """Tear down the tests"""
        self._setVB6()

    def assertParserFails(self, text, num_blocks):
        """Check that parsing fails for some text"""
        result = vb2py.vbparser.parseVB(text)
        self.assertEqual(len(result.blocks), num_blocks)
        self.assertIsInstance(result.blocks[num_blocks - 1], vb2py.parserclasses.VBParserFailure)

    def assertParsesAndContains(self, text, expected, num_failures=1):
        """Check that parsing succeeds and a bit of text is included"""
        result = vb2py.vbparser.parseVB(text)
        result_text = result.renderAsCode()
        self.assertIn(expected, result_text)
        self.assertEqual(num_failures, len(re.findall('UNTRANSLATED', result_text)))
        return result_text

    def assertParses(self, text):
        """Check that parsing succeeds"""
        result = vb2py.vbparser.parseVB(text)
        result_text = result.renderAsCode()
        self.assertEqual(0, len(re.findall('UNTRANSLATED', result_text)))
        self.assertEqual(0, len(re.findall('ParserError', result_text)))
        return result_text

    def _setDotNet(self):
        """Set .net mode on"""
        vb2py.utils.BASE_GRAMMAR_SETTINGS['dialect'] = 'vb.net'

    def _setVB6(self):
        """Set VB6 mode on"""
        vb2py.utils.BASE_GRAMMAR_SETTINGS['dialect'] = 'VB6'


class TestSafeMode(TestGrammarModes):
    """Test of the SafeMode class"""

    def setUp(self):
        """Set up the tests"""

    def _setSafe(self):
        """Set safe mode on"""
        vb2py.utils.BASE_GRAMMAR_SETTINGS['mode'] = 'safe'

    def _setUnsafe(self):
        """Set safe mode off"""
        vb2py.utils.BASE_GRAMMAR_SETTINGS['mode'] = 'rigorous'

    def testSingleLine(self):
        """testSingleLine: single line works in safe mode"""
        text = 'a ='
        self._setUnsafe()
        self.assertParserFails(text, 1)
        self._setSafe()
        self.assertParsesAndContains(text, '[a =]', 1)

    def testLineInBlock(self):
        """testLineInBlock: line a block works"""
        self._setDotNet()
        text = 'a = 1\nb =\nc = 2\nd ='
        self._setUnsafe()
        self.assertParserFails(text, 2)
        self._setSafe()
        self.assertParsesAndContains(text, 'a = Integer(1)', 2)
        self.assertParsesAndContains(text, '[b =]', 2)
        self.assertParsesAndContains(text, 'c = Integer(2)', 2)
        self.assertParsesAndContains(text, '[d =]', 2)

    def testForStart(self):
        """testForStart: works with a failure during the first line of a for"""
        text = 'For i error = 1 To 20\nB = B + 1\nNext i\n'
        self._setUnsafe()
        self.assertParserFails(text, 1)
        self._setSafe()
        self.assertParsesAndContains(text, '[For i error = 1 To 20]', 2)
        self.assertParsesAndContains(text, '[Next i]', 2)

    def testForEnd(self):
        """testForEnd: works with a failure during the last line of a for"""
        text = 'For i = 1 To 20\nB = B + 1\n'
        self._setUnsafe()
        self.assertParserFails(text, 1)
        self._setSafe()
        self.assertParsesAndContains(text, '[For i = 1 To 20]')

    def testSubWithInnerError(self):
        """testSubWithInnerError: should be able to do a sub with inner error"""
        text = 'Sub DoIt()\na =\nEnd Sub'
        self._setUnsafe()
        self.assertParserFails(text, 1)
        self._setSafe()
        self.assertParsesAndContains(text, '[a =]')

    def testSubWithInnerBlockError(self):
        """testSubWithInnerBlockError: should be able to do a sub with inner block error"""
        text = 'Sub DoIt()\nFor i  = 1 To 10\na =\nNext i\nEnd Sub'
        self._setUnsafe()
        self.assertParserFails(text, 1)
        self._setSafe()
        self.assertParsesAndContains(text, '[a =]', 1)

    def testSafeInlineIf(self):
        """testSafeInlineIf: should be able to work with inline if"""
        self._setUnsafe()
        self.assertParses('If X Then DoIt')
        self._setSafe()
        self.assertParses('If X Then DoIt')

    def testIfAndElseIf(self):
        """testIfAndElseIf: should handle ElseIf"""
        text = """
            If A = 10 Then
                    DoSomething()
            ElseIf  B = 20 Then
                    DoSomethingElse()
            Else
                    OtherCase()
                    If B = 20 Then C = 0 Else C = 1
            End If        
        """
        self._setSafe()
        self.assertParses(text)

    def testIfWithOneBlock(self):
        """testIfWithOneBlock: should handle a single block if"""
        text = """
            If A = 10 Then
                b = b -
            End If
        """
        self._setSafe()
        self.assertParsesAndContains(text, "[b = b -]", 1)

    def testWhile(self):
        """testWhile: while should work"""
        text = """
            While A
            Wend   
            
            Do Until A
            Loop    
            
            Do
            Loop Until a
        """
        self._setSafe()
        self.assertParses(text)

    def testSelect(self):
        """testSelect: should zoom in on a select clause"""
        text = """
                Select Case A
                    Case 1
                        B = B + X
                    Case 2
                        B = B - 
                    Case Else
                        B = 0
                    End Select
        """
        self._setSafe()
        self.assertParsesAndContains(text, "[B = B -]", 1)

    def testImplicitCall(self):
        """testImplicitCall: implicit call should work"""
        text = 'DoIt'
        self._setUnsafe()
        self.assertParsesAndContains(text, 'DoIt()', 0)
        self._setSafe()
        self.assertParsesAndContains(text, 'DoIt()', 0)

    def testDoubleElseIf(self):
        """testDoubleElseIf: safe mode with double elseif should work"""
        text = '''
            If A Then
            ElseIf B Then
            ElseIf C Then
            End If        
        '''
        self._setUnsafe()
        self.assertParses(text)
        self._setSafe()
        self.assertParses(text)


class TestDotNet(TestGrammarModes):
    """Test of the .net conversion dialect"""

    def testDotNetFunctionReturns(self):
        """testDotNetFunctionReturns: return should be simplified in .net"""
        text = """
        Function A()
            Return 10
        End Function
        """
        self._setDotNet()
        r = self.assertParses(text)
        self.assertIn('return Integer(10)', r)

    def testClassAsKeyword(self):
        """testClassAsKeyword: class as keyword should be OK in VB6"""
        text = 'Class = 1'
        self._setVB6()
        self.assertParses(text)
        self._setDotNet()
        self.assertParserFails(text, 1)


if __name__ == '__main__':
    unittest.main()