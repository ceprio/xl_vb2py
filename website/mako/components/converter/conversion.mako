
<script>

    var vb_marker = null;
    var py_marker = null;
    let conversion_expected_duration = 0.0;
    let conversion_total_duration = 0.0;
    let conversion_callback_interval = 500.0;
    let conversion_show_progress = true;
    let conversion_bar = null;
    let start_time = null;

    $(document).ready(function () {
        conversion_bar = $('#progress-indicator');
    });

    function convert_selection() {
        let range = vbeditor.selection.getRange();
        let selected_text = vbeditor.getSession().doc.getTextRange(range);
        //
        // If nothing was selected then just do the current line
        if (selected_text.length == 0) {
            range.start.column = 0;
            range.end.column = 1000;
            selected_text = vbeditor.getSession().doc.getTextRange(range);
        }
        convert_text(selected_text, range.start.row, 'Selection');
    }

    function convert_code(category) {
        let vbtext = vbeditor.getValue();
        convert_text(vbtext, 0, category);
    }

    function convert_text(vbtext, selection_offset, category) {
        show_start_conversion(vbtext);

        var context = $('#context')[0].value;
        var type = $('#type')[0].value;
        var class_name = $('#class-name')[0].value;
        var number_of_lines = vbtext.split(/\r\n|\r|\n/).length;

        var language = 'Unset Language';

        var url;
        if (context == 'code') {
            url = '/single_code_module';
        } else if (context == 'class') {
            url = '/single_class_module';
        } else {
            url = '/single_form_module';
        }
        var conversion_style;
        if (type == 'exact') {
            conversion_style = 'vb';
        } else {
            conversion_style = 'pythonic';
        }

        // Clear old markers and errors
        if (vb_marker != null) {
            vbeditor.session.removeMarker(vb_marker);
        }
        if (py_marker != null) {
            pyeditor.session.removeMarker(py_marker);
        }

        for (item in vbeditor.session.getMarkers(true)) {
            vbeditor.session.removeMarker(item)
        }
        for (item in pyeditor.session.getMarkers(true)) {
            pyeditor.session.removeMarker(item)
        }
        let failure_mode = $('#failure-mode')[0].value;
        let dialect = $('#dialect')[0].value;

        let config = getConfigAsJSON();

        if (!DEVELOPMENT && window.performance) {
            start_time = window.performance.now();
        }

        $.post(HOST + url, {
            'text': vbtext, 'style': conversion_style, 'class_name': class_name,
            'failure-mode': failure_mode, 'dialect': dialect, 'options': config
        }, function (data) {
            if (!DEVELOPMENT && window.performance) {
                let end_time = window.performance.now();
                let duration = end_time - start_time;
                let label = (data.parsing_failed ? "Parsing Failed" : "Succeeded");
                gtag('event', 'timing_complete', {
                    'name': 'Conversion',
                    'value': duration,
                    'event_category': category,
                    'event_label': label,
                })
            }
            if (data.status === 'OK') {
                pyeditor.session.setValue(data.result);
                let vb_error_list = $('#error-list')[0];
                vb_error_list.innerHTML = '';
                // Watch for parsing failure
                if (data.parsing_failed) {
                    show_stop_conversion(false);
                    for (i = 0; i < data.parsing_stopped_vb.length; i++) {
                        let vb_offset = data.parsing_stopped_vb[i] + selection_offset;
                        let py_offset = data.parsing_stopped_py[i];
                        let Range = ace.require('ace/range').Range;
                        vb_marker = vbeditor.session.addMarker(new Range(vb_offset, 0, vb_offset, 100),
                            "errorMarker", "line", true);

                         vb_error_list.innerHTML += get_error_menu_item(
                             vbeditor.session.getLine(vb_offset),
                             vb_offset,
                             data.parsing_stopped_py[i]
                         );

                        py_marker = pyeditor.session.addMarker(new Range(data.parsing_stopped_py[i], 0, data.parsing_stopped_py[i], 100),
                            "errorMarker", "line", true);

                        if (i === 0) {
                            vbeditor.scrollToLine(vb_offset);
                            pyeditor.scrollToLine(data.parsing_stopped_py);
                        }
                    }

                    ##  $('#error_message')[0].style['display'] = 'block';
                    ##  if (data.language === 'VB.NET') {
                    ##      $('#dot_net_message')[0].style['display'] = 'block';
                    ##  } else if (data.language === 'VBP') {
                    ##      show_language_alert('a VB Project File', 'type');
                    ##  } else if (data.language === 'C#') {
                    ##      show_language_alert('a C#, C++ or C File', 'language');
                    ##  }
                    ##  ;
                    language = data.language;

                } else {
                    show_stop_conversion(true);
                    ##  document.getElementsByClassName('error-header')[0].style.display = 'none';
                    ##  document.getElementsByClassName('error-header')[1].style.display = 'none';
                }
                if (!DEVELOPMENT) {
                    let label = (data.parsing_failed ? "Parsing Failed" : "Succeeded");
                    gtag('event', 'Convert', {
                        'event_category': category + '(' + data.language + ')',
                        'event_label': label,
                        'parameter1': data.language,
                        'value': number_of_lines
                    });
                }
            } else {
                show_stop_conversion(false);
                alert('Came back ' + data.status + ': ' + data.result);
                if (!DEVELOPMENT) {
                    gtag('event', 'Convert', {
                        'event_category': category,
                        'event_label': "Server Status Error: " + data.status + ", " + data.result,
                    });
                }
                ;
            }
            ##  $('#version')[0].innerHTML = '(VB2PY version=' + data.version + ')';
        }, 'json')
            .fail(function (data, status, error) {
                show_stop_conversion(false);
                pyeditor.session.setValue('There was an error talking to the server\nStatus=' +
                    status + '\n' + 'Error=' + error);
                if (!DEVELOPMENT) {
                    gtag('event', 'Convert', {
                        'event_category': category,
                        'event_label': "Server AJAX Error - " + error + " - " + status + " = " +
                            vbtext.split('\n').length,
                    });
                };
                $.get(HOST + '/server_log?text=Ajax Failure');
            });
    }

    function estimateTime(text) {
        // Return an estimate of how long it will take to convert
        return 0.2 * 0.0189 * text.split('\n').length + 0.1;
    }

    function show_start_conversion(text) {
        conversion_expected_duration = estimateTime(text);
        conversion_total_duration = 0.0;
        setTimeout(updateProgress, conversion_callback_interval);
        conversion_show_progress = true;
        conversion_bar.css('width', '0%');
        conversion_bar.removeClass('bg-warning');
        conversion_bar.removeClass('bg-success');
        conversion_bar.addClass('bg-info');
        $('#conversion-progress-toast').toast('show');
    }

    function show_stop_conversion(succeeded) {
        conversion_show_progress = false;
        conversion_bar.removeClass('bg-info');
        if (succeeded) {
            conversion_bar.addClass('bg-success');
            $('#conversion-progress-toast').toast('hide');
        } else {
            conversion_bar.addClass('bg-warning');
        }
    }

    function updateProgress() {
        if (conversion_show_progress) {
            conversion_total_duration += conversion_callback_interval / 1000.0;
            let pc_done = conversion_total_duration / conversion_expected_duration * 100.0;
            if (pc_done > 90) {
                pc_done = 90;
            }
            $('.progress-bar').css('width', pc_done.toString() + '%').attr('aria-valuenow', pc_done.toString());
            setTimeout(updateProgress, conversion_callback_interval);
        } else {
            $('.progress-bar').css('width', '100%');
        }
    }

</script>