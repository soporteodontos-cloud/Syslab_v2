var categoria = null;
var tipoTrabajo = null;
var color = null;
var trabajo = null;
var diasDuracion = null;
var diasDuracion5 = null;

$(document).ready(function() {
    $('.js-example-basic-multiple').select2({
        theme: "classic"
    });
    $('#id_maxilarSuperiorCompleto').parent().parent().hide();
    $('#id_maxilarInferiorCompleto').parent().parent().hide();
    $('#id_trabajoRepetido').parent().parent().hide();

    tabletrabajos = $('#trabajos').DataTable({
              "language": lenguaje,
              "serverSide": true,
              "ajax": '/rest/otr-list-intra/'+orden+'/?format=datatables',
              "scrollX": true,
              columnDefs: [
                    {
                        "targets": [0,1],
                        "visible": false
                    },
                ],
              "columns": [
                  {'data': 'maxilarSuperiorCompleto'},
                  {'data': 'maxilarInferiorCompleto'},
                  {'data': 'id'},
                  {
                      'data': function (row, type, val, meta) {
                          if (row.express == true) {
                              return 'SI'
                          } else {
                              return 'NO'
                          }
                      }
                  },
                  {'data': 'cantidad'},
                  {'data': 'color.marca.descripcion'},
                  {'data': 'color.codigo'},
                  {'data': 'categoria.descripcion'},
                  {'data': 'trabajo'},
                  {'data': 'fechaEntrega'},
                  {'data': 'observacion'},
                  {'data': 'dientes'},
                  {
                      'data': function (row, type, val, meta) {
                          if (row.maxilarSuperiorCompleto == true) {
                              return 'SI';
                          } else {
                              return 'NO';
                          }
                      }
                  },
                  {
                      'data': function (row, type, val, meta) {
                          if (row.maxilarInferiorCompleto == true) {
                              return 'SI';
                          } else {
                              return 'NO';
                          }
                      }
                  },
                  {'data': 'modoEnvio'},
                  {
                      'data': function (row, type, val, meta) {
                          var but = '';
                          if (estado=="PEDIDO NO CONFIRMADO") {
                              but+= '<a type="button" onclick="getOneEdit('+row.id+')" class="btn btn-warning btn-sm">Modificar</a> ';
                          }
                          but+= '<a type="button" onclick="changeTrabajo('+row.id+')" class="btn btn-danger btn-sm">Borrar</a>';
                          return but;
                      }
                  },
                ],
          });


    $(".fotos").formset({
        prefix: "detalles",
        addText: "Agregar",
        deleteText: "Borrar",
        added: function (row) {
            row.find('.js-example-basic-single').select2();
        }
    });
});


function getOneEdit(pk){
    $.ajax({
            method: 'GET',
            url: '/ordenes/workorder/'+pk+'/',
            headers: {"Content-Type": "application/json; charset=UTF-8"},
            contentType: 'application/json',
            processData: false,
        }).done(
            function (data) {
                console.log(data);
                trabajo = data.id;
                if (data.express == true){
                    $('#id_express').prop( "checked", true );
                } else {
                    $('#id_express').prop( "checked", false );
                };
                //$('#id_categoria').val(data.categoria.id).trigger('change');
                //$("#id_categoria").select2('data', {id:data.categoria.id, text:data.categoria.descripcion});
                var scategoria = $("#id_categoria");
                var option1 = new Option(data.categoria.descripcion, data.categoria.id, true, true);
                scategoria.append(option1).trigger('change');
                var strabajo = $("#id_trabajo");
                var option2 = new Option(data.trabajo.descripcion, data.trabajo.id, true, true);
                strabajo.append(option2).trigger('change');
                var scolor = $("#id_color");
                var option3 = new Option(data.color.marca.descripcion + ' - ' + data.color.codigo, data.color.id, true, true);
                scolor.append(option3).trigger('change');
                var sdientes = $("#id_dientes");
                for(var a = 0; a < data.dientes.length; a++){
                    var option4 = new Option(data.dientes[a], data.dientes[a], true, true);
                    sdientes.append(option4).trigger('change');
                };
                console.log(data.maxilarSuperiorCompleto);
                if (data.maxilarSuperiorCompleto == true){
                    $('#id_maxilarSuperiorCompleto').prop( "checked", true );
                    $('#id_maxilarSuperiorCompleto').parent().parent().show();
                } else {
                    $('#id_maxilarSuperiorCompleto').prop( "checked", false );
                    $('#id_maxilarSuperiorCompleto').parent().parent().hide();
                };
                if (data.maxilarInferiorCompleto == true){
                    $('#id_maxilarInferiorCompleto').prop( "checked", true );
                    $('#id_maxilarInferiorCompleto').parent().parent().show();
                } else {
                    $('#id_maxilarInferiorCompleto').prop( "checked", false );
                    $('#id_maxilarInferiorCompleto').parent().parent().hide();
                }
                $("#id_fechaEntrega").val(data.fechaEntrega);
                $("#id_modoEnvio").val(data.modoEnvio);
                $("#id_observacion").val(data.observacion);
            }
            );
}


function changeTrabajo(pk){
    var form = {
        'usuario': usuario,
        'orden': orden,
        'id': pk
    }

    $.ajax({
            method : 'POST',
            url : '/ordenes/workorder/delete/',
            contentType : 'application/json',
            data : JSON.stringify(form)
        }).done(function(data) {
            if (data.data == "OK"){
                alert("Trabajo borrado correctamente");
                tabletrabajos.ajax.reload();
            } else {
                alert("Ocurrio un error")
            }


    });
}


