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
        "Dim A, B, C, D, E, F",
        "Dim A ,B As Collection",
        "Dim B As String, B As Long, B As Integer, B As String, B As String",
        "Dim variable As Object.OtherObj, B, C, D, E",
        "Dim Var As Variant",
        "Dim A, B, C As New Collection",
        "Dim E As New Collection, F As New Object, F, G",
        "Dim H As New Object, G As New Object",
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
