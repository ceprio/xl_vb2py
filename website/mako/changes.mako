<%inherit file="components/base.mako"/>

<%block name="content">

    <div class="container" style="padding-top: 20px">
        <div class="row">
            <div class="col">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Latest changes</h5>
                              <ul class="list-group list-group-flush">
                                  % for short, items in attributes['changes']:
                                        <li class="list-group-item">
                                            <h4>${short}</h4>
                                            % for item in items:
                                                <p>&nbsp;-&nbsp;${item}</p>
                                            % endfor
                                        </li>
                                  % endfor
                              </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>

</%block>