from testframework import *
import vb2py.utils
import vb2py.vbparser


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


# Functions
tests.append((
    """
    a = _B(10)
    Function _B(x)
        Return 12 + x
    End Function
    """, {
        'a': 22,
    }
))


import vb2py.vbparser
vb2py.vbparser.log.setLevel(0)
TestClass = addTestsTo(BasicTest, tests, dialect='vb.net')

if __name__ == "__main__":
    main()
