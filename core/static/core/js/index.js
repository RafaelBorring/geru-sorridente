$(document).ready(function(){
    $(window).scroll(function(){
        if (window.pageYOffset >= $("img").height()) {
            $("#navbar-top").addClass("fixed-top container");
            $("main").css('margin-top', $("img").height());
        } else {
            $("#navbar-top").removeClass("fixed-top");
            $("main").css('margin-top', 0);
        }
    });
});