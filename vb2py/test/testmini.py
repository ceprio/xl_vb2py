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
'a = 10',
'a = 20+30',
'a = "hello there"',
'a = 10',
'a = Array(10,20)',
'a = myfunction.mymethod(10)',
'a = &HFF',
'a = &HFF00000L',
'a = &HFF&',
'a = #1/10/2000#',
'a = #1/10/2000 11:59#',
'a = #1/10/2000 11:59:12#',
'a = #1/10/2000 11:59:12 PM#',
'a = #1/10/2000 11:59:12 AM#',
'a = #11:59:12 AM#',
'a = #11:59:12#',
'a = #1/10#',
'a = 1#',
'a = 1.#',
'a = 1.2#',
'a = 10 Mod 2',
'a = 1000!',
'a = "12!12"',
'a = "=VLOOKUP(RC[-4],[Temp2.xlsx]Sheet1!C3C55,38,0)"',
'Range("X1").Select\nActiveWorkbook.Names.Add Name:="scrollx1", RefersToR1C1:="=OFFSET(All_logs!R2C19:R120C19,All_logs!R1C22,0,All_logs!R1C24,1)"',
])

tests.extend
vb_dot_net_tests = []

# Closures
# Decorators



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
