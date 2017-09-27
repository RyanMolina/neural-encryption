jQuery(document).ready(function($) {

    // Start
    $('#loader').hide();
    toggleShowButtons(false);

    function toggleShowButtons(visible) {
        if (visible == true) {
            $('#delete-image').show();
            $('#input-image').removeClass('img-placeholder')
            $('#encrypt-file-btn').show();
            $('#decrypt-file-btn').show();
        } else {
            $('#delete-image').hide();
            $('#encrypt-file-btn').hide();
            $('#decrypt-file-btn').hide();
            $('#download-file-btn').hide();
        }
    }

    // Upload Image
    $('#upload-input').click(function() {
        $(this).val("");
    });
    $('#upload-input').change(function(selected) {
        var files = selected.target.files;
        var file = files[0]
        var reader = new FileReader();
        reader.onload = (function (f) {
            return function(e) {
                if(e.target.result.substring(5,10) == "image") {
                    $('#input-image').attr('src', e.target.result);
                    $('#file-uploader').hide();
                    toggleShowButtons(true);
                } else {
                    alert("Sorry, file must be valid image format" );
                }
            };
        })(file);
        reader.readAsDataURL(file);
    });


    // Send to Flask
    function cryptography(url) {
        var key = $('#enc-dec-key').val();
        if (key != "") {
            var form_data = new FormData($('#upload-file')[0]);
            form_data.append("encryption_key", key);
            $('#input-image').addClass('blur');
            $('#loader').show();
            toggleShowButtons(false);
            $.ajax({
                type: 'post',
                url: url.data.url,
                processData: false,
                cache: false,
                contentType: false,
                data: form_data,
                success: function (response) {
                    $('#output-image').attr('src', response)
                    $('#delete-image').show();
                    $('#loader').hide();
                    $('#input-image').removeClass('blur');
                    $('#output-image').removeClass('img-placeholder');
                    $('#download-file-btn')
                            .show()
                            .attr('href', $('#output-image').attr('src'))
                            .attr('download', makeid());
                }
            });
        } else {
            alert("Fill the encryption keyfield")
        }
    }
    $('#encrypt-file-btn').on('click', {url: '/encrypt'}, cryptography);
    $('#decrypt-file-btn').on('click', {url: '/decrypt'}, cryptography);
    // Reset the image
    $('#delete-image').click(function() {
        $('#input-image').removeAttr('src');
        $('#output-image').removeAttr('src');
        $('#input-image').addClass('img-placeholder')
        $('#output-image').addClass('img-placeholder')
        $('#file-uploader').show();
        toggleShowButtons(false);
    });

    function makeid() {
        var text = "";
        var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
        for (var i = 0; i < 5; i++) {
            text += possible.charAt(Math.floor(Math.random() * possible.length));
        }
        return text;
    }
});

