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

# << Parsing tests >> (60 of 61)
# Simple enumeration
tests.append("""
Enum MyEnum
    one
    two
    three
    four
    five
End Enum
""")


# Scoped enumeration
tests.append("""
Public Enum MyEnum
    one
    two
    three
    four
    five
End Enum
""")

tests.append("""
Private Enum MyEnum
    one
    two
    three
    four
    five
End Enum
""")

# Simple enumeration with comments
tests.append("""
Enum MyEnum ' yeah
    one ' this 
    two ' is 
    three
    four ' neat
    five
End Enum
""")

# Simple enumeration with whole line comments
tests.append("""
Enum MyEnum ' yeah
    one 
    ' this 
    two 
    ' is 
    three
    four 
    ' neat
    ' oh
    five
End Enum
""")




class ParsingTest(unittest.TestCase):
    """Holder class which gets built into a whole test case"""


def getTestMethod(vb):
    """Create a test method"""
    def testMethod(self):
        try:
            buildParseTree(vb)
        except VBParserError:
            raise "Unable to parse ...\n%s" % vb
    return testMethod

#
# Add tests to main test class
for idx in range(len(tests)):
    setattr(ParsingTest, "test%d" % idx, getTestMethod(tests[idx]))


if __name__ == "__main__":
    unittest.main()
