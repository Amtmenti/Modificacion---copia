var input_fecha;
var input_hora_entrada;
var input_hora_salida;

$(function () {
    // Inicializar input_fecha
    input_fecha = $('input[name="fecha"]');

    input_fecha.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
    });

    // Inicializar input_hora_entrada
    input_hora_entrada = $('input[name="hora_entrada"]');

    input_hora_entrada.datetimepicker({
        useCurrent: false,
        format: 'hh:mm',
        locale: 'es',
        keepOpen: false,
    });

    // Inicializar input_hora_salida
    input_hora_salida = $('input[name="hora_salida"]');

    input_hora_salida.datetimepicker({
        useCurrent: false,
        format: 'hh:mm',
        locale: 'es',
        keepOpen: false,
    });

    // Inicializar select2 para el campo alumno
    $('.select2').select2({
        language: 'es',
        theme: 'bootstrap4'
    });
});
