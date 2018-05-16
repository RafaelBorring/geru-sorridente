$(document).ready(function(){
    $("input").keyup(function(){
		this.value = this.value.toUpperCase();
    });
    $("#id_username").mask("999 9999 9999 9999");
    $("#id_username").attr("placeholder", "700 0000 0000 0000");
    $("#id_cns").mask("999 9999 9999 9999");
    $("#id_cns").attr("placeholder", "700 0000 0000 0000");
    $("#id_nome").attr("placeholder", "JOÃO SANTOS");
    $("#id_nascimento").mask("99/99/9999");
    $("#id_nascimento").attr("placeholder", "01/01/2001");
    $("#id_endereco").attr("placeholder", "RUA A");
    $("#id_telefone").mask("(99) 99999-9999");
    $("#id_telefone").attr("placeholder", "(79) 99988-1234");
	$("#id_telefone").on("blur", function(){
	    var last = $(this).val().substr($(this).val().indexOf("-") + 1);
	    if (last.length == 3) {
	        var move = $(this).val().substr($(this).val().indexOf("-") - 1, 1);
	        var lastfour = move + last;
	        var first = $(this).val().substr(0, 9);
	        $(this).val(first + "-" + lastfour);
	    }
    });
});