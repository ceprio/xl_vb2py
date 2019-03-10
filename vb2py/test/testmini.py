#
# Turn off logging in extensions (too loud!)
import vb2py.extensions
import unittest
vb2py.extensions.disableLogging()

from vb2py.vbparser import buildParseTree, VBParserError

#
# Set some config options which are appropriate for testing
import vb2py.config
Config = vb2py.config.VB2PYConfig()
Config.setLocalOveride("General", "ReportPartialConversion", "No")


tests = []



tests.extend([
'a = fn(ByVal b)',
'a = fn(x, y, z, ByVal b)',
'a = fn(x, y, z, ByVal b, 10, 20, 30)',
'a = fn(ByVal a, ByVal b, ByVal c)',
'a = fn(ByRef b)',
'a = fn(x, y, z, ByRef b)',
'a = fn(x, y, z, ByRef b, 10, 20, 30)',
'a = fn(ByRef a, ByRef b, ByRef c)',
'fn ByVal b',
'fn x, y, z, ByVal b',
'fn x, y, z, ByVal b, 10, 20, 30',
'fn ByVal a, ByVal b, ByVal c',
'fn ByRef b',
'fn x, y, z, ByRef b',
'fn x, y, z, ByRef b, 10, 20, 30',
'fn ByRef a, ByRef b, ByRef c',

])





class ParsingTest(unittest.TestCase):
    """Holder class which gets built into a whole test case"""


def getTestMethod(vb):
    """Create a test method"""
    def testMethod(self):
        try:
            buildParseTree(vb)
        except VBParserError:
            raise "Unable to parse ...\n%s" % vb
    return testMethod

#
# Add tests to main test class
for idx in range(len(tests)):
    setattr(ParsingTest, "test%d" % idx, getTestMethod(tests[idx]))


if __name__ == "__main__":
    unittest.main()
