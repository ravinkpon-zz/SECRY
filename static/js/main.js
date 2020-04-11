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

$('.upload-form').submit((e) => {
    $('#submit').html('<span class="spinner">Uploading<span class="bounce1"></span><span class="bounce2"></span><span class = "bounce3"></span></span>');
});