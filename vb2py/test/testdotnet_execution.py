from testframework import *
import vb2py.utils
import vb2py.vbparser
import vb2py.parserclasses

in_vb_module_tests = []

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
    Class _MyClass
        Function B(x)
            Return 12 + x
        End Function
    End Class
    """, {
        'x': 22,
    },
    '''
    _a = _MyClass()
    x = _a.B(10)
    '''
))

# Properties
tests.append((
    """
Public Class _MyObject
    Dim _y = 0
    
    Public Property A As Integer
        Get
            Return _y
        End Get
        Set(Value as Integer)
            _y = Value
        End Set
    End Property
End Class  


    """, {
        'x': 0,
        'y': 1,
    },
    """
Set _a = _MyObject()
x = _a.A
_a.A = 1
y = _a.A   
    """
))


# Module
tests.append((
    """
    Module _MyClassName
        a = 1
    End Module
    """, {
        'x': 1,
    },
    '''
    _a = _MyClassName()
    x = _a.a
    '''
))

# Operators
in_vb_module_tests.extend([
    # IsNot
    ('a = 1 IsNot 2', {'a': True}),
    ('_x = 1\n_y = _x\na = _x IsNot _y', {'a': False}),

    # Assignment
    ('a = 1\na += 1', {'a': 2}),
    ('a = 1\na -= 1', {'a': 0}),
    ('a = 1\na *= 4', {'a': 4}),
    ('a = 11\na /= 2', {'a': 5}),
    ('a = 11\na \\= 2', {'a': 5}),
    ('a = 2\na ^= 3', {'a': 8}),
    ('a = 8\na <<= 2', {'a': 32}),
    ('a = 8\na >>= 2', {'a': 2}),
    ('a = 7\na &= 11', {'a': 3}),

])

import vb2py.vbparser
vb2py.vbparser.log.setLevel(0)
TestClass1 = addTestsTo(BasicTest, tests, dialect='vb.net')
TestClass2 = addTestsTo(BasicTest, in_vb_module_tests, dialect='vb.net', container=vb2py.parserclasses.VBModule)


if __name__ == "__main__":
    main()
