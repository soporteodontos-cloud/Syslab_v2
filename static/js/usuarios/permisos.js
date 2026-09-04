$(document).ready(function() {
    $('.guardar').on('click', function(e) {
        $(this).attr('disabled', true);
    });
} );

function addall(){
    var values = $("#id_user_permissions_all>option");
    var select = document.getElementById("id_user_permissions_added");
    for (var a = 0; a < values.length; a++){
        select.add(values[a]);
    }
};

function removeall(){
    var values = $("#id_user_permissions_added>option");
    var select = document.getElementById("id_user_permissions_all");
    for (var a = 0; a < values.length; a++){
        select.add(values[a]);
    }
};

function add(){
    var a = $('#id_user_permissions_all').find(":selected");
    var select = document.getElementById("id_user_permissions_added");
    select.add(a[0]);
};

function remove(){
    var a = $('#id_user_permissions_added').find(":selected");
    var select = document.getElementById("id_user_permissions_all");
    select.add(a[0]);
};

function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

function save() {
    var $crf_token = readCookie('csrftoken');
    var permissions = []
    var values = $("#id_user_permissions_added>option");
    for (var a = 0; a < values.length; a++){
        permissions.push(values[a].value);
    }
    var body = {
        permisos: permissions,
        usuario: parseInt($('#usuario').val()),
    };
    $.ajax({
        method: 'POST',
        url: '/usuario/permisos',
        contentType: 'application/json',
        headers: {"X-CSRFToken": $crf_token, "Content-Type": "application/json; charset=UTF-8"},
        data: JSON.stringify(body),
        processData: false,
    }).done(
        function (data) {
            window.location.href = '/usuarios'
    });
}

