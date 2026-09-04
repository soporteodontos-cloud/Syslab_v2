$(document).ready(function() {
    $('.js-example-basic-single').select2();
    $('.entero').autoNumeric('destroy');
    $('.entero').autoNumeric('init', {
        mDec: '0',
        aSep: '.',
        aDec: ','
    });
    $(".detalles").formset({
        prefix: "detalles",
        addText: "Agregar",
        deleteText: "Borrar",
    });
});

function submit(){
    $( ".entero" ).each(function( index ) {
        $(this).val(
            $(this).val().split('.').join('')
            );
    });
    $('#formulario').submit()
}