<div class="modal" tabindex="-1" role="dialog" id="load-file-modal">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Load File</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body">
                <div class="input-group mb-3">
                    <div class="input-group-prepend">
                        <span class="input-group-text" id="inputGroupFileAddon01">Load File</span>
                    </div>
                    <div class="custom-file">
                        <input type="file" class="custom-file-input" id="inputGroupFile01"
                               aria-describedby="inputGroupFileAddon01" onchange="openFile(event)">
                        <label class="custom-file-label" for="inputGroupFile01">Choose file</label>
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
            </div>
        </div>
    </div>
</div>


<script>
    function openFile(event) {
        $('#load-file-modal').modal('hide');
        var input = event.target;
        var reader = new FileReader();
        reader.onload = function () {
            var text = reader.result;
            vbeditor.session.setValue(text);
        };

        if (input.files.length != 0) {
            reader.readAsText(input.files[0]);
            let extn = input.files[0].name.toLowerCase();
            let context = $('#context')[0];
            let class_name = $('#class-name')[0];
            let chosen_name = input.files[0].name.split('.')[0];
            chosen_name = chosen_name.replace(/ /g, "_");
            if (extn.endsWith('.frm')) {
                context.selectedIndex = 2;
                class_name.value = chosen_name;
            } else if (extn.endsWith('.cls')) {
                context.selectedIndex = 1;
                class_name.value = chosen_name;
            } else if (extn.endsWith('.vb')) {
                context.selectedIndex = 1;
                class_name.value = chosen_name;
            } else {
                context.selectedIndex = 0;
            }
            if (!DEVELOPMENT) {
                gtag('event', 'Load', {
                    'event_category': 'File',
                    'event_label': extn.split(".")[1],
                });
            }
        }
    };
</script>