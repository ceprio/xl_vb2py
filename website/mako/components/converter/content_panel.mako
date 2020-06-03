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

    function create_tree_from_structure(structure) {
        html = '<ul id="tree" class="easyui-tree">' + get_tree_nodes(structure) + '</ul>';
        $('#error-list')[0].innerHTML = html;
        $('#tree').tree();
    }

    function get_tree_nodes(structure) {
        let html = '';
        structure.forEach(function (item, index) {
            let children_html = get_tree_nodes(item[4]);
            if (TREE_ITEMS.indexOf(item[1]) != -1) {
                html += '<li><span>' + item[1] + '</span><ul>' + children_html + '</ul></li>';
            } else {
                html += children_html;
            }
        });
        return html;
    }

    let TREE_ITEMS = [
            'sub_start_definition',
            'sub_end_definition',
            'fn_start_definition',
            'fn_end_definition',
            'assignment_statement',
            'select_start_statement',
            'case_item_block',
            'case_else_block',
            'select_end_statement',
            'dim_statement',
    ]
</script>