function saveTrabajo(){
    if (categoria != null && tipoTrabajo != null && color != null && $('#id_fechaEntrega').val() != ''){
        var form = {
            'orden': orden,
            'express': $('#id_express').is(":checked"),
            'categoria': categoria,
            'trabajo': tipoTrabajo,
            'color': color,
            'dientes': $('#id_dientes').select2("val"),
            'maxilarSuperiorCompleto': $('#id_maxilarSuperiorCompleto').is(":checked"),
            'maxilarInferiorCompleto': $('#id_maxilarInferiorCompleto').is(":checked"),
            'fechaEntrega': $('#id_fechaEntrega').val(),
            'modoEnvio': $('#id_modoEnvio').val(),
            'observacion': $('#id_observacion').val(),
            'usuario': usuario,
            'id': trabajo
        }

        console.log(form);

        $.ajax({
                method : 'POST',
                url : '/ordenes/workorder/',
                contentType : 'application/json',
                data : JSON.stringify(form)
            }).done(function(data) {
                if (data.data == "OK"){
                    alert("Trabajo guardado correctamente");
                    tabletrabajos.ajax.reload();
                    $('#id_fechaEntrega').val('');
                    $('#id_observacion').val('');
                    $('#id_categoria').val(null).trigger('change');
                    $('#id_trabajo').val(null).trigger('change');
                    $('#id_color').val(null).trigger('change');
                    $('#id_dientes').val(null).trigger('change');
                    $('#id_express').prop( "checked", false );
                    $('#id_maxilarSuperiorCompleto').prop( "checked", false );
                    $('#id_maxilarInferiorCompleto').prop( "checked", false );
                    $('#id_maxilarSuperiorCompleto').parent().parent().hide();
                    $('#id_maxilarInferiorCompleto').parent().parent().hide();
                } else {
                    alert("Ocurrio un error")
                }


        });
    } else {
        alert("Faltan datos, verifique.");
    }
}


function guardar(){
    if (tabletrabajos.rows().count() > 0) {
        $('#formulario').submit()
    } else {
        alert('No se han cargado trabajos.');
    }
}


function change_metodo(){
    $('#id_trabajoRepetido').val('');
    if ($('#id_metodoEnvio').val() == "Repetición"){
        $('#id_trabajoRepetido').parent().parent().show();
    } else {
        $('#id_trabajoRepetido').parent().parent().hide();
    };
}

$(document).bind('change', function (e) {
    console.log(e.target.name)
    if (e.target.name == 'categoria'){
      if (isNaN(parseInt(e.target.value)) == false)
        categoria = parseInt(e.target.value);
      else
        categoria = null;
    } else if (e.target.name == 'color'){
      if (isNaN(parseInt(e.target.value)) == false)
        color = parseInt(e.target.value);
      else
        color = null;
    } else if (e.target.name == 'trabajo'){
        if (isNaN(parseInt(e.target.value)) == false) {
            tipoTrabajo = parseInt(e.target.value);
            $.ajax({
                method: 'GET',
                url: '/ordenes/workmet/' + e.target.value + '/',
                headers: {"Content-Type": "application/json; charset=UTF-8"},
                contentType: 'application/json',
                processData: false,
            }).done(
                function (data) {
                    if (data.met == "MAXILAR") {
                        $('#id_maxilarSuperiorCompleto').parent().parent().show();
                        $('#id_maxilarInferiorCompleto').parent().parent().show();
                    } else {
                        $('#id_maxilarSuperiorCompleto').parent().parent().hide();
                        $('#id_maxilarSuperiorCompleto').prop("checked", false);
                        $('#id_maxilarInferiorCompleto').parent().parent().hide();
                        $('#id_maxilarInferiorCompleto').prop("checked", false);
                    }
                    diasDuracion = data.dias;
                    diasDuracion5 = data.dias5;
                    var fsolicitud = $('#id_fechaSolicitud').val();
                    console.log(fsolicitud);
                    //var newDate =  moment(fsolicitud,"YYYY-MM-DD");
                    var newDate = moment();
                    if ((newDate.day() + diasDuracion) > 7)
                        dias = diasDuracion + 1;
                    else
                        dias = diasDuracion;
                    var dateJob = newDate.add(dias, 'days').format("yyyy-MM-DD");
                    console.log(dateJob);
                    $('#id_fechaEntrega').val(dateJob);
                }
            );
        }
      else
        tipoTrabajo = null;
     } else if (e.target.name == 'dientes'){
            if ($('.js-example-basic-multiple').select2("val").length >= 5){
                var newDate =  moment();
                if ((newDate.day() + diasDuracion5) > 7)
                    dias = diasDuracion5+1;
                if ((newDate.day() + diasDuracion5) > 14)
                    dias = diasDuracion5+2;
                else
                    dias = diasDuracion5;
                var dateJob = newDate.add(dias, 'days').format("yyyy-MM-DD");
                console.log(dateJob);
                $('#id_fechaEntrega').val(dateJob);
            } else {
                var newDate =  moment();
                if ((newDate.day() + diasDuracion) > 7)
                    dias = diasDuracion+1;
                else
                    dias = diasDuracion;
                var dateJob = newDate.add(dias, 'days').format("yyyy-MM-DD");
                console.log(dateJob);
                $('#id_fechaEntrega').val(dateJob);
            }
    }
 });