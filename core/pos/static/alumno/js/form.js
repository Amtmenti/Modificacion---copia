var input_periodo_inicio;
var input_periodo_termino;

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
