import xlwings as xw
import warnings


class CellClass:

    def __init__(self, cell=None):
        self.cell = cell  # cell must be an xlwings object

    def __repr__(self):
        return f"CellClass(Value={self.cell.value})"

    @property
    def Value(self):  # instance.Value == 0
        return self.cell.value

    @Value.setter
    def Value(self, x):
        self.cell.value = x

    def __add__(self, other):
        if isinstance(other, CellClass):
            other = other.Value
        return type(other)(self.cell.value) + other

    def __sub__(self, other):
        if isinstance(other, CellClass):
            other = other.Value
        return type(other)(self.cell.value) - other

    def __rsub__(self, other):
        """if isinstance(other, CellClass):
            other = other.Value"""
        return other - type(other)(self.cell.value)

    def __mul__(self, other):
        if isinstance(other, CellClass):
            other = other.Value
        return type(other)(self.cell.value) * other

    def __div__(self, other):
        if isinstance(other, CellClass):
            other = other.Value
        return type(other)(self.cell.value) / other

    def __rtruediv__(self, other):
        return other / type(other)(self.cell.value)

    def __lt__(self, other):
        if isinstance(other, CellClass):
            other = other.Value
        return type(other)(self.cell.value) < other

    def __le__(self, other):
        if isinstance(other, CellClass):
            other = other.Value
        return type(other)(self.cell.value) <= other

    def __gt__(self, other):
        if isinstance(other, CellClass):
            other = other.Value
        return type(other)(self.cell.value) > other

    def __ge__(self, other):
        if isinstance(other, CellClass):
            other = other.Value
        return type(other)(self.cell.value) >= other

    def __eq__(self, other):
        if isinstance(other, CellClass):
            other = other.Value

        if isinstance(other, str) and self.cell.value is None:
            return "" == other
        return type(other)(self.cell.value) == other

    def __ne__(self, other):
        if isinstance(other, CellClass):
            other = other.Value

        if isinstance(other, str) and self.cell.value is None:
            return "" != other
        return type(other)(self.cell.value) != other


class CellsClass:  # Do not keep OLE Objects as the structure will get destroyed

    def __init__(self, cells=None):
        assert isinstance(cells, xw.Range)
        self.cells = cells  # Must be an XLWings object

    @property
    def Column(self):
        return self.cells.column + 1

    @property
    def Row(self):
        return self.cells.row + 1

    def Range(self, range):
        """ Use cases:
        Rng.Range('a4:b18')
        Rng.Range('a4')
        """
        new_range = self.cells.sheet.range(self.cells.api.Range(range).Address)
        cell_count = new_range.count
        # Convert to a single cell class if only one cell
        if cell_count == 1:
            return CellClass(new_range)
        else:
            return CellsClass(new_range)

    @property
    def Rows(self):
        return RowsClass(self.cells)

    def __getitem__(self, keys):  # worksheet[key1,key2]
        """ Use cases:
        sheet.Cells[g.Qtable, g.VceTable] -> returns a CellClass (single cell)
        r(1,1)
        variable0.Cells[g.GdataStart - 1, 1].Value = 'Step'
        """
        assert self.cells != None, "Cells cannot be None"
        range = self.cells(*keys)
        cell_count = range.count
        if cell_count == 1:
            return CellClass(range)
        else:
            return CellsClass(range)

    def __setitem__(self, keys, value):
        """ Use cases:
        sheet.cells[100, 1] = cnt + 1
        """
        if isinstance(value, CellClass):
            value = value.cell.value
        self.cells(*keys).value = value

    def __call__(self, *keys):  # worksheet(key1,key2)
        """ Use case:
        sheet.Cells(22, 4)
        """
        ret = self.__getitem__(keys)
        return ret


class RowsClass(CellsClass):

    @property
    def Count(self):
        return str(self.cells.api.Rows.Count)


