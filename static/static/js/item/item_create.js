$(document).ready(function() {
    $(".detalles").formset({
        prefix: "detalles",
        addText: "Agregar",
        deleteText: "Borrar",
        added: function (row) {
            row.find('.js-example-basic-single').select2();
        }
    });

    $('.entero').autoNumeric('destroy');
    $('.entero').autoNumeric('init', {
        mDec: '0',
        aSep: '.',
        aDec: ','
    });

    $('.decimal').autoNumeric('destroy');
    $('.decimal').autoNumeric('init', {
        mDec: '2',
        aSep: '.',
        aDec: ','
    });

    $('.js-example-basic-single').select2();

    var condicion = document.getElementById('id_controlStock');
    change_comprobante(condicion);

});


function change_comprobante(a){
    if(a.checked){
        $('#id_cantidadMinima').parent().show();
        $('#id_dias').val('');
    } else {
        $('#id_cantidadMinima').parent().hide();
        $('#id_dias').val('');
    };
}


function guardar(){
    $('.entero').each(function( index ) {
        $(this).val(
            $(this).val().split('.').join('')
        );
    });
    $('.decimal').each(function( index ) {
        $(this).val(
            $(this).val().split('.').join('').split(',').join('.')
        );
    });
    $('#formulario').submit();
}