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
        "If a = 10 Then b = 20",
        "If a = 20 And b = 5 Then d = 123",
        "If a = 12 Then d = 1 Else g = 5",
        "If a = 10 Then doit",
        "If a = 10 Then doit 10, 20, 30",
        "If a = 10 Then doit Else dont",
        "If a = 10 Then doit 10, 20, 30 Else dont",
        "If a = 10 Then doit 10, 20, 30 Else dont 5, 10, 15",
        "If a = 10 Then Exit Function",
        "If a = 10 Then Exit Function Else DoIt",
        "If a = 10 Then Exit Function Else DoIt=1",
        "If a = 10 Then Exit Function Else DoIt 1, 2, 3",
        "If a = 10 Then DoIt Else Exit Function",
        "If a = 10 Then DoIt=1 Else Exit Function",
        "If a = 10 Then DoIt 1,2,34 Else Exit Function",
        "If a = 10 Then Remove X",
        "If ip Then i1 = ip: b = 1  Else i1 = 0",
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
