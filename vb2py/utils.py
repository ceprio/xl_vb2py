import os
import mako.template
import mako.lookup

BASE_GRAMMAR_SETTINGS = {
    'dialect': 'VB6',
    'mode': 'rigorous',
}

def rootPath():
    """Return the root path"""
    return os.path.split(os.path.abspath(__file__))[0]


def relativePath(*paths):
    """Return the path to a file"""
    return os.path.join(rootPath(), *paths)


def loadGrammarFrom(filename, data=None):
    """Return the text of a grammar file loaded from the disk"""
    text = open(filename, 'r').read()
    lookup = mako.lookup.TemplateLookup(directories=[relativePath('grammars')])
    template = mako.template.Template(text, lookup=lookup)
    #
    base_data = {}
    base_data.update(BASE_GRAMMAR_SETTINGS)
    #
    if data:
        base_data.update(data)
    #
    return str(template.render(**base_data))

