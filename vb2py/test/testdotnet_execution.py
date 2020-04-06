from testframework import *
import vb2py.utils
import vb2py.vbparser


tests.append((
    'a = "hello".Length',
    {'MyClass.a': 5},
))
tests.append((
    'a = ("hello").Length',
    {'MyClass.a': 5},
))
tests.append((
    'a = ("hello" + "world").Length + 2',
    {'MyClass.a': 12},
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


# Operators
tests.extend([
    # IsNot
    ('a = 1 IsNot 2', {'MyClass.a': True}),
    ('a = 1 IsNot 1', {'MyClass.a': False}),

    # Assignment
    ('a = 1\na += 1', {'MyClass.a': 2}),
    ('a = 1\na -= 1', {'MyClass.a': 0}),
    ('a = 1\na *= 4', {'MyClass.a': 4}),
    ('a = 1\na /= 2', {'MyClass.a': 0.5}),
    ('a = 11\na \\= 2', {'MyClass.a': 5}),
    ('a = 2\na ^= 3', {'MyClass.a': 8}),
    ('a = 8\na <<= 2', {'MyClass.a': 2}),
    ('a = 8\na >>= 2', {'MyClass.a': 32}),
    ('a = 7\na &= 11', {'MyClass.a': 3}),

])

import vb2py.vbparser
vb2py.vbparser.log.setLevel(0)
TestClass = addTestsTo(BasicTest, tests, dialect='vb.net')

if __name__ == "__main__":
    main()
