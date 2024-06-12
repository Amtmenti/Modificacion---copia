var input_periodo_inicio;
var input_periodo_termino;
var input_horas_totales;

$(function () {
    // Inicializar input_periodo_inicio
    input_periodo_inicio = $('input[name="periodo_inicio"]');

    input_periodo_inicio.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
    });

   input_periodo_termino = $('input[name="periodo_termino"]');

    input_periodo_termino.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
    });

    // Inicializar input_horas_totales
    input_horas_totales = $('input[name="hora_entrada"]');

    input_horas_totales.datetimepicker({
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

    // Validación de nombre (solo letras)
    $('input[name="nombre"]').on('keypress', function (e) {
        return validate_text_box({'event': e, 'type': 'letters'});
    });

    // Validación de teléfono (solo números)
    $('input[name="telefono"]').on('keypress', function (e) {
        return validate_text_box({'event': e, 'type': 'numbers'});
    });
});
