$(window).scroll(function () {
        $('nav').toggleClass('scrolled',$(this).scrollTop()>200);
    });

    
$(document).ready(function () {
    $('.upload-form input').change(function () {
        $('.upload-form p').text(this.files.length + " file(s) selected");
    });
});