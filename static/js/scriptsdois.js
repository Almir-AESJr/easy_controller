async function enviarDados2() {
    
    let amostragem = $("#amostragem").val();
    let amostragem1 = $("#amostragem1").val();
    let saturacao1 = $("#saturacao1").val();
    let referencia = $("#referencia").val();
    let saturacao = $("#saturacao").val();
    let controladores = $("#controlador").val();
    let kp = $("#kp").val();
    let ti = $("#ti").val();
    let td = $("#td").val();
    let controladorescalc = $("#controladorcalc").val();
    let denominador = $("#denominador").val();
    let numerador = $("#numerador").val();
    $("#denominador").prop("disabled", false);
    $("#numerador").prop("disabled", false);
    $("#denominadorH").prop("disabled", false);
    $("#numeradorH").prop("disabled", false);
    $("#denominadorD").prop("disabled", false);
    $("#numeradorD").prop("disabled", false);

    console.log(saturacao1);
    console.log(controladores);
    console.log(amostragem);
    console.log(referencia);
    console.log(kp);
    console.log(ti);
    console.log(td);

    let response = await $.ajax({
        url: "chamadas2/dadosgrafico2",
        data: {
            saturacao1: saturacao1,
            amostragem1: amostragem1,
            controladores: controladores,
            amostragem: amostragem,
            referencia: referencia,
            saturacao:  saturacao,
            kp: kp,
            ti: ti,
            td: td,
            numerador: numerador,
            controladorescalc: controladorescalc,
            denominador: denominador
        },
        error: function (e) {
            alert(e.responseText);
            console.log("Erro: ", e);
        },
    });

    console.log(response.newsaida);
    console.log(response.newcontrole);
    console.log(response.newtempo);
    console.log(response.newamostragem);
    for (i = 0; i < response.newG.length; i++) {
        if (i == 1) {
            $("#numeradoreq1").empty().append(response.newG[i]);
        } else if (i == 2){
            $("#barraeq1").empty().append(response.newG[i]);
        } else if (i == 3){
            $("#denominadoreq1").empty().append(response.newG[i]);
        }
        

    }
    
    let kp2 = response.newkp;
    let ti2 = response.newti;
    let td2 = response.newtd;
    let referencia2 = response.newreferencia;
    let amostragem5 = response.newamostragem;
    let saturacao5 = response.newsaturacao;
    let eixo_x = response.newtempo;
    let eixo_yy = response.newsaida;
    let eixo_yu = response.newcontrole;

    let sinalsaida = {
        x: eixo_x,
        y: eixo_yy,
        mode: 'line',
        type: 'scatter'
    };

    let sinalcontrole = {
        x: eixo_x,
        y: eixo_yu,
        mode: 'line',
        type: 'scatter'
    };


    let controlesaida = document.getElementById("controle-saida");
    var layout1 = {
        title: 'Sinal de saída', 
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
    let controlecontrole = document.getElementById('controle-controle');
    var layout2 = {
        title: 'Sinal de controle',
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
    $('#card2').show();
    $('#card3').show();

    Plotly.newPlot(controlesaida, [sinalsaida],layout1);
    Plotly.newPlot(controlecontrole, [sinalcontrole],layout2);

    $('#kp1').val(kp2);
    kp1.disabled = true;
    $('#ti1').val(ti2);
    ti1.disabled = true;
    $('#td1').val(td2);
    td1.disabled = true;
    $('#amostragemo').val(amostragem5);
    amostragemo.disabled = true;
    $('#saturacaoo').val(saturacao5);
    saturacaoo.disabled = true;
    $('#referencia1').val(referencia2);
    referencia1.disabled = true;

    if(controladores==4){
      $('#textoPI').hide();
      $('#textoPD').hide();
      $('#textoP').hide();
      $('#textoPID').show();
    }
    if(controladores==3){
      $('#textoPI').hide();
      $('#textoPID').hide();
      $('#textoP').hide();
      $('#textoPD').show();
    }
    if(controladores==2){
      $('#textoPD').hide();
      $('#textoPID').hide();
      $('#textoP').hide();
      $('#textoPI').show();
    }
    if(controladores==1){
      $('#textoPI').hide();
      $('#textoPID').hide();
      $('#textoPD').hide();
      $('#textoP').show();
    }
}

$('#botao2').on('click', enviarDados2);