$(document).ready(function() {
    $.getJSON("/agenda_closed/", function(data) {
        var teste = $.isEmptyObject(data);
        if (! teste) {
            $.each(data, function(key, val) {
                 if (val.fields.mes) {
                    $('#' + val.fields.mes).removeClass('btn-warning').addClass('btn-success').removeAttr('href');
                 }
            });
        }
    });
});