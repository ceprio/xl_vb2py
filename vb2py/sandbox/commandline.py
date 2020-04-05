"""A simple module intended to aid interactive testing of the parser

We just import a lot of useful things with short names so they are easy to type!

"""


import sys
sys.path.append('..')

from vb2py.vbparser import convertVBtoPython, parseVB as p, parseVBFile as f, getAST as t
import vb2py.vbparser
b = vb2py.vbparser.utils.bcolors

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


def pp(ast, text, indent=0):
    """Print out a pretified version of the ast"""
    if not ast:
        print
        return None
    cleaned_ast = []
    for entry in ast:
        if len(entry) == 1:
            print (' ' * indent),
            cleaned_ast.append((indent, pp(entry, text, indent + 1)))
        else:
            production, start, end, contents = entry
            print ' ' * indent + nice_text(text, production, start, end)
            cleaned_ast.append((indent, nice_text(text, production, start, end), pp(contents, text, indent + 1)))
    return cleaned_ast


def n(text, *args, **kw):
    ast = t(text, *args, **kw)
    pp(ast, text)
    print c(text, *args, **kw)


def nice_text(text, name, start, finish):
    subset = text[start:finish]
    conjoined = subset.replace('\n', ' $ ')
    return '%s [%s]' % (
        b.UNDERLINE + b.BOLD + name + b.ENDC,
        b.OKBLUE + conjoined + b.ENDC
    )


def safe():
    vb2py.vbparser.utils.BASE_GRAMMAR_SETTINGS['mode'] = 'safe'

def unsafe():
    vb2py.vbparser.utils.BASE_GRAMMAR_SETTINGS['mode'] = 'rigorous'


if __name__ == "__main__":
    def c(*args, **kw):
        print convertVBtoPython(*args, **kw)
