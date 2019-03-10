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

# Conditional expressions
tests.extend(["a = a = 1",
              "a = a <> 10",
              "a = a > 10",
              "a = a < 10",
              "a = a <= 10",
              "a = a >= 10",
              "a = a = 1 And b = 2",
              "a = a = 1 Or b = 2",
              "a = a Or b",
              "a = a Or Not b",
              "a = Not a = 1",
              "a = Not a",
              "a = a Xor b",
              "a = b Is Nothing",
              "a = b \ 2",
              "a = b Like c",
              'a = "hello" Like "goodbye"',
              'a = x Imp b',
])

#

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
