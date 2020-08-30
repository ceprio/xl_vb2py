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

# Simple assignments
tests.extend([
        "a = fn(AddressOf fn)",
        "a = fn(a, b, c, AddressOf fn)",
        "a = fn(a, AddressOf b, AddressOf c, AddressOf fn)",
        "a = fn(a, AddressOf b.m.m, AddressOf c.k.l, AddressOf fn)",
        "a = AddressOf b",
        "DoIt AddressOf b",
        "DoIt AddressOf b, That",
        "DoIt This, AddressOf b",
])

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
