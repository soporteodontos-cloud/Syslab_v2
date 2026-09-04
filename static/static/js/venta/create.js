$(document).ready(function() {
    $('#id_numeroRecibo').inputmask("999-999-9999999");  //static mask
    $(".detalles").formset({
        prefix: "detalles",
        addText: "Agregar",
        deleteText: "Borrar",
        added: function (row) {
            row.find('.js-example-basic-single').select2();
            $('.entero').autoNumeric('destroy');
            $('.entero').autoNumeric('init', {
                mDec: '0',
                aSep: '.',
                aDec: ','
            });
            $('.decimal').autoNumeric('destroy');
            $('.decimal').autoNumeric('init', {
                mDec: '3',
                aSep: '.',
                aDec: ','
            });
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
        mDec: '3',
        aSep: '.',
        aDec: ','
    });

    $('.js-example-basic-single').select2();

    $(".delete-row").click(function () {
        cal_total();
    })

    $(".add-row").click(function () {
        $(".delete-row").click(function () {
            cal_total();
        })
    })

    var a = document.getElementById('id_nuevoCliente');
    change_cliente(a)

});

function change_cliente(a){
    if(a.checked){
        $('#id_razonSocial').parent().parent().show();
        $('#id_ruc').parent().parent().show();
        $('#id_dv').parent().parent().show();
    } else {
        $('#id_razonSocial').parent().parent().hide();
        $('#id_ruc').parent().parent().hide();
        $('#id_dv').parent().parent().hide();
        $('#id_razonSocial').val('');
        $('#id_ruc').val('');
        $('#id_dv').val('');
    }
}


function obt_precio(campo){
    if (!campo.value=="")
        $.ajax({
            method: 'GET',
            url: '/ventas/precio/'+campo.value+'/',
            headers: {"Content-Type": "application/json; charset=UTF-8"},
            contentType: 'application/json',
            processData: false,
        }).done(
            function (data) {
                if (data.precio == null && data.existencia == null){
                    alert('Este item no tiene existencia');
                    campo.value = "";
                    return;
                } else {
                    campo.parentNode.parentNode.nextSibling.nextSibling.childNodes[0].childNodes[0].value = data.precio;
                    campo.parentNode.parentNode.nextSibling.nextSibling.nextSibling.nextSibling.childNodes[0].childNodes[0].value = data.existencia;
                }
            });
    //else
    //    campo.parentNode.nextSibling.nextSibling.childNodes[1].value = "";
}

function subtotal(campo){
    var origen = campo.name.split('-');
    var cantidad = 0;
    var precio = 0;
    var total = 0;
    if (origen[2]=="cantidad"){
        var existencia = parseInt(campo.parentNode.parentNode.previousSibling.previousSibling.childNodes[0].childNodes[0].value.split('.').join(''));
        console.log(existencia)
        cantidad = parseFloat(campo.value.split('.').join('').split(',').join('.'));
        if (existencia < cantidad) {
            alert('Esta intentado vender una cantidad superior a la existente.');
            campo.value = "";
            return;
        } else {
            precio = parseInt(campo.parentNode.parentNode.previousSibling.previousSibling.previousSibling.previousSibling.childNodes[0].childNodes[0].value.split('.').join(''));
            if (isNaN(precio) == false && isNaN(cantidad) == false)
                total = precio * cantidad;
            campo.parentNode.parentNode.nextSibling.nextSibling.childNodes[0].childNodes[0].value = total.toLocaleString('en').split(',').join('.');
        }
    } else {
        precio = parseInt(campo.value.split('.').join(''));
        cantidad = parseFloat(campo.parentNode.parentNode.nextSibling.nextSibling.nextSibling.nextSibling.childNodes[0].childNodes[0].value.split('.').join('').split(',').join('.'));
        if (isNaN(precio)==false && isNaN(cantidad)==false)
            total = precio*cantidad;
        campo.parentNode.parentNode.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.childNodes[0].childNodes[0].value = total.toLocaleString('en').split(',').join('.');
    }
    cal_total();
}

function cal_total(){
    var total = 0;
    $( ".subtotal" ).each(function( index ) {
        if ($(this).parent().parent().parent().parent().is(":visible") == true){
            var subtotal = parseInt($(this).val().
            split('.').join(''));
            if (isNaN(subtotal)==false){
                total = total + subtotal;
            }
        }
    });
    $('#id_total').val((total).toLocaleString('en').split(',').join('.'));
}


function guardar(){
    $( ".entero" ).each(function( index ) {
        $(this).val(
            $(this).val().split('.').join('')
            );
    });
    $( ".decimal" ).each(function( index ) {
        $(this).val(
            $(this).val().split('.').join('').split(',').join('.')
            );
    });
    $('#formulario').submit();
}