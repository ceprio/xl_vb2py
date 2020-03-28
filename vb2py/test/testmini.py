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

# comments and colons in awkward places
tests.extend([
"""
If a =0 Then ' nasty comment
    b=1
End If ' other nasty comment
""",

"""
While a<0 ' nasty comment
    b=1
Wend ' other nasty comment
""",

"""
Select Case a ' nasty comment
Case 10 ' oops
    b=1
Case Else ' other nasty comment
    b = 2
End Select ' gotcha
""",

"""
For i = 0 To 100 ' nasty comment
    b=1
Next i ' other nasty comment
""",

"""
Sub a() ' nasty comment
    b=1
End Sub ' other nasty comment
""",

"""
Function f() ' nasty comment
    b=1
End Function ' other nasty comment
""",

"""
Sub a():
    b=1
End Sub 
""",


"""
Sub a()
    b=1
End Sub: 
""",

"""
Sub a
    b=12
End Sub 
""",


"""
Function a
    b=1
End Function
""",

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
