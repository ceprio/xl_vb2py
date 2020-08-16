from vb2py.test.testframework import *
import vb2py.utils
import vb2py.vbparser
import vb2py.parserclasses
import sys

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
    ('a = 11\na /= 2', {'a': 5.5}),
    ('a = 11\na \\= 2', {'a': 5}),
    ('a = 2\na ^= 3', {'a': 8}),
    ('a = 8\na <<= 2', {'a': 32}),
    ('a = 8\na >>= 2', {'a': 2}),
    ('a = 7\na &= 11', {'a': 3}),

])


class TestModule:
    path = 1

sys.modules['TestModule'] = TestModule


# Imports
tests.extend([
    ('Imports TestModule\nClass _MyClassName\na = path\nEnd Class\n',
     {'b': 1, 'path': 1},
     '_a = _MyClassName()\nb = _a.a\n',
     ),
    ('Imports b = TestModule\nClass _MyClassName\na = b.path\nEnd Class\n',
     {'b': 1},
     '_a = _MyClassName()\nb = _a.a\n',
     ),
])

in_vb_module_tests.extend([
    (
        '''
        B = 0
        For A = 1 To 10
        B = B + A
        Next
        ''',
        {'A': 10, 'B': 55}
    ),
    (
        '''
        B = 0
        For A As Integer = 1 To 10
        B = B + A
        Next
        ''',
        {'A': 10, 'B': 55}
    )
])



# Try statements

# Bare catch
in_vb_module_tests.append(('''
Try
    a = 1
Catch
    a = 2
End Try
''', {
    'a': 1,
}))

in_vb_module_tests.append(('''
Try
    a = 1 / 0
Catch
    a = 2
End Try
''', {
    'a': 2,
}))



# Named exception type
in_vb_module_tests.append(('''
Try
    a = 1
Catch ZeroDivisionError
    a = 2
End Try
''', {
    'a': 1
}))
in_vb_module_tests.append(('''
Try
    a = 1 / 0
Catch ZeroDivisionError
    a = 2
End Try
''', {
    'a': 2
}))
in_vb_module_tests.append(('''
Try
    a = 1 / 0
Catch IndexError
    a = 2
Catch
    a = 3
End Try
''', {
    'a': 3
}))
in_vb_module_tests.append(('''
Try
    a = 1 / 0
Catch IndexError
    a = 2
Catch ZeroDivisionError
    a = 3
Catch
    a = 4
End Try
''', {
    'a': 3
}))

# Collect the exception in a variable
in_vb_module_tests.append(('''
Try
    a = 1
Catch ZeroDivisionError As Err
    a = 2
End Try
''', {
    'a': 1
}))
in_vb_module_tests.append(('''
Try
    a = 1 / 0
Catch ZeroDivisionError As _Err
    a = 2
    b = str(_Err)
End Try
''', {
    'a': 2, 'b': "division by zero"
}))
in_vb_module_tests.append(('''
Try
    a = 1 / 0
Catch ZeroDivisionError As _Err
    a = 2
    Exit Try
    b = str(_Err)
End Try
''', {
    'a': 2,
}))


# Conditional catching
in_vb_module_tests.append(('''
b = 1
Try
    a = 1
Catch ZeroDivisionError As Err When b = 1
    a = 2
Catch
    a = 3
End Try
''', {
    'a': 1, 'b': 1,
}))
in_vb_module_tests.append(('''
b = 1
Try
    a = 1 / 0
Catch ZeroDivisionError As Err When b = 1
    a = 2
Catch
    a = 3
End Try
''', {
    'a': 2, 'b': 1,
}))
in_vb_module_tests.append(('''
b = 1
Try
    Try
        a = 1 / 0
    Catch ZeroDivisionError As Err When b = 2
        a = 2
    Catch
        a = 3
    End Try
Catch ZeroDivisionError
    a = 4
End Try
''', {
    'a': 4, 'b': 1,
}))


# Finally
in_vb_module_tests.append(('''
b = 1
Try
    a = 1
Finally
    b = 2
End Try
''', {
    'a': 1, 'b': 2
}))
in_vb_module_tests.append(('''
b = 1
Try
    a = 1
Catch
    a = 2
Finally
    b = 2
End Try
''', {
    'a': 1, 'b': 2
}))
in_vb_module_tests.append(('''
b = 1
Try
    a = 1 / 0
Catch
    a = 2
Finally
    b = 2
End Try
''', {
    'a': 2, 'b': 2
}))
in_vb_module_tests.append(('''
b = 1
Try
    a = 1 / 0
Catch
    a = 2
    Exit Try
    a = 3
Finally
    b = 2
End Try
''', {
    'a': 2, 'b': 2
}))


# Array initialization
in_vb_module_tests.append(('''
    Dim _A As String() = New String() {"1", "2", "3"}
    a = _A(0)
    b = _A(1)
    c = _A(2)
''', {
    'a': '1', 'b': '2', 'c': '3',
}))

in_vb_module_tests.append(('''
    Function _ReturnIt(Array, Index)
        Return Array(Index)
    End Function
    a = _ReturnIt(New String() {"1", "2", "3"}, 0)
    b = _ReturnIt(New String() {"1", "2", "3"}, 1)
    c = _ReturnIt(New String() {"1", "2", "3"}, 2)
''', {
    'a': '1', 'b': '2', 'c': '3',
}))

import vb2py.vbparser
vb2py.vbparser.log.setLevel(0)
TestClass1 = addTestsTo(BasicTest, tests, dialect='vb.net')
TestClass2 = addTestsTo(BasicTest, in_vb_module_tests, dialect='vb.net', container=vb2py.parserclasses.VBModule)


if __name__ == "__main__":
    main()
