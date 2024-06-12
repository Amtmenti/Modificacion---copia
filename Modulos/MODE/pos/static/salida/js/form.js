var input_fecha_s;
var input_hora_salida;

$(function () {
    // Inicializar fecha_e
    input_fecha_s = $('input[name="fecha_s"]');

    input_fecha_e.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
    });

    // Inicializar hora_salida
    input_hora_salida = $('input[name="hora_salida"]');

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
