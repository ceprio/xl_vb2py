<%inherit file="components/base.mako"/>

<%block name="content">

    <div class="container" style="padding-top: 20px">
        <div class="row">
            <div class="col">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">News About the Project</h5>
                              <ul class="list-group list-group-flush">
                                  % for short, long in attributes['news']:
                                        <li class="list-group-item">
                                            <h4>${short}</h4>
                                            <p>${long}</p>
                                        </li>
                                  % endfor
                              </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>

</%block>