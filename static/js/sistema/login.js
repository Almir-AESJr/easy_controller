$(document).ready(function () {
    $("#formlogin").submit(function () {
        var login = $.trim($("#login").val().toLowerCase());
        var senha = $.trim($("#senha").val().toLowerCase());

        if (login == "admin" && senha == "admin") {
            return true;
        } else {
            alert("Login inválido!");
            $("#login").focus();
            return false;
        }
    });
});