class SheetClass:

    def __init__(self, sheet):
        self.sheet = sheet

    def Range(self, range1, range2=None):
        """
        Use cases:
            Worksheets('Dev').Range('N27')
            Worksheets('Dev').Range(CellClass1,CellClass2)  # Should return a range over the two 
        """
        if range2 is None:
            value = self.sheet.range(range1).value
            if isinstance(value, list):
                for n in range(len(value)):
                    if value[n] == None:
                        value[n] = 0  # To do:Value 0 needs revision
            return value
        else:
            return CellsClass(self.sheet.range(range1.cell, range2.cell))

    def Rows(self, range):
        return self.sheet.api.Range(range)

    def __getattr__(self, name):  # sheet.name1
        if name == 'Cells':
            return CellsClass(self.sheet.cells)
        a = getattr(self.sheet, name, None)
        if a is None:
            return self.sheet.shapes(name).api.OLEFormat.Object.Object
        return a

    def __getitem__(self, key):  # sheet['name1']
        sh = xw.Book.caller().sheets[key]
        return SheetClass(sh)


class ChartsClass:

    def __init__(self, charts):
        self.charts = charts

    def __getitem__(self, key):
        return self.charts[key - 1].api[0]


class WorksheetsClass:

    def __init__(self, sheets=None):
            assert sheets is None or isinstance(sheets, xw.main.Sheets), "WorksheetsClass parameter must be of type xlwings.main.Sheets"
            self.sheets = sheets  # type <class 'xlwings.main.Sheets'>

    def __getitem__(self, key):
        if self.sheets is None:
            self.sheets = xw.Book.caller().sheets
        sh = None
        for sheet in self.sheets:
            if sheet.name == key:
                sh = sheet
                break
        if sh == None:
            raise IndexError(f"key '{key}' not found")
        return SheetClass(sh)

    def __call__(self, key):
        """ Use case:
        worksheet(key)
        """
        sh = xw.Book.caller().sheets[key]
        return SheetClass(sh)


class ActiveSheetClass:
    ""

    def __getattr__(self, name):
        if name == 'ChartObjects':
            obj = ChartsClass(xw.Book.caller().sheets.active.charts)
        else:
            obj = xw.Book.caller().sheets.active.api.__getattr__(name)
        return obj


class ThisWorkbookClass:

    def __getattr__(self, name):
        if name == 'Worksheets':
            return WorksheetsClass(xw.Book.caller().sheets)
        else:
            obj = xw.Book.caller().sheets.active.api.__getattr__(name)
        return obj


class ApplicationClass:

    def __getattr__(self, name):
        if name == "WorksheetFunction":
            return WorksheetFunctionClass()
        obj = xw.Book.caller().app.api.__getattr__(name)
        return obj


class WorksheetFunctionClass:

    def __getattr__(self, name):
        return FunctionClass(name)


class FunctionClass:

    def __init__(self, function_name):
        self.function_name = function_name

    def __call__(self, *args):
        """ Overload of all functions found under WorksheetFunction:
        This is needed to convert arguments types used as arguments.
        """
        new_args = []
        for arg in args:
            if isinstance(arg, CellClass):
                new_args.append(arg.cell.api)  # Convert to OLE object
            elif isinstance(arg, CellsClass):
                new_args.append(arg.cells.api)  # Convert to OLE object
            else:
                new_args.append(arg)

        func = xw.Book.caller().app.api.WorksheetFunction.__getattr__(self.function_name)
        return func(*new_args)


ActiveSheet = ActiveSheetClass()
Worksheets = WorksheetsClass()
ThisWorkbook = ThisWorkbookClass()
Application = ApplicationClass()
WorksheetFunction = WorksheetFunctionClass()
vbCrLf = '\n'


class StaticTyped:
    "Will make sure assignments are casted to their original static type"

    def __setattr__(self, name, value):  # inst.name1 = value
        if name in type(self).__dict__:
            t = type(type(self).__dict__[name])
            self.__dict__.__setitem__(name, t(value))
        else:
            self.__dict__.__setitem__(name, value)


class Range():
    "Mock up definition of a range"
