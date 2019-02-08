$(document).ready(function() {
    $("#desmarcar").click(function(event) {
        if (confirm('Deseja realmente desmarcar a consulta?')) {
            return true;
        }
        else {
            return false;
        }
     });
});