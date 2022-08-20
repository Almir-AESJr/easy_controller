function verifica(value) {


    if (value == 1) {
        kp.disabled = false;
        ti.disabled = true;
        td.disabled = true;
    }
    if (value == 2) {
        kp.disabled = false;
        ti.disabled = false;
        td.disabled = true;
    }
    if (value == 3) {
        kp.disabled = false;
        ti.disabled = true;
        td.disabled = false;
    }
    if (value == 4) {
        kp.disabled = false;
        ti.disabled = false;
        td.disabled = false;
    }
};
function verifica1(value) {

    if (value == 1) {
        saturacao.disabled = false;

    }
    if (value == 0) {
        saturacao.disabled = true;


    }
};
function verifica2(value) {

    if (value == 1) {
        amostragem.disabled = false;

    }
    if (value == 0) {
        amostragem.disabled = true;


    }
};
function verifica3(value) {

    if (value == 1) {
        kp.disabled = false;
        ti.disabled = false;
        td.disabled = false;
        }
        if (value == 2) {
            kp.disabled = true;
            ti.disabled = true;
            td.disabled = true;
        }
        if (value == 3) {
            kp.disabled = true;
            ti.disabled = true;
            td.disabled = true;
        }
        
};
    
    
        
