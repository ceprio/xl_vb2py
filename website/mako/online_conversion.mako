<%inherit file="components/base.mako"/>

<%block name="includes">
    <title>vb2py Online Conversion</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <link rel="stylesheet" type="text/css" href="main.css">

    <script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.3/ace.js"></script>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"
            integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1"
            crossorigin="anonymous"></script>
    <script type="text/javascript" src="split.js"></script>
    <link rel="stylesheet" type="text/css" href="split.css"/>
</%block>


<%block name="raw_content">
<!-- Buttons and Menus-->
<table border="0" cellspacing="0" width="100%">


    <!-- Main content and conversion buttons -->
    <tr>
        <td colspan="5">
            <div class="" id="conversion-box">
                <div>
                    <!-- Error and warning messages -->
                    <div>&nbsp;
                        <div id="error_message" class="hidden alert alert-danger" role="alert" style="display: none">
                            There was a parsing error in, or just after the highlighted line.
                            <input type="button" class="btn btn-success" value="Submit this code as a test file"
                                   onclick="submit_file();"/>
                            to help the project improve!<span class="version" id="version"></span>
                        </div>
                        <div id="dot_net_message" class="hidden alert alert-primary" role="alert" style="display: none">
                            Note that this code looks like VB.NET. There is only limited support for .NET code
                            currently.
                        </div>
                    </div>

                    <!-- Convert Buttons and Options -->
                    <div style="margin-top: 20px">

                        <!-- Conversion and other main buttons -->
                        <p align="center">
                            <input type="button" class="btn btn-primary" name="Do" value="Convert all code to Python"
                                   onclick="convert_code();">
                            &nbsp;&nbsp;
                            <input type="button" class="btn btn-secondary" name="Do"
                                   value="Just convert line / selection"
                                   onclick="convert_selection();">
                            &nbsp;&nbsp;
                            <input type="button" class="btn btn-secondary" name="Do" value="Show/Hide options ..."
                                   data-toggle="collapse" data-target="#options-panel" aria-expanded="false"
                                   aria-controls="collapseExample">
                            &nbsp;&nbsp;
                            <input type="button" class="btn btn-outline-dark" id="server-status" name="Server"
                                   value="Server Status" data-toggle="modal" data-target="#whats-new-dialog"
                                   value="Open">
                        </p>

                        <!-- Small options panel -->
                        <div id="options-panel" class="collapse" style="padding-right: 20px">
                            <div class="form-group row" align="center"> <!-- Context -->
                                <label class="col-sm-2 col-form-label">
                                    Dialect
                                </label>
                                <select class="form-control col-sm-2" id="dialect">
                                    <option selected value="detect">Auto detect</option>
                                    <option value="VB6">VB6</option>
                                    <option value="VB.NET">VB.NET</option>
                                    <option value="VBA">VBA (Excel)</option>
                                    <option value="VBScript">VB Script</option>
                                </select>

                                <label class="col-sm-2 col-form-label">
                                    Parsing Type
                                </label>
                                <select class="form-control col-sm-2" id="failure-mode">
                                    <option selected value="fail-safe">Fast</option>
                                    <option value="line-by-line">Fallback</option>
                                </select>

                                <label class="col-sm-2 col-form-label">
                                    Conversion Type
                                </label>
                                <select class="form-control col-sm-2" id="type">
                                    <option selected value="pythonic">Pythonic code</option>
                                    <option value="exact">Match VB exactly</option>
                                </select>

                                <label class="col-sm-2 col-form-label">
                                    Context
                                </label>
                                <select class="form-control col-sm-2" id="context">
                                    <option selected value="code">Code module</option>
                                    <option value="class">Class module</option>
                                    <option value="form">Form module</option>
                                </select>
                                <label class="col-sm-2 col-form-label">
                                    Class Name
                                </label>
                                <input class="col-sm-2" id="class-name" value="MyClass"/>

                                <label class="col-sm-2 col-form-label">
                                    Advanced Options
                                </label>
                                <button id="advanced-options-button" type="button" class="col-sm-2 btn btn-info"
                                        data-toggle="modal" data-target="#conversion-options" value="Open"
                                        onclick="recordOptionsOpen()">
                                    Open ...
                                </button>
                            </div>
                        </div>

                        <!-- Progress Indicator -->
                        <div class="progress" style="height: 20px;">
                            <div id="progress-indicator" class="progress-bar bg-success" role="progressbar" style="width: 100%;transition:none;display: block" aria-valuenow="0" aria-valuemin="100" aria-valuemax="100"></div>
                        </div>

                    </div>

                    <!-- Code boxes -->
                    <div class="vertically_divided code-box">
                        <div>
                            <div class="code-header">Type VB Code or
                                <!-- VB Code Panel buttons -->
                                <div class="btn-group" role="group" aria-label="Button group with nested dropdown">
                                    <!-- Paste button -->
                                    <span id="paste-fn" style="display: none">
                                        <button id="Paste" type="button"
                                                class="btn-small btn-secondary" onclick="pasteCode()">
                                            Paste
                                        </button>
                                          &nbsp;or&nbsp;
                                    </span>
                                    <!-- Load button -->
                                    <div class="btn-group" role="group">
                                        <button id="LoadGroup" type="button"
                                                class="btn-small btn-secondary dropdown-toggle" data-toggle="dropdown"
                                                aria-haspopup="true" aria-expanded="false">
                                            Load File
                                        </button>
                                        <div class="dropdown-menu" aria-labelledby="LoadGroup">
                                            <div>
                                                <input class="btn-small btn-success file-input" type='file'
                                                       onchange='openFile(event)'>
                                            </div>
                                        </div>
                                    </div>
                                    &nbsp;&nbsp;or&nbsp;&nbsp;
                                    <!-- Examples -->
                                    <div class="btn-group" role="group">
                                        <button id="ExampleGroup" type="button"
                                                class="btn-small btn-secondary dropdown-toggle" data-toggle="dropdown"
                                                aria-haspopup="true" aria-expanded="false">
                                            See example
                                        </button>
                                        <div class="dropdown-menu" aria-labelledby="ExampleGroup">
                                            <a class="dropdown-item" href="#" onclick="getExample('dim')">Dim</a>
                                            <a class="dropdown-item" href="#" onclick="getExample('if')">If</a>
                                            <a class="dropdown-item" href="#" onclick="getExample('with')">With</a>
                                            <a class="dropdown-item" href="#" onclick="getExample('select')">Select</a>
                                            <a class="dropdown-item" href="#" onclick="getExample('for')">For / For
                                                Each</a>
                                            <a class="dropdown-item" href="#" onclick="getExample('while')">While /
                                                Do</a>
                                            <a class="dropdown-item" href="#" onclick="getExample('using')">Using</a>
                                            <div class="dropdown-divider"></div>
                                            <a class="dropdown-item" href="#"
                                               onclick="getExample('sub')">Subroutines</a>
                                            <a class="dropdown-item" href="#" onclick="getExample('fn')">Functions</a>
                                            <a class="dropdown-item" href="#" onclick="getExample('class')">Classes</a>
                                            <a class="dropdown-item" href="#" onclick="getExample('properties')">Properties</a>
                                            <div class="dropdown-divider"></div>
                                            <a class="dropdown-item" href="#" onclick="getExample('type')">Types</a>
                                            <a class="dropdown-item" href="#" onclick="getExample('enum')">Enums</a>
                                            <a class="dropdown-item" href="#" onclick="getExample('open')">Open /
                                                Files</a>
                                        </div>
                                    </div>
                                    &nbsp;&nbsp;
                                    <div class="error-header">
                                        &nbsp;or&nbsp;
                                        <button id="VBErrorGroup" type="button"
                                                class="btn-small btn-secondary dropdown-toggle" data-toggle="dropdown"
                                                aria-haspopup="true" aria-expanded="false">
                                            Jump to error
                                        </button>
                                        <div id="vb-error-dropdown-menu" class="dropdown-menu"
                                             aria-labelledby="VBErrorGroup">
                                        </div>
                                    </div>

                                </div>
                            </div>
                            <!-- VB Editor -->
                            <div id="vbcode" class="vbcode">
                            </div>
                        </div>
                        <div>
                            <div class="code-header">Python Equivalent
                                <!-- Python Code Panel buttons -->
                                <div class="btn-group" role="group">
                                    <button id="PyCopyButton" type="button" onclick="copyPython()"
                                            class="btn-small btn-secondary">
                                        Copy
                                    </button>

                                    &nbsp;&nbsp;
                                    <div class="btn-group" role="group">
                                        <button id="PyButtonsGroup" type="button"
                                                class="btn-small btn-secondary dropdown-toggle" data-toggle="dropdown"
                                                aria-haspopup="true" aria-expanded="false">
                                            Download
                                        </button>
                                        <div class="dropdown-menu" aria-labelledby="PyButtonsGroup">
                                            <a class="dropdown-item" href="#" onclick="downloadPython()">Code (.py)</a>
                                            <a class="dropdown-item" href="#" onclick="downloadAll()">Code + Runtime (.zip)</a>
                                        </div>
                                    </div>
                                    &nbsp;&nbsp;
                                    <div class="error-header">
                                        &nbsp;or&nbsp;
                                        <button id="PyErrorGroup" type="button"
                                                class="btn-small btn-secondary dropdown-toggle" data-toggle="dropdown"
                                                aria-haspopup="true" aria-expanded="false">
                                            Jump to error
                                        </button>
                                        <div id="py-error-dropdown-menu" class="dropdown-menu"
                                             aria-labelledby="PyErrorGroup">
                                        </div>
                                    </div>

                                </div>
                            </div>
                            <!-- Python editor -->
                            <div id="pycode" class="pycode"></div>
                        </div>
                    </div>
                </div>
            </div>
        </td>
    </tr>
