$(document).ready(function() {
    $('.js-example-basic-single').select2();
    $('.decimal').autoNumeric('destroy');
    $('.decimal').autoNumeric('init', {
        mDec: '2',
        aSep: '.',
        aDec: ','
    });
});

function submit(){
    $( ".decimal" ).each(function( index ) {
        $(this).val(
            $(this).val().split('.').join('').split(',').join('.')
            );
    });
    $('#formulario').submit()
}