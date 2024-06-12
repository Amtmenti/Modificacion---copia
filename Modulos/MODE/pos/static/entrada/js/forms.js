var input_fecha_e;
var input_hora_entrada;

$(function () {
    // Inicializar fecha_e
    input_fecha_e = $('input[name="fecha_e"]');

    input_fecha_e.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
    });

    // Inicializar hora_entrada
    input_hora_entrada = $('input[name="hora_entrada"]');

    input_hora_entrada.datetimepicker({
        useCurrent: false,
        format: 'hh:mm',
        locale: 'es',
        keepOpen: false,
    });

    // Inicializar select2
    $('.select2').select2({
        language: 'es',
        theme: 'bootstrap4'
    });

});
