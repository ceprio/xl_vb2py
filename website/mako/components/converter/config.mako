
<!-- Pop-up options dialog -->
<div class="modal fade" id="conversion-options" tabindex="-1" role="dialog"
     aria-labelledby="advanced-options-button"
     aria-hidden="true">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLabel">Advanced Options</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body">
                <ul class="list-group list-group-flush">
                    <li class="list-group-item">
                        <div class="form-group row"> <!-- Advanced Options -->
                            <label class="col-sm-4 col-form-label">
                                Function returns
                            </label>
                            <select class="form-control col-sm-7" id="Cfg-Functions-JustUseReturnStatement">
                                <option selected value="No">Use temporary variable</option>
                                <option value="Yes">Use return statement only (.NET)</option>
                            </select>
                        </div>

                        <div class="form-group row">
                            <label class="col-sm-4 col-form-label">
                                Return variable
                            </label>
                            <select class="form-control col-sm-7" id="Cfg-Functions-PreInitializeReturnVariable">
                                <option selected value="Yes">Pre-initialise (safe)</option>
                                <option value="No">Do not initialise</option>
                            </select>
                        </div>

                        <div class="form-group row">
                            <label class="col-sm-4 col-form-label">
                                Variable name
                            </label>
                            <input type="text" class="form-control col-sm-7" id="Cfg-Functions-ReturnVariableName"
                                   value="fn_return_value">
                        </div>
                    </li>

                    <li class="list-group-item">
                        <div class="form-group row">
                            <label class="col-sm-4 col-form-label">
                                Literals
                            </label>
                            <select class="form-control col-sm-7" id="Cfg-Classes-ExplicitlyTypeLiterals">
                                <option value="No">Use Python literals</option>
                                <option selected value="Yes">Explicitly declare as objects</option>
                            </select>
                        </div>

                        <div class="form-group row">
                            <label class="col-sm-4 col-form-label">
                                Private Variables
                            </label>
                            <select class="form-control col-sm-7" id="Cfg-General-RespectPrivateStatus">
                                <option selected value="Yes">Respect VB scope</option>
                                <option value="No">Make all public</option>
                            </select>
                        </div>
                    </li>
                    <li class="list-group-item">

                        <div class="form-group row">
                            <label class="col-sm-4 col-form-label">
                                Select variable
                            </label>
                            <select class="form-control col-sm-7" id="Cfg-Select-EvaluateVariable">
                                <option selected value="Smart">Guess best approach</option>
                                <option value="Once">Create temp variable</option>
                                <option value="EachTime">Evaluate each time</option>
                            </select>
                        </div>

                        <div class="form-group row">
                            <label class="col-sm-4 col-form-label">
                                Select name
                            </label>
                            <select class="form-control col-sm-7" id="Cfg-Select-UseNumericIndex">
                                <option selected value="Yes">Make unique</option>
                                <option value="No">Reuse (fails if nested)</option>
                            </select>
                        </div>

                        <div class="form-group row">
                            <label class="col-sm-4 col-form-label">
                                Name prefix
                            </label>
                            <input type="text" class="form-control col-sm-7" id="Cfg-Select-SelectVariablePrefix"
                                   value="select_">
                        </div>
                    </li>
                    <li class="list-group-item">

                        <div class="form-group row">
                            <label class="col-sm-4 col-form-label">
                                With variable
                            </label>
                            <select class="form-control col-sm-7" id="Cfg-With-EvaluateVariable">
                                <option selected value="Once">Create temp variable</option>
                                <option value="EveryTime">Evaluate each time</option>
                            </select>
                        </div>

                        <div class="form-group row">
                            <label class="col-sm-4 col-form-label">
                                With name
                            </label>
                            <select class="form-control col-sm-7" id="Cfg-With-UseNumericIndex">
                                <option selected value="Yes">Make unique</option>
                                <option value="No">Reuse (fails if nested)</option>
                            </select>
                        </div>

                        <div class="form-group row">
                            <label class="col-sm-4 col-form-label">
                                Name prefix
                            </label>
                            <input type="text" class="form-control col-sm-7" id="Cfg-With-WithVariablePrefix"
                                   value="with_">
                        </div>
                    </li>

                </ul>

                <div class="modal-footer">
                    <button type="button" class="btn btn-danger" onclick="restoreDefaultConfig()">Defaults</button>
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-info" onclick="applyConfigChanges(false)">Save</button>
                    <button type="button" class="btn btn-primary" onclick="applyConfigChanges(true)">Save and Convert
                    </button>
                </div>
            </div>
        </div>
    </div>
</div>


<script>

    //region Storing and reloading configuration
    function applyConfigChanges(also_convert_code) {
        $('.form-control').each(function (idx, item) {
            if (item.id.startsWith('Cfg-')) {
                setCookie(item.id.substr(4), item.value, 365);
            }
        });
        $('#conversion-options').modal('hide');
        if (also_convert_code) {
            convert_code();
        }
    }

    function restoreDefaultConfig() {
        default_config.forEach(function (item) {
            $('#' + item[0])[0].value = item[1];
        })
    }

    function loadConfigFromCookie() {
        $('.form-control').each(function (idx, item) {
            if (item.id.startsWith('Cfg-')) {
                let value = getCookie(item.id.substr(4));
                if (value !== "") {
                    item.value = value;
                }
            }
        })
    }

    function getConfigAsJSON() {
        let result = '';
        $('.form-control').each(function (idx, item) {
            if (item.id.startsWith('Cfg-')) {
                let value = getCookie(item.id.substr(4));
                if (value !== "") {
                    let name = item.id.split('-');
                    if (result !== '') {
                        result += ', ';
                    }
                    result += (
                        '["' + name[1] + '", ' +
                        '"' + name[2] + '", ' +
                        '"' + item.value + '"]'
                    );
                }
            }
        })
        return '[' + result + ']';
    }

    function recordOptionsOpen() {
        if (!DEVELOPMENT) {
            gtag('event', 'Options', {
                'event_category': 'Open Options',
            });
        }
    }
    //endregion

    //region Cookie Handling
    function setCookie(cname, cvalue, exdays) {
        var d = new Date();
        d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
        var expires = "expires=" + d.toUTCString();
        document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
    }

    function getCookie(cname) {
        var name = cname + "=";
        var ca = document.cookie.split(';');
        for (var i = 0; i < ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) === ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) === 0) {
                return c.substring(name.length, c.length);
            }
        }
        return "";
    }
    //endregion

</script>