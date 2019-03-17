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

tests.append("""
Public Enum KeyRoot
[HKEY_CLASSES_ROOT] = &H80000000 'stores OLE class information and file associations
[HKEY_CURRENT_CONFIG] = &H80000005 'stores computer configuration information
[HKEY_CURRENT_USER] = &H80000001 'stores program information for the current user.
[HKEY_LOCAL_MACHINE] = &H80000002 'stores program information for all users
[HKEY_USERS] = &H80000003 'has all the information for any user (not just the one provided by HKEY_CURRENT_USER)
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
            raise Exception("Unable to parse ...\n%s" % vb)
    return testMethod

#
# Add tests to main test class
for idx in range(len(tests)):
    setattr(ParsingTest, "test%d" % idx, getTestMethod(tests[idx]))


if __name__ == "__main__":
    unittest.main()
