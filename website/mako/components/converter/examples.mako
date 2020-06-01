
<div style="display: none">
    %for name, container, content in attributes['examples']:
        %if name:
            %if container:
                <div id="ex-${name}" context="${container}">
            %else:
                <div id="ex-${name}">
            %endif
            ${content}
            </div>
        %endif
    %endfor
</div>

<script>
        function getExample(name) {
        //
        // Get the text
        let e = null;
        if (name == 'initial') {
            e = $('#ex-general')[0];
        } else {
            e = $('#ex-' + name)[0];
        }
        vbeditor.session.setValue(unescape(e.innerHTML));
        //
        // Set the context
        let context = e.attributes['context'];
        if ($('#context')[0]) {
            if (context == null) {
                $('#context')[0].value = 'code';
            } else {
                $('#context')[0].value = context.textContent;
            }
        }
        if (name !== 'initial') {
            convert_code('Demo');
            if (!DEVELOPMENT) {
                gtag('event', 'Example', {
                    'event_category': 'Example',
                    'event_label': name,
                });
            }
        }
    }
</script>