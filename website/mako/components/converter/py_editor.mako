<div data-options="region:'east',split:true" style="width:40%" title="Python Code Will Appear Here">
    <div class="btn-toolbar" role="toolbar" aria-label="VB Editor Toolbar" style="padding-bottom: 2px">
        <div class="btn-group btn-group-sm mr-2" role="group" aria-label="py-content-buttons">
            <button type="button" class="btn btn-secondary" onclick="recordOptionsOpen()"
                    data-toggle="modal" data-target="#conversion-options" value="Open">
                <i data-toggle="tooltip" title="Edit options to control the conversion" data-feather="settings" height="20px"></i><span class="button-label"> Options</span>
            </button>
        </div>

        <div class="btn-group btn-group-sm mr-2" role="group" aria-label="py-get">
            <button type="button" class="btn btn-secondary" onclick="copyPython()"
                    data-toggle="tooltip" title="Copy converted code to clipboard">
                <i data-feather="copy" height="20px"></i><span class="button-label"> Copy</span>
            </button>
            <button id="PyButtonsGroup" type="button"
                    class="btn-small btn-secondary dropdown-toggle" data-toggle="dropdown"
                    aria-haspopup="true" aria-expanded="false">
                <i data-feather="download" height="20px" data-toggle="tooltip" title="Download converted code"></i><span class="button-label"> Download</span>
            </button>
            <div class="dropdown-menu" aria-labelledby="PyButtonsGroup">
                <a class="dropdown-item" href="#" onclick="downloadPython()">Code (.py)</a>
                <a class="dropdown-item" href="#" onclick="downloadAll()">Code + Runtime (.zip)</a>
            </div>
        </div>

    </div>

    <div id="pycode" class="pycode">
    </div>
</div>

<script>

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
                .fail(function () {
                    alert('Could not reach server');
                })
    }

    //endregion

</script>