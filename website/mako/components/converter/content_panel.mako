<div data-options="region:'west',split:true" style="width:10%;" title="Details">
    <div class="btn-toolbar" role="toolbar" aria-label="VB Editor Toolbar" style="padding-bottom: 2px">
        <div class="btn-group btn-group-sm mr-2" role="group" aria-label="detail-buttons">
            <button type="button" class="btn btn-secondary">
                <i data-toggle="tooltip" title="Show the parsing issues" data-feather="alert-circle" height="20px"></i>
                <span class="button-label"> Errors</span>
            </button>

            <button type="button" class="btn btn-secondary">
                <i data-toggle="tooltip" title="Show the code structure" data-feather="layers" height="20px"></i>
                <span class="button-label"> Structure</span>
            </button>

        </div>
    </div>

    <div id="error-list">

    </div>
</div>


<script>

    function get_error_menu_item(line_text, line_vb, line_py) {
        let short_name = line_text;
        if (name.length > 25) {
            short_name = name.substring(0, 25) + ' ...';
        }
        let text = '<a href="#" onclick="move_to(' + line_vb + ', ' + line_py + ')"><br>' + short_name + '</a>';
        return text;
    }

    function move_to(vb_line, py_line) {
        vbeditor.scrollToLine(vb_line);
        pyeditor.scrollToLine(py_line);
    }

</script>