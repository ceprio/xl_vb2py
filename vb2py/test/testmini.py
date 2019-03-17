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

# Simple expressions
tests.extend([
'a = 10',
'a = 20+30',
'a = "hello there"',
'a = 10',
'a = Array(10,20)',
'a = myfunction.mymethod(10)',
'a = &HFF',
'a = &HFF&',
'a = #1/10/2000#',
'a = #1/10/2000 11:59#',
'a = #1/10/2000 11:59:12#',
'a = #1/10/2000 11:59:12 PM#',
'a = #1/10/2000 11:59:12 AM#',
'a = #1/10#',
'a = 10 Mod 2',
'a = 1000!',
])

class ParsingTest(unittest.TestCase):
    """Holder class which gets built into a whole test case"""


def getTestMethod(vb):
    """Create a test method"""
    def testMethod(self):
        try:
            buildParseTree(vb)
        except VBParserError:
            raise Exception("Unable to parse ...\n%s" % vb)
    return testMethod

#
# Add tests to main test class
for idx in range(len(tests)):
    setattr(ParsingTest, "test%d" % idx, getTestMethod(tests[idx]))


if __name__ == "__main__":
    unittest.main()
