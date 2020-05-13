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


# #If
tests.append("""
#If a = 10 Then
    b = 20
#Else
    c=2
#End If
#If c < 1 Then
    d = 15
#Else
    c=2
#End If
""")

# Empty #If
tests.append("""
#If a = 10 Then
#Else
    c=2
#End If
""")

# Empty #If with comments
tests.append("""
#If a = 10 Then ' comment here
#Else
    c=2
#End If
""")

# Simple #If with And/Or
tests.append("""
#If a = 10 And k = "test" Then
    b = 20
#Else
    c=2
#End If
#If c < 1 Or d Then
    d = 15
#Else
    c=2
#End If
""")

# If with comments at end
tests.append('''
#If Debug
    DoIt
#End If     ' 
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