</table>

<!-- Pop-up options dialog -->
<div class="modal fade" id="conversion-options" tabindex="-1" role="dialog"
     aria-labelledby="advanced-options-button"
     aria-hidden="true">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLabel">Advanced Options</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body">
                <ul class="list-group list-group-flush">
                    <li class="list-group-item">
                        <div class="form-group row"> <!-- Advanced Options -->
                            <label class="col-sm-4 col-form-label">
                                Function returns
                            </label>
                            <select class="form-control col-sm-7" id="Cfg-Functions-JustUseReturnStatement">
                                <option selected value="No">Use temporary variable</option>
                                <option value="Yes">Use return statement only (.NET)</option>
                            </select>
                        </div>

                        <div class="form-group row">
                            <label class="col-sm-4 col-form-label">
                                Return variable
                            </label>
                            <select class="form-control col-sm-7" id="Cfg-Functions-PreInitializeReturnVariable">
                                <option selected value="Yes">Pre-initialise (safe)</option>
                                <option value="No">Do not initialise</option>
                            </select>
                        </div>

                        <div class="form-group row">
                            <label class="col-sm-4 col-form-label">
                                Variable name
                            </label>
                            <input type="text" class="form-control col-sm-7" id="Cfg-Functions-ReturnVariableName"
                                   value="fn_return_value">
                        </div>
                    </li>

                    <li class="list-group-item">
                        <div class="form-group row">
                            <label class="col-sm-4 col-form-label">
                                Literals
                            </label>
                            <select class="form-control col-sm-7" id="Cfg-Classes-ExplicitlyTypeLiterals">
                                <option value="No">Use Python literals</option>
                                <option selected value="Yes">Explicitly declare as objects</option>
                            </select>
                        </div>

                        <div class="form-group row">
                            <label class="col-sm-4 col-form-label">
                                Private Variables
                            </label>
                            <select class="form-control col-sm-7" id="Cfg-General-RespectPrivateStatus">
                                <option selected value="Yes">Respect VB scope</option>
                                <option value="No">Make all public</option>
                            </select>
                        </div>
                    </li>
                    <li class="list-group-item">

                        <div class="form-group row">
                            <label class="col-sm-4 col-form-label">
                                Select variable
                            </label>
                            <select class="form-control col-sm-7" id="Cfg-Select-EvaluateVariable">
                                <option selected value="Smart">Guess best approach</option>
                                <option value="Once">Create temp variable</option>
                                <option value="EachTime">Evaluate each time</option>
                            </select>
                        </div>

                        <div class="form-group row">
                            <label class="col-sm-4 col-form-label">
                                Select name
                            </label>
                            <select class="form-control col-sm-7" id="Cfg-Select-UseNumericIndex">
                                <option selected value="Yes">Make unique</option>
                                <option value="No">Reuse (fails if nested)</option>
                            </select>
                        </div>

                        <div class="form-group row">
                            <label class="col-sm-4 col-form-label">
                                Name prefix
                            </label>
                            <input type="text" class="form-control col-sm-7" id="Cfg-Select-SelectVariablePrefix"
                                   value="select_">
                        </div>
                    </li>
                    <li class="list-group-item">

                        <div class="form-group row">
                            <label class="col-sm-4 col-form-label">
                                With variable
                            </label>
                            <select class="form-control col-sm-7" id="Cfg-With-EvaluateVariable">
                                <option selected value="Once">Create temp variable</option>
                                <option value="EveryTime">Evaluate each time</option>
                            </select>
                        </div>

                        <div class="form-group row">
                            <label class="col-sm-4 col-form-label">
                                With name
                            </label>
                            <select class="form-control col-sm-7" id="Cfg-With-UseNumericIndex">
                                <option selected value="Yes">Make unique</option>
                                <option value="No">Reuse (fails if nested)</option>
                            </select>
                        </div>

                        <div class="form-group row">
                            <label class="col-sm-4 col-form-label">
                                Name prefix
                            </label>
                            <input type="text" class="form-control col-sm-7" id="Cfg-With-WithVariablePrefix"
                                   value="with_">
                        </div>
                    </li>

                </ul>

                <div class="modal-footer">
                    <button type="button" class="btn btn-danger" onclick="restoreDefaultConfig()">Defaults</button>
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-info" onclick="applyConfigChanges(false)">Save</button>
                    <button type="button" class="btn btn-primary" onclick="applyConfigChanges(true)">Save and Convert
                    </button>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Pop-up what's new dialog -->
