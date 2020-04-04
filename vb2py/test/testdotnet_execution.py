from testframework import *
import vb2py.utils
import vb2py.vbparser

dot_net_grammar = vb2py.utils.loadGrammarFrom(
    vb2py.utils.relativePath('grammars', 'vbgrammar.mako'),
    data={
        'dialect': 'vb.net',
    }
)
vb2py.vbparser.declaration = dot_net_grammar


tests.append((
    'a = "hello".Length',
    {'a': 5},
))
tests.append((
    'a = ("hello").Length',
    {'a': 5},
))
tests.append((
    'a = ("hello" + "world").Length + 2',
    {'a': 12},
))

import vb2py.vbparser
vb2py.vbparser.log.setLevel(0) # Don't print all logging stuff
TestClass = addTestsTo(BasicTest, tests)

if __name__ == "__main__":
    main()
