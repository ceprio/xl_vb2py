<div data-options="region:'center', split:true" style="width:50%" title="Enter VB Code Here">
    <div class="btn-toolbar" role="toolbar" aria-label="VB Editor Toolbar" style="padding-bottom: 2px">
        <div class="btn-group btn-group-sm mr-2" role="group" aria-label="vb-content-buttons">

            <button type="button" class="btn btn-secondary"
                    data-toggle="tooltip" title="Load a VB file from your computer">
                <i data-feather="folder" height="20px"></i><span class="button-label"> Load</span>
            </button>

            <button id="paste-button" type="button" class="btn btn-secondary"
                    data-toggle="tooltip" title="Paste from clipboard"
                    style="display: none" onclick="pasteCode()"
            >
                <i data-feather="clipboard" height="20px"></i><span class="button-label"> Paste</span>
            </button>

            <button id="ExampleGroup" type="button"
                    class="btn-small btn-secondary dropdown-toggle" data-toggle="dropdown"
                    aria-haspopup="true" aria-expanded="false">
                <i data-feather="file-text" height="20px" data-toggle="tooltip" title="Insert some example VB code"></i><span class="button-label"> Examples</span>
            </button>

            <div class="dropdown-menu" aria-labelledby="ExampleGroup">
                %for name, container, content in attributes['examples']:
                    %if name:
                        <a class="dropdown-item" href="#" onclick="getExample('${name}')">${name.capitalize()}</a>
                    %else:
                        <div class="dropdown-divider"></div>
                    %endif
                %endfor
            </div>

        </div>
        <div class="btn-group btn-group-sm mr-2" role="group" aria-label="vb-convert-buttons">
            <button type="button" class="btn btn-primary" onclick="convert_code('All')"
                    data-toggle="tooltip" title="Convert all the code to Python">
                <i data-feather="chevrons-right" height="20px"></i><span class="button-label"> Convert</span>
            </button>
            <button type="button" class="btn btn-secondary" onclick="convert_selection()"
                    data-toggle="tooltip" title="Convert current selection to Python">
                <i data-feather="chevron-right" height="20px"></i><span class="button-label"> Selection</span>
            </button>
        </div>
    </div>
    <div id="vbcode" class="vbcode">
        VBCode
    </div>

</div>

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


<script>
    $(document).ready(function () {
        navigator.permissions.query({name: 'clipboard-read'}).then(result => {
            $('#paste-button').show();
        });
    });

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
</script>