<div class="modal fade" id="whats-new-dialog" tabindex="-1" role="dialog"
     aria-labelledby="advanced-options-button"
     aria-hidden="true">
    <div class="modal-dialog modal-lg modal-dialog-scrollable" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="whatsNewModalLabel">What's New</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body card-text" id="whats-new-content">
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
            </div>
        </div>
    </div>
</div>

<!-- Pop-up language error dialog -->
<div class="modal fade" id="language-error-dialog" tabindex="-1" role="dialog"
     aria-hidden="true">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="languageErrorModalLabel">Conversion Issue</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body" id="language-error-content">

            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
            </div>
        </div>
    </div>
</div>

<!-- Code samples -->
<div style="display: none">
    <div id="ex-general">
Dim A as Integer
B = 20

Sub DotIt(X as Double)
    Select Case A
        Case 1
            B = B + X
        Case 2
            B = B - X
        Case Else
            B = 0
    End Select
End Sub

Function GetHalfB() As Integer
    GetHalfB = B / 2
End Function
    </div>
    <div id="ex-if">

'
' Multi-line and singe-line ifs are converted to blocks in Python
If A = 10 Then
    DoSomething()
ElseIf B = 20 Then
    DoSomethingElse()
Else
    OtherCase()
If B = 20 Then C = 0 Else C = 1
End If
    </div>
    <div id="ex-with">

