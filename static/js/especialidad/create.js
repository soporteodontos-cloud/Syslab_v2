$(document).ready(function() {
    $(".detalles").formset({
        prefix: "detalles",
        addText: "Agregar",
        deleteText: "Borrar",
        added: function (row) {
            row.find('.js-example-basic-single').select2();
        }
    });
    $('.js-example-basic-single').select2();
});