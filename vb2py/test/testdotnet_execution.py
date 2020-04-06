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




import vb2py.vbparser
vb2py.vbparser.log.setLevel(0)
TestClass = addTestsTo(BasicTest, tests, dialect='vb.net')

if __name__ == "__main__":
    main()
