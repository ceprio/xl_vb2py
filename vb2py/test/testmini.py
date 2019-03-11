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

# Empty Do's
tests.append("Property Get Position() As Long: Position = Loc(mFileNumber): End Property")
tests.append("""
Property Get Position() As Long: Position = Loc(mFileNumber)
End Property
""")
tests.append("""
Property Get Position() As Long
Position = Loc(mFileNumber): End Property
""")

tests.extend(["""
Property Let MyProp(NewVal As String)
 a = NewVal
 Exit Property
End Property
""",
"""
Property Get MyProp() As Long
 MyProp = NewVal
 Exit Property
End Property
""",
"""
Property Set MyProp(NewObject As Object) 
 Set MyProp = NewVal
 Exit Property
End Property
"""
"""
Public Property Let MyProp(NewVal As String)
 a = NewVal
End Property
""",
"""
Public Property Get MyProp() As Long
 MyProp = NewVal
End Property
""",
"""
Public Property Set MyProp(NewObject As Object) 
 Set MyProp = NewVal
End Property
""",
"""
Public Property Get MyProp(   ) As Long
 MyProp = NewVal
End Property
""",
])

# Simple property let/get/set with labels
tests.extend(["""
1: Property Let MyProp(NewVal As String)
1:  a = NewVal
1: End Property
""",
"""
1: Property Get MyProp() As Long
1:  MyProp = NewVal
1: End Property
""",
"""
1: Property Set MyProp(NewObject As Object) 
1:  Set MyProp = NewVal
1: End Property
"""
])

# Simple property let/get/set with labels and comment
tests.extend(["""
1: Property Let MyProp(NewVal As String) ' comment
1:  a = NewVal  ' comment
1: End Property  ' comment
""",
"""
1: Property Get MyProp() As Long  ' comment
1:  MyProp = NewVal  ' comment
1: End Property  ' comment
""",
"""
1: Property Set MyProp(NewObject As Object)   ' comment
1:  Set MyProp = NewVal  ' comment
1: End Property  ' comment
"""
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
