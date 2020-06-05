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

    function get_content_menu_item(line_text, line_vb, line_py) {
        let short_name = line_text;
        if (name.length > 25) {
            short_name = name.substring(0, 25) + ' ...';
        }
        let text = '<a href="#" onclick="move_to(' + line_vb + ', ' + line_py + ')">' + short_name + '</a>';
        return text;
    }

    function move_to(vb_line, py_line) {
        vbeditor.scrollToLine(vb_line);
        vbeditor.selection.clearSelection();
        vbeditor.moveCursorToPosition({row: vb_line, col: 0});
        vbeditor.selection.selectLine();

        pyeditor.scrollToLine(py_line);
    }

    function create_tree_from_structure(structure, vb_error_lines, py_error_lines, selection_offset) {
        html = '<ul id="tree" class="easyui-tree">';
        if (vb_error_lines !== null) {
            html += '<li><span>Parsing Issues</span><ul>' +
                    get_error_nodes(vb_error_lines, py_error_lines, selection_offset) +
                    '</ul></li>';
        };
        if (structure.length !== 0) {
            html += '<li><span>Structure</span><ul>' +
                    get_tree_nodes(structure) +
                    '</ul></li>';
        };
        html += '</ul>';
        $('#error-list')[0].innerHTML = html;
        $('#tree').tree();
    }

    function get_tree_nodes(structure) {
        let html = '';
        structure.forEach(function (item, index) {
            let children_html = get_tree_nodes(item[5]);
            html += '<li><span>' +
                    get_content_menu_item(
                        item[2],
                        item[0],
                        -1
                    ) +
                    '</span><ul>' +
                    children_html +
                    '</ul></li>';
        });
        return html;
    }

    function get_error_nodes(vb_error_lines, py_error_lines, selection_offset) {
        let html = '';
        if (vb_error_lines) {
            for (let i = 0; i < vb_error_lines.length; i++) {
                let vb_offset = vb_error_lines[i] + selection_offset;
                let py_offset = py_error_lines[i];
                html += '<li data-options="iconCls:\'icon-cancel\'"><span>' +
                        get_content_menu_item(
                                vbeditor.session.getLine(vb_offset),
                                vb_offset,
                                py_offset
                        ) +
                        '</span><ul></ul></li>'
            }
        }
        return html;
    }

</script>