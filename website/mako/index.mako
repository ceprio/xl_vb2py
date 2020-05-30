<%inherit file="components/base.mako"/>

<%block name="content">

    <h6 style="padding-top: 50px">The <b>vb2Py</b> project is developing a suite of conversion tools to aid in
        translating Visual Basic projects into Python.</h6>

    <h7>The conversion includes,
        <ul>
            <li>VB code modules translating to Python code modules</li>
            <li>VB classes to Python classes</li>
        </ul>
    </h7>

    <div class="container" style="padding-top: 20px">
        <div class="row">
            <div class="col">
                <a href="online_conversion.html">
                    <div class="media">
                        <img src="gifs/translate.png" class="align-self-start mr-3" width="128px" height="128px">
                        <div class="media-body">
                            <h5 class="mt-0">Convert Now</h5>
                            Convert VB to Python in your browser
                        </div>
                    </div>
                </a>
            </div>
            <div class="col">
                <a href="documentation.html">
                    <div class="media">
                        <img src="gifs/learn.png" class="align-self-start mr-3" width="128px" height="128px">
                        <div class="media-body">
                            <h5 class="mt-0">Learn</h5>
                            Learn more about how the conversion works
                            and how VB code is translated.
                        </div>
                    </div>
                </a>
            </div>
            <div class="col">
                <a href="downloads.html">
                    <div class="media">
                        <img src="gifs/download.png" class="align-self-start mr-3" width="128px" height="128px">
                        <div class="media-body">
                            <h5 class="mt-0">Download</h5>
                            Download the source code to use from
                            your own computer.
                        </div>
                    </div>
                </a>
            </div>
        </div>
    </div>

    <h7 style="padding-top: 20px">
        The project is also aiming to support translation of VB Script,
        ASP and VBA code into Python equivalent code. See the <a href="roadmap.html">roadmap</a> for more details.<br><br>

        If you have experience in ASP and are interesting in <a href="contribute.html">contributing</a>,
        please get in <a href="mailto:paulpaterson@users.sourceforge.net">touch.</a>

    </h7>

    <div class="container" style="padding-top: 20px">
        <div class="row">
            <div class="col">
                <div class="card">
                  <div class="card-body">
                    <h5 class="card-title">Latest News</h5>
                      <ul class="list-group list-group-flush">
                          % for short, long in attributes['news'][:5]:
                                <li class="list-group-item">${short}</li>
                          % endfor
                      </ul>
                      <div class="card-body">
                        <a href="news.html" class="card-link"><i data-feather="edit"></i> Go to news</a>
                      </div>
                  </div>
                </div>
            </div>
            <div class="col">
                <div class="card">
                  <div class="card-body">
                    <h5 class="card-title">Latest Changes</h5>
                      <ul class="list-group list-group-flush">
                          % for short, long in attributes['changes'][:5]:
                                <li class="list-group-item">${short} (${len(long)} changes)</li>
                          % endfor
                      </ul>
                      <div class="card-body">
                        <a href="changes.html" class="card-link"><i data-feather="calendar"></i> Go to changes</a>
                      </div>

                  </div>
                </div>
            </div>
        </div>
    </div>
</%block>