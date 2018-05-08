$(document).ready(function(){
    $(window).scroll(function(){
        if (window.pageYOffset >= $("img").height()) {
            $("#navbar-top").addClass("fixed-top container");
        } else {
            $("#navbar-top").removeClass("fixed-top");
        }
    });
});