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

tests.append("If IsMissing (oDoc) Then oDoc = ThisComponent")
tests.append('If NOT oDoc.SupportsService ("com.sun.star.sheet.SpreadsheetDocument") Then Exit Function')
tests.append('If (iSheet>= oSheets.getCount ()) Then Exit Function')
tests.append('oSheet = oSheets.getByIndex (iSheet)')
tests.append('arrayOfString () = Split (tmpString, ";")')
tests.append('If UBound (arrayOfString) <( 3 + iSheet) Then Exit Function')
tests.append('''
If InStr (tmpString, "+")> 0 Then
       arrayOfString () = Split (tmpString, "+")||
Else
 arrayOfString () = Split (tmpString, "/")||
End If

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
