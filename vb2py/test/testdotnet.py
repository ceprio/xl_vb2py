# -*- coding: latin-1 -*-

#
# Turn off logging in extensions (too loud!)
from testframework import *
import vb2py.extensions
import vb2py.utils
vb2py.extensions.disableLogging()

from vb2py.vbparser import buildParseTree, VBParserError

#
# Set some config options which are appropriate for testing
import vb2py.config
Config = vb2py.config.VB2PYConfig()
Config.setLocalOveride("General", "ReportPartialConversion", "No")




tests = []

# String methods
tests.extend([
    'a = "hello".Length',
    'a = ("hello").Length',
    'a = ("hello" + "world").Length',
    'a = ("hello" + "world").Length + 2',
])




# Expression calls
tests.extend([
    '(a + b).Truncate()',
])

tests.append(
    """
Function B()
    Return 12
End Function             
    """
)




class ParsingTest(unittest.TestCase):
    """Holder class which gets built into a whole test case"""


def getTestMethod(vb):
    """Create a test method"""
    def testMethod(self):
        try:
            buildParseTree(vb, dialect='vb.net')
        except VBParserError:
            raise Exception("Unable to parse ...\n%s" % vb)
    return testMethod


# Add tests to main test class
for idx in range(len(tests)):
    setattr(ParsingTest, "test%d" % idx, getTestMethod(tests[idx]))


if __name__ == "__main__":
    main()
