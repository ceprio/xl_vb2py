"""A simple module intended to aid interactive testing of the parser

We just import a lot of useful things with short names so they are easy to type!

"""


import sys
sys.path.append('..')

from vb2py.vbparser import convertVBtoPython, parseVB as p, parseVBFile as f, getAST as t
import vb2py.vbparser

try:
    from win32clipboard import *
    import win32con

    def getClipBoardText():
        """Get text from the clipboard"""
        OpenClipboard()
        try:
            got = GetClipboardData(win32con.CF_UNICODETEXT)
        finally:
            CloseClipboard()
        return str(got)
    v = getClipBoardText
except ImportError:
    print "Clipboard copy not working!"


def pp(ast):
    """Print out a pretified version of the ast"""
    if not ast:
        return None
    cleaned_ast = []
    for entry in ast:
        if len(entry) == 1:
            cleaned_ast.append(pp(entry))
        else:
            production, start, end, contents = entry
            cleaned_ast.append((production, pp(contents)))
    return cleaned_ast


if __name__ == "__main__":
    def c(*args, **kw):
        print convertVBtoPython(*args, **kw)
