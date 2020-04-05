"""Test of the different grammar modes and settings"""

import unittest
import vb2py.utils
import vb2py.vbparser
import vb2py.parserclasses


class TestSafeMode(unittest.TestCase):
    """Test of the SafeMode class"""

    def setUp(self):
        """Set up the tests"""

    def tearDown(self):
        """Tear down the tests"""

    def _setSafe(self):
        """Set safe mode on"""
        vb2py.utils.BASE_GRAMMAR_SETTINGS['mode'] = 'safe'

    def _setUnsafe(self):
        """Set safe mode off"""
        vb2py.utils.BASE_GRAMMAR_SETTINGS['mode'] = 'rigorous'

    def assertParserFails(self, text, num_blocks):
        """Check that parsing fails for some text"""
        result = vb2py.vbparser.parseVB(text)
        self.assertEqual(len(result.blocks), num_blocks)
        self.assertIsInstance(result.blocks[num_blocks - 1], vb2py.parserclasses.VBParserFailure)

    def assertParsesAndContains(self, text, expected):
        """Check that parsing succeeds and a bit of text is included"""
        result = vb2py.vbparser.parseVB(text)
        result_text = result.renderAsCode()
        self.assertIn(expected, result_text)

    def testSingleLine(self):
        """testSingleLine: single line works in safe mode"""
        text = 'a ='
        self._setUnsafe()
        self.assertParserFails(text, 1)
        self._setSafe()
        self.assertParsesAndContains(text, '[a =]')

    def testLineInBlock(self):
        """testLineInBlock: line a block works"""
        text = 'a = 1\nb =\nc = 2\nd ='
        self._setUnsafe()
        self.assertParserFails(text, 2)
        self._setSafe()
        self.assertParsesAndContains(text, 'a = 1')
        self.assertParsesAndContains(text, '[b =]')
        self.assertParsesAndContains(text, 'c = 2')
        self.assertParsesAndContains(text, '[d =]')

    def testForStart(self):
        """testForStart: works with a failure during the first line of a for"""
        text = 'For i error = 1 To 20\nB = B + 1\nNext i\n'
        self._setUnsafe()
        self.assertParserFails(text, 1)
        self._setSafe()
        self.assertParsesAndContains(text, '[For i error = 1 To 20]')
        self.assertParsesAndContains(text, '[Next i]')

    def testForEnd(self):
        """testForEnd: works with a failure during the last line of a for"""
        text = 'For i = 1 To 20\nB = B + 1\n'
        self._setUnsafe()
        self.assertParserFails(text, 1)
        self._setSafe()
        self.assertParsesAndContains(text, '[For i = 1 To 20]')





if __name__ == '__main__':
    unittest.main()