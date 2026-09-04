$(document).ready(function() {
    $('#tabla').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
        "paging": true,
        "pageLength": 10,
        "language": {
            "lengthMenu": "Mostrando _MENU_ registros por página",
            "zeroRecords": "No se encontraron registros - disculpe",
            "info": "Mostrando página _PAGE_ de _PAGES_",
            "infoEmpty": "No hay registros disponibles",
            "decimal":        "",
            "emptyTable":     "No hay registros disponibles en la tabla",
            "infoFiltered":   "(Filtrando de _MAX_ registros)",
            "infoPostFix":    "",
            "thousands":      ",",
            "loadingRecords": "Cargando...",
            "processing":     "Procesando...",
            "search":         "Buscar:",
            "paginate": {
                "first":      "Primero",
                "last":       "Último",
                "next":       "Siguiente",
                "previous":   "Anterior"
            },
            "aria": {
                "sortAscending":  ": Ordenar en forma ascendente",
                "sortDescending": ": Ordenar en forma descendente"
            }
        },
    });
});