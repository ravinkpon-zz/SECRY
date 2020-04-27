$(window).on('load',function () {
    $(".loader").fadeOut("slow");;
});


$(window).scroll(function () {
        $('nav').toggleClass('scrolled',$(this).scrollTop()>200);
    });

    
$(document).ready(function () {
    $('.upload-form input').change(function () {
        $('.upload-form p').text(this.files.length + " file(s) selected");
    });
});

$(document).ready(function () {
    window.setTimeout("fadeMyDiv();", 3000); //call fade in 3 seconds
})

function fadeMyDiv() {
    $("#myDiv").fadeOut('slow');
}

$('.table tbody').on('click', '.btn', function () {
     var currow = $(this).closest('tr');
     var fid = currow.find('td:eq(0)').text();
     var fname = currow.find('td:eq(1)').text();
     $('form #fileid').val(fid);
     $('form #filename').val(fname);
})

$(document).ready(function () {
    $('#post-form').on('submit', function (e) {
        e.preventDefault();
        $('#cover-spin').show(0);
        var filename = $('#filename').val()
        var formData = new FormData(this);
        $.ajax({
            type: 'POST',
            url: 'download_file', 
            data: formData,
            cache: false,
            contentType: false,
            processData: false,
            success: function (response, status, xhr) {
                location.reload(true);
                var disposition = xhr.getResponseHeader('Content-Disposition');
                var type = xhr.getResponseHeader('Content-Type');
                var blob = new Blob([response], {
                    type: type
                });
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
            },
            error:function(response) {  
                $('#cover-spin').fadeOut('fast'); 
                alert(response.responseJSON.error);
            }
        })
    })
})

function upvalid(){
    var file = document.getElementById('myfile');
    var size = file.files[0].size;
    if (size > 41943040) {
        file.setCustomValidity("File size exceed the limit");
    } else {
        $('#cover-spin').show(0);
    }
}