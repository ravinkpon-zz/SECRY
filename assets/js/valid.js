window.onload = function () {
    if (document.getElementById("pass") && document.getElementById("re_pass"))
    {
        var txtPassword = document.getElementById("pass");
        var txtConfirmPassword = document.getElementById("re_pass");
        txtPassword.onchange = ConfirmPassword;
        txtConfirmPassword.onkeyup = ConfirmPassword;
        function ConfirmPassword() {
            txtConfirmPassword.setCustomValidity("");
            if (txtPassword.value != txtConfirmPassword.value) {
                txtConfirmPassword.setCustomValidity("Passwords do not match.");
            }
        }
    }
}


// Disable form submissions if there are invalid fields
(function () {
    'use strict';
    window.addEventListener('load', function () {
        // Get the forms we want to add validation styles to
        var forms = document.getElementsByClassName('needs-validation');
        // Loop over them and prevent submission
        var validation = Array.prototype.filter.call(forms, function (form) {
            form.addEventListener('submit', function (event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }, false);
});

$(document).ready(function () {
    $('form.upload-form').on('submit', function (e) {
        var file = document.getElementById('myfile');
        var size = file.files[0].size;
        if (size > 41943040) 
        {
            file.setCustomValidity("File size exceed the limit");
        }
        else
        {
            $('#cover-spin').show(0);
        }
    });
}