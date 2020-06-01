<%inherit file="components/base.mako"/>

<%block name="includes">
    <title>vb2py Online Conversion</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <link rel="stylesheet" type="text/css" href="main.css">

    <!-- Jquery -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.3/ace.js"></script>

    <!-- East UI -->
    <script src="jquery-easyui-1.9.4/jquery.easyui.min.js"></script>
    <link rel="stylesheet" type="text/css" href="jquery-easyui-1.9.4/themes/gray/easyui.css">
    <link rel="stylesheet" type="text/css" href="jquery-easyui-1.9.4/themes/icon.css">

    <!-- ACE -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.3/ace.js"></script>
</%block>


<%block name="raw_content">

<div style="margin:20px 0 10px 0;"></div>

<div class="easyui-panel" style="width:100%;height:90%;padding:10px;">
    <div class="easyui-layout" data-options="fit:true">
        <%include file="components/converter/content_panel.mako"/>
        <%include file="components/converter/vb_editor.mako"/>
        <%include file="components/converter/py_editor.mako"/>
    </div>
</div>

<%include file="components/converter/examples.mako"/>

<script>
    var DEVELOPMENT = !location.host.startsWith('vb2py');
    var HOST;
    if (DEVELOPMENT) {
        HOST = 'http://localhost:8090';
    } else {
        //HOST = 'http://vb2py.dyndns.org:8090';
        HOST = 'http://23.99.213.204:8090';
    }

    let pyeditor = null;
    let vbeditor = null;

    $(document).ready(function () {
        vbeditor = ace.edit("vbcode");
        vbeditor.setTheme("ace/theme/dawn");
        vbeditor.session.setMode("ace/mode/vbscript");
        pyeditor = ace.edit("pycode");
        pyeditor.setTheme("ace/theme/dawn");
        pyeditor.session.setMode("ace/mode/python");

        // Set the initial example
        getExample('initial');

        // Enable tooltips
        $(function () {
          $('[data-toggle="tooltip"]').tooltip()
        })

        // Hide button labels
        $('.button-label').hide();

        // Enable toasts
        $('.toast').toast({'autohide': false});
    });


</script>

<%include file="components/converter/conversion.mako"/>
<%include file="components/converter/config.mako"/>
<%include file="components/converter/progress.mako"/>

</%block>