'
' With statements allow quick access to properties and methods
' of an object. These will be translated into explicit calls to
' a temporary object (in case of side-effects)
With Container.Member
    .Init
    .IncrementCounter 43
    With .ChildItem
        .Refresh
    End With
End With
    </div>
    <div id="ex-select">

'
' Selects are converted to If blocks with a temporary variable to
' hold the tested variables (in case of side-effects). Case ranges
' and options are handled as additional clauses for the if
Select Case A
    Case 1
        B = B + X
    Case 2
        B = B - X
        Select Case B
            Case 0 to 10
                C = 1
            Case 11, 12
                C = 2
        End Select
    Case Else
        B = 0
End Select
    </div>
    <div id="ex-for">

'
' Numeric for loops use a helper function to create the underlying
' sequence to be iterated over
For I = 1 To 10
    B = B + 1
    For J = 10 To 0 Step -1
        If B = 20 Then Exit For
    Next J
Next I

'
' For Each relies on the underlying object supporting the iteration
' protocol (which might not be the case!)
For Each Child in Parent
    Child.CleanUp
Next
    </div>
    <div id="ex-while">

'
' While and Do loops are converted to a Python while
' block.
While Something %3C%3E 10
    Something = Something + 1
Wend

'
' A starting until clause reverses the condition
Do Until Something = 5
    Something = Something - 1
Loop

'
' A final Until clause will generate an If with a break
Do
    Something = Something - 1
Loop Until Something = 0
    </div>
    <div id="ex-dim">
'
' Dim statements define the types of variables and perform initialisation
' and so are mapped to helper functions which create python objects that
' try to behave like the VB equivalents
Dim A
Dim B as Integer, C As String
A = 10: B = 30: C = "Hello World"

'
' Where arrays are defined these use a helper function which creates
' a variant of a list which has initial values
Dim D(10) As String, E(10, 2, 3) As MyClass

D(5) = "Hello"
E(1, 1, 2) = New MyClass(20)

'
' ReDim statements use the helper function to resize the underlying list
' objects while retaining the size
ReDim Preserve D(5)
ReDim C(20)

    </div>
    <div id="ex-sub">
'
' Subroutines are converted to Python functions and can
' include optional parameters with defaults
'
' An optional parameter with no default uses the helper
' object VBMissingArgument and the helper function IsMissing
Sub MySub(X, Optional Y, Optional Z=20)
    Dim subLocal
    If IsMissing(Y) Then Y = 12
    subLocal = X + Y + Z + moduleGlobal
End Sub

MySub 1, 2
MySub 1, Z:=10

'
' Passing by Value converts but behaves differently for
' immutable types in Python.
Sub DoIt(x, ByVal y)
    x = x + 1
    y = y + 1
End Sub

x = 0
y = 0
DoIt x, y
' x is now 1, y is still 0
    </div>
    <div id="ex-fn">
'
' Functions use a variable to store the result of the
' function during its execution
Function MyFunc(X, Optional Y, Optional Z=20)
    Dim subLocal
    subLocal = X + Y + Z
    MyFunc = subLocal*10
End Function

a = MyFunc(1, 2)
a = MyFunc(1, Z:=10)
    </div>
    <div id="ex-type">
'
' Types create classes with properties to store the
' values of the types
Type Point
    X As Single
    Y As Single
End Type
'
Type Line2D
    Start As Point
    Finish As Point
End Type
'
Dim p1 As Point, p2 As Point
p1.X = 10
p1.Y = 20
p2.X = 30
p3.Y = 40
'
Dim l1 As Line2D
l1.Start = p1
l1.Finish = p2

    </div>
    <div id="ex-enum">
'
' Enums create variables with the same names
Enum Number
    One = 1
    Two = 2
    Three = 3
    Four = 4
    Ten = 10
    Hundred = 100
End Enum

Enum Day
    Mon
    Tue
    Wed
    Thu
    Fri
End Enum
    </div>
    <div id="ex-properties" context="class">
'
' In class modules you can use properties to provide
' accessor functions. These are converted to the Python
' equivalent
Dim myValue = 0

Property Let PriceToPublic(Value As Integer)
    myValue = myValue - Value
    If myValue %3C 0 Then myValue = 0
End Property

Property Get PriceToPublic()
    PriceToPublic = 2 * myValue
End Property

    </div>
    <div id="ex-class" context="class">

'
' In the context of a class module, dimensioned variables
' are converted to attributes of the class and any
' subroutines and functions are converted to methods
' of the class.
Dim A as Integer
Dim B = 20

