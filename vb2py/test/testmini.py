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


# Two line continuations
tests.append("""
a = _
10 + 20 + 30
b = 10/ _
25
c = (one + _
     two + three)
""")

# Milti-line continuations
tests.append("""
a = _
      10 + 20 + 30 _
    * 10/ _
      25
c = (one + _
     two + three) * _
     four.five()
""")

# 880612 Continuation character inside call
tests.append("""
Sub MySub _
(ByVal a, ByRef y)
a=10
n=20
c="hello"
End Sub
""")

# Continuation using a comment
tests.append("' This is a comment a _\n= 1 /")
tests.append("B = 10 ' This is a comment a _\n= 1 /")

# Continuation with a blank line
tests.append("a = 1 _\n\nb = 2")

# Continuation within a with
tests.append('''
With A
  If LenB(contntMD5) <> 0 Then _
   .setRequestHeader "Content-MD5", contntMD5
End With
''')

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
