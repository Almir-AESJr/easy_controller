async function enviarDados() {

    let denominador = $("#denominador").val();
    let numerador = $("#numerador").val();
    $("#denominador").prop("disabled", true);
    $("#numerador").prop("disabled", true);
    $("#denominadorH").prop("disabled", true);
    $("#numeradorH").prop("disabled", true);
    $("#denominadorD").prop("disabled", true);
    $("#numeradorD").prop("disabled", true);

    console.log(denominador);
    console.log(numerador);


    let response = await $.ajax({
        url: "chamadas/dadosgrafico",
        data: {
            numerador: numerador,
            denominador: denominador

        },
        error: function (e) {
            alert(e.responseText);
            console.log("Erro: ", e);
        },
    });

    console.log(response.newY);
    console.log(response.newX);
    console.log(response.newEquacao);
    console.log(response.newnumerador);
    console.log(response.newdenominador);

    for (i = 0; i < response.newEquacao.length; i++) {
        if (i == 1) {
            $("#numeradoreq").empty().append(response.newEquacao[i]);
        } else if (i == 2){
            $("#barraeq").empty().append(response.newEquacao[i]);
        } else if (i == 3){
            $("#denominadoreq").empty().append(response.newEquacao[i]);
        }
        

    }

    $("#equacao").html(response.newEquacao);


    let eixo_x = response.newX;
    let eixo_y = response.newY;

    let traco = {
        x: eixo_x,
        y: eixo_y,
        mode: 'line',
        type: 'scatter'
    };

    let localGrafico = document.getElementById('local-grafico');
    var layout3 = {
        title: 'Resposta ao degrau unitário',
        titlefont: {
          family: 'Arial, sans-serif',
          size: 28,
          color: 'black'},
        xaxis: {
          title: 'Tempo',
          titlefont: {
            family: 'Arial, sans-serif',
            size: 28,
            color: 'black'
          },
          showticklabels: true,
          tickangle: 'auto',
          tickfont: {
            family: 'Old Standard TT, serif',
            size: 24,
            color: 'black'
          },
          exponentformat: 'e',
          showexponent: 'all'
        },
        yaxis: {
          title: 'Amplitude',
          titlefont: {
            family: 'Arial, sans-serif',
            size: 28,
            color: 'black'
          },
          showticklabels: true,
          tickangle: 45,
          tickfont: {
            family: 'Old Standard TT, serif',
            size: 24,
            color: 'black'
          },
          exponentformat: 'e',
          showexponent: 'all'
        }
      };
    $('#texto').show(); //.hide() para esconder
    $('#card2').show(); //.hide() para esconder
    $('#card1').show();
    $('#malha_fechada').hide();
    $('#card3').hide();
    Plotly.newPlot(localGrafico, [traco], layout3);
}

$('#botao-de-envio').on('click', enviarDados);