Sub DotIt(X as Double)
    Select Case A
        Case 1
            B = B + X
        Case 2
            B = B - X
        Case Else
            B = 0
    End Select
End Sub

Function GetHalfB() As Integer
    GetHalfB = B / 2
End Function
    </div>
    <div id="ex-open">
'
' File operations using #channels are mapped to a helper
' function that keeps track of the open files
Open "myfile.txt" For Input as #1
Line Input #1, aLine
Close #1

'
' This also handles the writing of files
Open "myOtherFile.txt" For Append as #2
Print #2, "Hello World"
Seek #2, 1
Print #2, "Here at the begining"
Close #2
    </div>
    <div id="ex-using">
'
' Using blocks are mapped to with blocks.
Using A As Object.Value
    b = A.Result()
End Using
    </div>
</div>

<!-- Main Scripts -->
<script>

    //region Globals Definitions
    var vbeditor = ace.edit("vbcode");
    vbeditor.setTheme("ace/theme/monokai");
    vbeditor.session.setMode("ace/mode/vbscript");
    var pyeditor = ace.edit("pycode");
    pyeditor.setTheme("ace/theme/monokai");
    pyeditor.session.setMode("ace/mode/python");
    var vb_marker = null;
    var py_marker = null;
    var unchanged_hash = hashFnv32a(vbeditor.getValue());
    let start_time = null;
    let whats_new_text = 'Unknown';


    var DEVELOPMENT = !location.host.startsWith('vb2py');
    var HOST;
    if (DEVELOPMENT) {
        HOST = 'http://localhost:8090';
    } else {
        //HOST = 'http://vb2py.dyndns.org:8090';
        HOST = 'http://23.99.213.204:8090';
    }

    let USE_STATUS_CHECK = false;

    let default_config = [];
    let status_checker = null;
    //endregion

    //region Document loaded functions
    $(document).ready(function () {
        // Remember initial config
        $('.form-control').each(function (idx, item) {
            if (item.id.startsWith('Cfg-')) {
                default_config.push([item.id, item.value]);
            }
        });
        loadConfigFromCookie();

        // Set the initial example
        getExample('initial');

        // Update the display of the server
        updateServerStatus();

        // Allow popover
        ##  $(function () {
        ##      $('[data-toggle="popover"]').popover()
        ##  });

        // Allow pasting in dev only
        if (DEVELOPMENT) {
            $('#paste-fn')[0].style = 'display: block';
        }
    });
    //endregion

    function recordOptionsOpen() {
        if (!DEVELOPMENT) {
            gtag('event', 'Options', {
                'event_category': 'Open Options',
            });
        }
    }

    //region Storing and reloading configuration
    function applyConfigChanges(also_convert_code) {
        $('.form-control').each(function (idx, item) {
            if (item.id.startsWith('Cfg-')) {
                setCookie(item.id.substr(4), item.value, 365);
            }
        });
        $('#conversion-options').modal('hide');
        if (also_convert_code) {
            convert_code();
        }
    }

    function restoreDefaultConfig() {
        default_config.forEach(function (item) {
            $('#' + item[0])[0].value = item[1];
        })
    }

    function loadConfigFromCookie() {
        $('.form-control').each(function (idx, item) {
            if (item.id.startsWith('Cfg-')) {
                let value = getCookie(item.id.substr(4));
                if (value !== "") {
                    item.value = value;
                }
            }
        })
    }

    function getConfigAsJSON() {
        let result = '';
        $('.form-control').each(function (idx, item) {
            if (item.id.startsWith('Cfg-')) {
                let value = getCookie(item.id.substr(4));
                if (value !== "") {
                    let name = item.id.split('-');
                    if (result !== '') {
                        result += ', ';
                    }
                    result += (
                        '["' + name[1] + '", ' +
                        '"' + name[2] + '", ' +
                        '"' + item.value + '"]'
                    );
                }
            }
        })
        return '[' + result + ']';
    }
    //endregion

    //region Cookie Handling
    function setCookie(cname, cvalue, exdays) {
        var d = new Date();
        d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
        var expires = "expires=" + d.toUTCString();
        document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
    }

    function getCookie(cname) {
        var name = cname + "=";
        var ca = document.cookie.split(';');
        for (var i = 0; i < ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) === ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) === 0) {
                return c.substring(name.length, c.length);
            }
        }
        return "";
    }
    //endregion

    function get_error_menu_item(name, line_vb, line_py) {
        let short_name = name;
        if (name.length > 25) {
            short_name = name.substring(0, 25) + ' ...';
        }
        let text = '<a class="dropdown-item" href="#" onclick="move_to(' + line_vb + ', ' + line_py + ')">' + short_name + '</a>';
        return text;
    }

    //region Status checking with the server
    function start_status_checker() {
        stop_status_checker();
        status_checker = setInterval(function () {
            let url = "/test";
            $.get(HOST + url, function (data) {
                pyeditor.session.setValue(pyeditor.session.getValue() + '.');
            });
        }, 1000);
    }

    function stop_status_checker() {
        if (status_checker != null) {
            clearInterval(status_checker);
            status_checker = null;
        }
    }

    function updateServerStatus() {
        let status_element = $('#server-status')[0];
        $.post(HOST + '/server_stats', function (data) {
            if (data.status === 'OK') {
                status_element.value = 'V' + data.version + ': Updated ' + data.date;
                $('#whats-new-content')[0].innerHTML = data['whats-new'];
            } else {
                status_element.value = 'Unable to reach'
            }
        }, 'json')
        .fail(function() {
            status_element.value = 'Server unavailable'
            status_element.classList.remove('btn-outline-dark');
            status_element.classList.add('btn-danger');
        })
        ;
    }
    //endregion

    function move_to(vb_line, py_line) {
        vbeditor.scrollToLine(vb_line);
        pyeditor.scrollToLine(py_line);
    }

    //region Conversion of code
    function convert_selection() {
        let range = vbeditor.selection.getRange();
        let selected_text = vbeditor.getSession().doc.getTextRange(range);
        //
        // If nothing was selected then just do the current line
        if (selected_text.length == 0) {
            range.start.column = 0;
            range.end.column = 1000;
            selected_text = vbeditor.getSession().doc.getTextRange(range);
        }
        convert_text(selected_text, range.start.row);
    }

    function convert_code() {
        let vbtext = vbeditor.getValue();
        convert_text(vbtext, 0);
    }

    function show_language_alert(type, error_kind) {
        $('#language-error-dialog').modal('show');
        let error_text = 'It looks like this might be <b>' +
            type + '</b> rather than VB text.';
        if (error_kind === 'type') {
            error_text = error_text + '<br><br>If loading or copying files please ensure ' +
               'to pick the actual source, class, or form definition files.';
        } else if (error_kind === 'language') {
            error_text = error_text + '<br><br>VB2PY can only convert VB type languages to Python.';
        }
        $('#language-error-content')[0].innerHTML = error_text;
        if (!DEVELOPMENT) {
            gtag('event', 'Caught Wrong File', {
                'event_category': 'UI',
                'event_label': error_kind,
            });
        }
    }

    function convert_text(vbtext, selection_offset) {
        show_start_conversion(vbtext);

        var context = $('#context')[0].value;
        var type = $('#type')[0].value;
        var class_name = $('#class-name')[0].value;
        var number_of_lines = vbtext.split(/\r\n|\r|\n/).length;

        var category;
        if (hashFnv32a(vbeditor.getValue()) == unchanged_hash) {
            category = "Demo";
        } else if (selection_offset == 0) {
            category = "All";
        } else {
            category = "Selection";
        }
        ;


        var language = 'Unset Language';

        var url;
        if (context == 'code') {
            url = '/single_code_module';
        } else if (context == 'class') {
            url = '/single_class_module';
        } else {
            url = '/single_form_module';
        }
        var conversion_style;
        if (type == 'exact') {
            conversion_style = 'vb';
        } else {
            conversion_style = 'pythonic';
        }

        // Clear old markers and errors
        if (vb_marker != null) {
            vbeditor.session.removeMarker(vb_marker);
        }
        if (py_marker != null) {
            pyeditor.session.removeMarker(py_marker);
        }
        $('#error_message')[0].style = 'display: none';
        $('#dot_net_message')[0].style = 'display: none';

        for (item in vbeditor.session.getMarkers(true)) {
            vbeditor.session.removeMarker(item)
        }
        for (item in pyeditor.session.getMarkers(true)) {
            pyeditor.session.removeMarker(item)
        }
        let failure_mode = $('#failure-mode')[0].value;
        let dialect = $('#dialect')[0].value;

        let config = getConfigAsJSON();

        if (USE_STATUS_CHECK) {
            start_status_checker();
        }
        ;

        if (!DEVELOPMENT && window.performance) {
            start_time = window.performance.now();
        }

        $.post(HOST + url, {
            'text': vbtext, 'style': conversion_style, 'class_name': class_name,
            'failure-mode': failure_mode, 'dialect': dialect, 'options': config
        }, function (data) {
            if (!DEVELOPMENT && window.performance) {
                let end_time = window.performance.now();
                let duration = end_time - start_time;
                let label = (data.parsing_failed ? "Parsing Failed" : "Succeeded");
                gtag('event', 'timing_complete', {
                    'name': 'Conversion',
                    'value': duration,
                    'event_category': category,
                    'event_label': label,
                })
            }
            if (USE_STATUS_CHECK) {
                stop_status_checker();
            }
            ;
            if (data.status === 'OK') {
                pyeditor.session.setValue(data.result);

                // Initialise the dropdown list of errors
                let vb_error_list = $('#vb-error-dropdown-menu')[0];
                let py_error_list = $('#py-error-dropdown-menu')[0];
                vb_error_list.innerHTML = '';
                py_error_list.innerHTML = '';

                // Watch for parsing failure
                if (data.parsing_failed) {
                    show_stop_conversion(false);
                    document.getElementsByClassName('error-header')[0].style.display = 'block';
                    document.getElementsByClassName('error-header')[1].style.display = 'block';

                    for (i = 0; i < data.parsing_stopped_vb.length; i++) {
                        let vb_offset = data.parsing_stopped_vb[i] + selection_offset;
                        let py_offset = data.parsing_stopped_py[i];
                        let Range = ace.require('ace/range').Range;
                        vb_marker = vbeditor.session.addMarker(new Range(vb_offset, 0, vb_offset, 100),
                            "errorMarker", "line", true);

                        vb_error_list.innerHTML += get_error_menu_item(
                            vbeditor.session.getLine(vb_offset),
                            vb_offset,
                            data.parsing_stopped_py[i]
                        );
                        py_error_list.innerHTML += get_error_menu_item(
                            pyeditor.session.getLine(py_offset),
                            vb_offset,
                            py_offset
                        );

                        py_marker = pyeditor.session.addMarker(new Range(data.parsing_stopped_py[i], 0, data.parsing_stopped_py[i], 100),
                            "errorMarker", "line", true);

                        if (i === 0) {
                            vbeditor.scrollToLine(vb_offset);
                            pyeditor.scrollToLine(data.parsing_stopped_py);
                        }
                    }

                    $('#error_message')[0].style['display'] = 'block';
                    if (data.language === 'VB.NET') {
                        $('#dot_net_message')[0].style['display'] = 'block';
                    } else if (data.language === 'VBP') {
                        show_language_alert('a VB Project File', 'type');
                    } else if (data.language === 'C#') {
                        show_language_alert('a C#, C++ or C File', 'language');
                    }
                    ;
                    language = data.language;

                } else {
                    show_stop_conversion(true);
                    document.getElementsByClassName('error-header')[0].style.display = 'none';
                    document.getElementsByClassName('error-header')[1].style.display = 'none';
                }
                if (!DEVELOPMENT) {
                    let label = (data.parsing_failed ? "Parsing Failed" : "Succeeded");
                    gtag('event', 'Convert', {
                        'event_category': category + '(' + data.language + ')',
                        'event_label': label,
                        'parameter1': data.language,
                        'value': number_of_lines
                    });
                }
            } else {
                show_stop_conversion(false);
                alert('Came back ' + data.status + ': ' + data.result);
                if (!DEVELOPMENT) {
                    gtag('event', 'Convert', {
                        'event_category': category,
                        'event_label': "Server Status Error: " + data.status + ", " + data.result,
                    });
                }
                ;
            }
            $('#version')[0].innerHTML = '(VB2PY version=' + data.version + ')';
        }, 'json')
            .fail(function (data, status, error) {
                show_stop_conversion(false);
                pyeditor.session.setValue('There was an error talking to the server\nStatus=' +
                    status + '\n' + 'Error=' + error);
                if (!DEVELOPMENT) {
                    gtag('event', 'Convert', {
                        'event_category': category,
                        'event_label': "Server AJAX Error - " + error + " - " + status + " = " +
                            vbtext.split('\n').length,
                    });
                };
                $.get(HOST + '/server_log?text=Ajax Failure');
            });
    }
    //endregion

    // region Copy and Paste
    function copyPython() {
        let sel = pyeditor.selection.toJSON();
        if (pyeditor.selection.isEmpty()) {
            pyeditor.selectAll();
        }
        pyeditor.focus();
        document.execCommand('copy');
        pyeditor.selection.fromJSON(sel);
        if (!DEVELOPMENT) {
            gtag('event', 'Copy Python', {
                'event_category': 'UI',
            });
        }
    }

    function pasteCode() {
        navigator.permissions.query({name: 'clipboard-read'}).then(result => {
            // If permission to read the clipboard is granted or if the user will
            // be prompted to allow it, we proceed.

            if (result.state === 'granted' || result.state === 'prompt') {
                navigator.clipboard.readText()
                    .then(text => {
                        let sel = vbeditor.selection.toJSON();
                        if (vbeditor.selection.isEmpty()) {
                            vbeditor.selectAll();
                        }
                        vbeditor.insert(text);
                        vbeditor.selection.fromJSON(sel);

                        if (!DEVELOPMENT) {
                            gtag('event', 'Paste VB', {
                                'event_category': 'UI',
                            });
                        }
                    })
                    .catch(err => {
                        console.error('Failed to read clipboard contents: ', err);
                    });
            } else {
                alert('Unable to paste from clipboard (probably browser security settings)');
            }
        });
    }
    // endregion

    function submit_file() {
        var vbtext = vbeditor.getValue();
        $.post(HOST + '/submit_file', {'text': vbtext}, function (data) {
        });
        alert('Thanks for submitting the file! This helps to make vb2py better.');
        if (!DEVELOPMENT) {
            gtag('event', 'Submit', {
                'event_category': 'UI',
            });
        }
        ;
    }

    var openFile = function (event) {
        var input = event.target;

        var reader = new FileReader();
        reader.onload = function () {
            var text = reader.result;
            vbeditor.session.setValue(text);
        };

        $('#dot_net_message')[0].style = 'display: none';

        if (input.files.length != 0) {
            reader.readAsText(input.files[0]);
            let extn = input.files[0].name.toLowerCase();
            let context = $('#context')[0];
            let class_name = $('#class-name')[0];
            let chosen_name = input.files[0].name.split('.')[0];
            chosen_name = chosen_name.replace(/ /g, "_");
            if (extn.endsWith('.frm')) {
                context.selectedIndex = 2;
                class_name.value = chosen_name;
            } else if (extn.endsWith('.cls')) {
                context.selectedIndex = 1;
                class_name.value = chosen_name;
            } else if (extn.endsWith('.vb')) {
                context.selectedIndex = 1;
                class_name.value = chosen_name;
                $('#dot_net_message')[0].style = '';
            } else {
                context.selectedIndex = 0;
            }
            if (!DEVELOPMENT) {
                gtag('event', 'Load', {
                    'event_category': 'File',
                    'event_label': extn.split(".")[1],
                });
            }
        }
    };

    function hashFnv32a(str, asString, seed) {
        /*jshint bitwise:false */
        var i, l,
            hval = (seed === undefined) ? 0x811c9dc5 : seed;

        for (i = 0, l = str.length; i < l; i++) {
            hval ^= str.charCodeAt(i);
            hval += (hval << 1) + (hval << 4) + (hval << 7) + (hval << 8) + (hval << 24);
        }
        if (asString) {
            // Convert to 8 digit hex string
            return ("0000000" + (hval >>> 0).toString(16)).substr(-8);
        }
        return hval >>> 0;
    }

    //region Download artifacts
    function downloadPython() {
        let element = document.createElement('a');
        let text = pyeditor.session.getValue();
        element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
        element.setAttribute('download', 'converted_code.py');

        element.style.display = 'none';
        document.body.appendChild(element);

        element.click();

        document.body.removeChild(element);

        if (!DEVELOPMENT) {
            gtag('event', 'Download Python', {
                'event_category': 'Converted Python',
            });
        }
    }

    function downloadAll() {
        let element = document.createElement('a');
        $.post(HOST + '/get_runtime_zip', {'code': pyeditor.session.getValue()}, function (data) {
            if (data.status === 'OK') {
                element.setAttribute('href', 'data:application/zip;base64,' + data.zipdata);
                element.setAttribute('download', 'converted_code.zip');

                element.style.display = 'none';
                document.body.appendChild(element);
                element.click();
                document.body.removeChild(element);

                if (!DEVELOPMENT) {
                    gtag('event', 'Download Python', {
                        'event_category': 'Converted Python + Runtime',
                    });
                }
            } else {
                alert('Failed to create ZIP');
            }
        }, 'json')
        .fail(function() {
            alert('Could not reach server');
        })
    }

    //endregion

    function getExample(name) {
        //
        // Get the text
        let e = null;
        if (name == 'initial') {
            e = $('#ex-general')[0];
        } else {
            e = $('#ex-' + name)[0];
        }
        vbeditor.session.setValue(unescape(e.innerHTML));
        //
        // Set the context
        let context = e.attributes['context'];
        if (context == null) {
            $('#context')[0].value = 'code';
        } else {
            $('#context')[0].value = context.textContent;
        }
        if (name !== 'initial') {
            convert_code();
            if (!DEVELOPMENT) {
                gtag('event', 'Example', {
                    'event_category': 'Example',
                    'event_label': name,
                });
            }
        }
    }

    //region Timing and Progress
    function estimateTime(text) {
        // Return an estimate of how long it will take to convert
        return 0.2 * 0.0189 * text.split('\n').length + 0.1;
    }

    function show_start_conversion(text) {
        pyeditor.session.setValue('# Converting code now ...');
        conversion_expected_duration = estimateTime(text);
        conversion_total_duration = 0.0;
        setTimeout(updateProgress, conversion_callback_interval);
        conversion_show_progress = true;
        conversion_bar.css('width', '0%');
        conversion_bar.removeClass('bg-warning');
        conversion_bar.removeClass('bg-success');
        conversion_bar.addClass('bg-info');
    }

    function show_stop_conversion(succeeded) {
        conversion_show_progress = false;
        conversion_bar.removeClass('bg-info');
        if (succeeded) {
            conversion_bar.addClass('bg-success');
        } else {
            conversion_bar.addClass('bg-warning');
        }
    }

    let conversion_expected_duration = 0.0;
    let conversion_total_duration = 0.0;
    let conversion_callback_interval = 100.0;
    let conversion_show_progress = true;
    let conversion_bar = $('.progress-bar');

    function updateProgress() {
        if (conversion_show_progress) {
            conversion_total_duration += conversion_callback_interval / 1000.0;
            let pc_done = conversion_total_duration / conversion_expected_duration * 100.0;
            if (pc_done > 90) {
                pc_done = 90;
            }
            $('.progress-bar').css('width', pc_done.toString() + '%').attr('aria-valuenow', pc_done.toString());
            setTimeout(updateProgress, conversion_callback_interval);
        } else {
            $('.progress-bar').css('width', '100%');
        }
    }
    //endregion

</script>
</%block>