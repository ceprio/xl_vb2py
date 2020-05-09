import vb2py
import os
import vb2py.converter

event_translator = {
        "Click" : "mouseClick",
}

possible_controls = {}


class Resource(vb2py.converter.BaseResource):
    """Represents a resource object"""

    target_name = "Console"

    def __init__(self, *args, **kw):
        """Initialize the vb2py.PythonCard resource"""
        vb2py.converter.BaseResource.__init__(self, *args, **kw)
        self._rsc = eval(open("%s.txt" % self.basesourcefile, "r").read())
        self._rsc["controls"] = []
        self._code = open("%s.py" % self.basesourcefile, "r").read()

    def writeToFile(self, basedir, write_code=0):
        """Write ourselves out to a directory"""
        fle = open(os.path.join(basedir, self.name) + ".py", "w")
        lines = []
        if write_code:
            #
            # Assemble our code
            for block in self.subs + self.fns:
                lines.append('    def %s(self, %s):\n        """Sub"""' % (block.name, block.args))
                for code_line in block.code.splitlines():
                    lines.append("        %s" % code_line)
                lines.append("")

            added_code = "\n".join(lines)
        else:
            added_code = ""

        fle.write(self._code.replace("# CODE_GOES_HERE", added_code))
        fle.close()


class VBUnknownControl:
    """Dummy to hold control properties"""

