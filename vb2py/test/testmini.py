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

# Constants with different types
tests.extend([
    "Const a = 10",
    'Const a = "Hello"',
    "Const a = &HA1",
    "Const a = 1#",
    "Const a = 1%",
    "Const a = 1&",
    "Const a = 1@",
    "Public Const a = 10",
    'Public Const a = "Hello"',
    "Public Const a = &HA1",
    "Public Const a = 1#",
    "Public Const a = 1%",
    "Public Const a = 1&",
    "Private Const a = 10",
    'Private Const a = "Hello"',
    "Private Const a = &HA1",
    "Private Const a = 1#",
    "Private Const a = 1%",
    "Private Const a = 1&",
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
