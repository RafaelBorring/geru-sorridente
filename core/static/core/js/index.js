$(document).ready(function(){
    $(window).scroll(function(){
        if (window.pageYOffset >= 150) {
            $('#navbar-top').addClass("fixed-top container");
        } else {
            $('#navbar-top').removeClass("fixed-top");
        }
    });
});