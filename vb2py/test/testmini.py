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

tests.append(("""
Global _a() As String
b = (_a="") ' Check we got an array not a string
ReDim _a(10)
_a(1) = "hello"
_a(10) = "bye"
c = _a(1)
d = _a(10)
"""
))
# Simple dims
tests.extend([
        "Dim A",
        "Dim B As String",
        "Dim variable As Object.OtherObj",
        "Dim Var As Variant",
        "Dim A As String * 100",
        "Dim A (10)",
])

# Dims with New
tests.extend([
        "Dim A As New Object",
        "Dim B As New Collection",
])

# Multiple dims on one line
tests.extend([
        "Dim A, B, C, D, E, F",
        "Dim B As String, B As Long, B As Integer, B As String, B As String",
        "Dim variable As Object.OtherObj, B, C, D, E",
        "Dim Var As Variant",
        "Dim A, B, C As New Collection",
        "Dim E As New Collection, F As New Object, F, G",
        "Dim H As New Object, G As New Object",
])

# Array type dims
tests.extend([
        "Dim A()",
        "Dim B(10, 20, 30) As String",
        "Dim variable() As Object.OtherObj",
        "Dim Var(mysize) As Variant",
])

# Scoped dims
tests.extend([
        "Public A",
        "Private B As String",
        "Private A, B, C, D, E, F",
        "Private B As String, B As Long, B As Integer, B As String, B As String",
        "Private variable As Object.OtherObj, B, C, D, E",
        "Public Var As Variant",
])

# Static dims
tests.extend([
        "Static A",
        "Static B As String",
        "Static A, B, C, D, E, F",
        "Static B As String, B As Long, B As Integer, B As String, B As String",
        "Static variable As Object.OtherObj, B, C, D, E",
        "Static Var As Variant",
])

# Arrays
tests.extend([
    "Dim a(10)",
    "Dim a(0)",
    "Dim a(0), b(20), c(30)",
    "Dim a(10+20)",
    "Dim a(10+20, 1+3)",
    "Dim a(1 To 10)",
    "Dim a(1 To 10, 5 To 20)",
])

# Redims
tests.extend([
    "ReDim a(10)",
    "ReDim a(0)",
    "ReDim Preserve a(20)",
    "ReDim a(0), b(20), c(30)",
    "ReDim Preserve a(20), b(20)",
    "ReDim a(10+20)",
    "ReDim a(10+20, 1+3)",
    "ReDim a(1 To 10)",
    "ReDim a(1 To 10, 5 To 20)",
])


# Complex examples
tests.extend([
"""
With Obj
    ReDim .Child(10)
End With
""",
"Dim A(10).B(10)",
"Dim A(10).B.C(10) As Object",

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
