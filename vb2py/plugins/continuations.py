try:
    import vb2py.extensions as extensions
except ImportError:
    import extensions

import re
commented_continuation = re.compile(r"(([^']*'[^']*')*[^']*'[^']*)(_)$")


class LineContinuations(extensions.SystemPlugin):
    """Plugin to handle line continuations

    Line continuations are indicated by a '_' at the end of a line and imply that
    the current line and the one following should be joined together. We could
    parse this out in the grammar but it is just easier to handle it as a pre-processor
    text as we aren't going to use it in the Python conversion.

    """

    order = 10 # We would like to happen quite early
    __is_plugin__ = 1

    def preProcessVBText(self, txt):
        """Convert continuation markers by joining adjacent lines"""

        txt_lines = txt.split("\n")
        stripped_lines = [lne.strip() for lne in txt_lines]
        # #
        # # Commented this out because it isn't clear how this is supposed
        # # to work. I have seen some code where the continuation marker
        # # continues the comment and others where the comment removes
        # # the continuation
        #
        # # Continuations should be ignored if they are on a comment line
        # for idx, line in enumerate(stripped_lines):
        #     if line.endswith('_') and commented_continuation.match(line):
        #         #
        #         # This is commented out, so remove the continuation marker
        #         stripped_lines[idx] = line[:-1]
        #
        txtout = "\n".join(stripped_lines)
        # txtout = txtout.replace(" _\n\n", " \n")
        # txtout = txtout.replace(" _\n.", " .")
        # txtout = txtout.replace(". _\n", ".")
        # txtout = txtout.replace(" _\n", " ")
        txtout += "\n\n"
        self.log.info("Line continuation:\nConverted '%s'\nTo '%s'" % (txt, txtout))
        #
        # Remove blanks
        # final = '\n'.join([lne.strip() for lne in txtout.splitlines() if lne]) + '\n\n'
        return txtout
