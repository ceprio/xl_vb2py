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

# Subroutines and functions with ParamArray
tests.append('''
Sub A(X, Y, ParamArray Z() As String)
    DoIt(Z)
End Sub
''')

tests.append('''
Sub A(X, Y, ParamArray Z() As Integer)
    DoIt(Z)
End Sub
''')

tests.append('''
Sub A(X, Y, ByVal ParamArray Z() As Integer)
    DoIt(Z)
End Sub
''')

tests.append('''
Function A(X, Y, ByVal ParamArray Z() As Integer)
    DoIt(Z)
End Function
''')
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
