# -*- coding: latin-1 -*-

#
# Turn off logging in extensions (too loud!)
import vb2py.extensions
import vb2py.utils
vb2py.extensions.disableLogging()

from vb2py.vbparser import buildParseTree, VBParserError

#
# Set some config options which are appropriate for testing
import vb2py.config
Config = vb2py.config.VB2PYConfig()
Config.setLocalOveride("General", "ReportPartialConversion", "No")

import unittest


tests = []


# Simple assignments
tests.append("""
a = 10
b = 20+30
c = "hello there"
oneVal = 10
twoVals = Array(10,20)
functioncall = myfunction.mymethod(10)


""")


dot_net_grammar = vb2py.utils.loadGrammarFrom(
    vb2py.utils.relativePath('grammars', 'vbgrammar.mako'),
    data={
        'dialect': 'vb.net',
    }
)


class ParsingTest(unittest.TestCase):
    """Holder class which gets built into a whole test case"""


def getTestMethod(vb):
    """Create a test method"""
    def testMethod(self):
        try:
            buildParseTree(vb, grammar=dot_net_grammar)
        except VBParserError:
            raise Exception("Unable to parse ...\n%s" % vb)
    return testMethod

#
# Add tests to main test class
for idx in range(len(tests)):
    setattr(ParsingTest, "test%d" % idx, getTestMethod(tests[idx]))


if __name__ == "__main__":
    unittest.main()