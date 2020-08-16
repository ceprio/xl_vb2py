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
vb_dot_net_tests = []

# Explicit Bare calls with arguments
tests.extend([

])


# Try statements
vb_dot_net_tests.append('''
Try
    a = 1
Catch
    a = 2
End Try
''')

vb_dot_net_tests.append('''
Try
    a = 1
Catch ValueError
    a = 2
End Try
''')

vb_dot_net_tests.append('''
Try
    a = 1
Catch ValueError.ThisError
    a = 2
End Try
''')

vb_dot_net_tests.append('''
Try
    a = 1
Catch ValueError.ThisError As Err
    a = 2
End Try
''')

vb_dot_net_tests.append('''
Try
    a = 1
Catch ValueError.ThisError As Err When B = 2
    a = 2
End Try
''')

vb_dot_net_tests.append('''
Try
    a = 1
Catch ValueError.ThisError As Err When B = 2
    a = 2
    Exit Try
    b = 2
End Try
''')

vb_dot_net_tests.append('''
Try
    a = 1
Catch ValueError.ThisError As Err When B = 2
    a = 2
    Exit Try
    b = 2
Catch OtherError
    b = 3
End Try
''')

vb_dot_net_tests.append('''
Try
    a = 1
Catch ValueError.ThisError As Err When B = 2
    a = 2
    Exit Try
    b = 2
Catch OtherError
    b = 3
Finally
    b = 4
End Try
''')

vb_dot_net_tests.append('''
Try
Catch ValueError.ThisError As Err When B = 2
Catch OtherError
Finally
End Try
''')

vb_dot_net_tests.append('''
Try
    a = 1
Catch    ValueError.ThisError   As    Err    When   B = 2  
    a = 2
    Exit    Try  
    b = 2
Catch    OtherError   
    b = 3
Finally
    b = 4
End     Try
''')

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
