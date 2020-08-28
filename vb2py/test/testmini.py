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

# Nested do  loop with line numbers

tests.extend([
"""
Enum thing
    _one = 1
    _two = 2
    _three = 3
    _four = 4
End Enum
""",
"""
Enum thing
    _one
    _two
    _three
    _four
End Enum
""",
"""
Public Enum Stats
xStrength = 1
Endurance
xIntelligence
Agility
Spirit
Stat_count
End Enum
""",
    """
Public Enum Stats As Integer
xStrength = 1
Endurance
xIntelligence
Agility
Spirit
Stat_count
End Enum
"""
])

vb_dot_net_tests = []




class ParsingTest(unittest.TestCase):
    """Holder class which gets built into a whole test case"""


def getTestMethod(vb, dialect='VB6'):
    """Create a test method"""
    def testMethod(self):
        try:
            buildParseTree(vb, dialect=dialect)
        except VBParserError:
            raise Exception("Unable to parse ...\n%s" % vb)
    return testMethod

#
# Add tests to main test class
for idx in range(len(tests)):
    setattr(ParsingTest, "test%d" % idx, getTestMethod(tests[idx]))


for idx in range(len(vb_dot_net_tests)):
    setattr(ParsingTest, "dot_net_test%d" % idx, getTestMethod(vb_dot_net_tests[idx], dialect='vb.net'))


if __name__ == "__main__":
    unittest.main()
