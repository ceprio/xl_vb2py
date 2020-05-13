"""Plug-in to implement directives"""

from vb2py import vbparser
import re
from vb2py import parserclasses

try:
    import vb2py.extensions as extensions
except ImportError:
    import extensions

class VBDirectives(extensions.SystemPlugin):
    """Convert directives (eg #If #Else #End If"""

    __enabled = 1

    directive_blocks = re.compile(
        r'(.*?)^#\s*If\s+(.*?)\sThen\s*$(.*?)^#End\s+If.*?$(.*)',
        re.DOTALL+re.M
    )
    warner = parserclasses.VBNamespace()

    def preProcessVBText(self, text):
        """Preprocess the text"""
        match = self.directive_blocks.match(text)
        path = int(vbparser.Config['Directives', 'Path'])
        while match:
            self.log.info('Matched directive: %s' % match.group(2))
            parts = re.split('#Else.*', match.group(3))
            message = "'" + self.warner.getWarning('CheckDirective', 'VB directive took path %s on %s\n' % (
                (path, match.group(2))))
            text = match.group(1) + message + parts[path - 1].lstrip() + match.group(4).lstrip()
            match = self.directive_blocks.match(text)

        return text