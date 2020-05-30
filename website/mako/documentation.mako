<%inherit file="components/base.mako"/>

<%block name="content">

    <div class="media documentation-media">
        <div class="media-body">
            <h5 class="mt-0">Please use the following links to learn more about the project.<br><br></h5>

            <ul class="list-group">
                <li class="list-group-item">
                    <i data-feather="help-circle"></i>&nbsp;
                    Instructions on how to use vb2Py are in the <a href="/docs/index.html">User
                    Guide.</a>
                </li>

                <li class="list-group-item">
                    <i data-feather="help-circle"></i>&nbsp;
                    The <a href="/docs/reference.html">Reference Manual</a> gives details
                    on how each of the VB code structures is represented in Python.
                </li>

                <li class="list-group-item">
                    <i data-feather="map"></i>&nbsp;
                    The project has a <a href="roadmap.html">roadmap.</a></li>

                <li class="list-group-item">
                    <i data-feather="file-text"></i>&nbsp;
                    For parsing VB we use the <a href="http://simpleparse.sourceforge.net">SimpleParse</a> package.</li>

                <li class="list-group-item">
                    <i data-feather="smile"></i>&nbsp;
                    A full list of <a href="credits.html">credits</a> is available here.</li>
            </ul>
        </div>
    </div>
</%block>