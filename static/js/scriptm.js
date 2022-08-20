async function enviarDadosMatriz() {

    let m1 = $("#m1").val();
    
    console.log(m1);
    

    let response = await $.ajax({
        url: "chamadamatriz/dadosmatriz",
        data: {
            m1: m1,
            

        },
        error: function (e) {
            alert(e.responseText);
            console.log("Erro: ", e);
        },
    });
    
}
$('#enviar-matriz').on('click', enviarDadosMatriz);