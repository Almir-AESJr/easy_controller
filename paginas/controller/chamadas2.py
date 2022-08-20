from django.http import JsonResponse
from control.matlab import*
import numpy as np
import sys
import json
import chamadas
from re import I
from typing import Container
import control
import numpy as np
from control.matlab import *
from scipy import signal
import json
import numpy
from unittest.mock import MagicMixin
from re import I
from typing import Container
from unittest.mock import MagicMixin
import control
from control.matlab.timeresp import step
import numpy as np
from control.matlab import *
from scipy import signal
import json
import numpy

def dadosgrafico2(request):

    zigler = request.GET.get('controladorescalc')
    zigler = int(zigler)
    s = tf('s')

    T = request.GET.get('amostragem')
    T = float(T)

    controladores = request.GET.get('controladores')
    controladores = int(controladores)
    amostragemop = request.GET.get('amostragem1')
    amostragemop = int(amostragemop)
    referencia = request.GET.get('referencia')
    referencia = float(referencia)
    kp = request.GET.get('kp')
    kp = float(kp)
    ti = request.GET.get('ti')
    ti = float(ti)
    td = request.GET.get('td')
    td = float(td)
    saturacao = request.GET.get('saturacao')
    saturacao = float(saturacao)  
    saturacao1 = request.GET.get('saturacao1')
    saturacao1 = float(saturacao1)  
    numerador = request.GET.get('numerador')
    denominador = request.GET.get('denominador')
    denominador = denominador.split(',')
    numerador = numerador.split(',')
    numerador2 = []
    denominador2 = []
    for i in numerador:
        numerador2.append(float(i))
    for i in denominador:
        denominador2.append(float(i))

    sys1 = tf(numerador2,denominador2)
    erro1 = float(0)
    erro2 = float(0)
    erro = float(0)

    if (saturacao1 == 0):
        saturacao = 100000
    
    if(zigler == 2):
        yout, tem = step(sys1)
        dy = np.zeros(len(tem))
        valor2 = 0

        for i in range(0, len(yout)-1):
            dy[i] = (yout[i+1] -yout[i])/(tem[i+1] -tem[i])
            
        for i in range(0, len(dy)):
            if (dy[i]>valor2):
                valor2 = dy[i]
                conta2 = [i]
                        

        tempo_dy = tem[conta2]           
        valor_y  = yout[conta2]            

        b = valor2*tempo_dy -valor_y
        Y = np.zeros(len(tem), dtype=float)
        Y1 = np.zeros(len(tem), dtype=float)

        for i in range(0, len(tem)):      
            Y[i] = valor2*tem[i]-b                    
        valor3 = 10000
        for i in range(0, len(Y)):
            Y1[i] = abs(Y[i])
            if (Y1[i] < valor3):
                valor3 = Y1[i]
                conta3 = [i]

        dentro = 100000

        for i in range(0, len(Y)):
            valor4 = abs(Y[i]-dcgain(sys1))
            if (valor4 < dentro):
                dentro = valor4
                conta4 = [i]

        K = dcgain(sys1)
        L = tem[conta3]
        TE = tem[conta4]-L

        if(controladores == 4):
            kp = 1.2*TE/(K*L)
            ti = 2*L
            td = L/2
            

        if (controladores == 2):
            kp = 0.9*TE/(K*L)
            ti = L/0.3

        if (controladores == 1):
            kp = TE/(K*L)


    # sengundo método
    if(zigler == 3):
        mag, phase, omega = bode(sys1, plot=False)
        #yout, T = step(sys1)
        dentro = 1000
        fase = np.zeros(len(phase), dtype=float)

        for i in range(0, len(phase)):
            fase[i] = phase[i]*(180/3.1415)
        
        for i in range(0, len(phase)):
            valor = (abs(180-abs(fase[i])))
            if (valor < dentro):
                dentro = valor
                conta = [i]

        Kcr = 1/mag[conta]               
        Pcr = 2*3.1415/omega[conta]

        if(controladores == 4):
            kp = 0.6*Kcr
            ti = Pcr/2
            td = Pcr/2

        if (controladores == 2):
            kp = 0.45*Kcr
            ti = Pcr/1.2

        if (controladores == 1):
            kp = Kcr/2
        
    #controlador PID
    if (controladores == 4):
        PID = kp*(1+(1/s*ti)+s*td)
        sys3 = (sys1*PID)/(1+sys1*PID)
        sys3 = control.minreal(sys3)
        d = damp(sys3)
        tau = 10000
        tau0 = 0
        tau1 = 0
        zeta = d[1][0:20]
        wo = d[0][0:20]
        zetawo = zeta*wo

        for i in range(0,len(zetawo)):
            tau0 = 1/zetawo[i]
            if (zetawo[i] !=0) :
                tau0 = 1/zetawo[i]
            if (tau0 > tau1):
                tau1 = tau0
            if (tau0 < tau):
                tau = tau0

        

        tempo = tau1*10

        if (amostragemop == 0):
            T1 = (1/tau) * 200
            T = (2*3.14)/T1

        sys2 = c2d( sys1 , T )

        denominador = sys2.den[0][0][1:20]
        numerador = sys2.num[0][0][0:20]
        ys = np.zeros(len(denominador), dtype=float)
        us = np.zeros(len(numerador), dtype=float)
        r0 = float(kp + kp*(td/T))
        r1 = float((-kp) + (kp*T/ti)-(2*kp*td/T))
        r2 = float(kp*td/T)
        t = np.arange(0, tempo, T)
        y = np.zeros(len(t), dtype=float)
        u = np.zeros(len(t), dtype=float)
        for i in range(1, len(t)):
            for x in range(0,len(denominador)):
                ys[x] = y[i-x-1]
       
            for f in range(0,len(numerador)):
                us[f] = u[i-f-1]
        
            y[i] = (-sum(denominador * ys )) + sum(numerador * us)
            erro = referencia - y[i-1]

            du = (r0*erro) + (r1*erro1) + (r2*erro2)

            u[i] = u[i-1] + du

            if (u[i]>= saturacao):
                u[i]= saturacao
            
            if (u[i]<= 0):
                u[i] = 0
            erro2 = erro1
            erro1 = erro

    # controlador PD
    if (controladores == 3):
        PD = kp*(1+s*td)
        sys3 = (sys1*PD)/(1+sys1*PD)
        d = damp(sys3)
        tau = 10000
        tau0 = 0
        tau1 = 0
        zeta = d[1][0:20]
        wo = d[0][0:20]
        zetawo = zeta*wo
        for i in range(0,len(zetawo)):
            tau0 = 1/zetawo[i]
            if (zetawo[i] !=0) :
                tau0 = 1/zetawo[i]
            if (tau0 > tau1):
                tau1 = tau0
            if (tau0 < tau):
                tau = tau0


        tempo = tau1*10

        if (amostragemop == 0):
            T1 = (1/tau) * 200
            T = (2*3.14)/T1
        sys2 = c2d( sys1 , T )
        denominador = sys2.den[0][0][1:20]
        numerador = sys2.num[0][0][0:20]
        ys = np.zeros(len(denominador), dtype=float)
        us = np.zeros(len(numerador), dtype=float)
        t = np.arange(0, tempo, T)
        y = np.zeros(len(t), dtype=float)
        u = np.zeros(len(t), dtype=float)
        r0 = float(kp*(td +T)/T)
        r1 = float(-kp*td/T)
           
        for i in range(1, len(t)):
            for x in range(0,len(denominador)):
                ys[x] = y[i-x-1]
       
            for f in range(0,len(numerador)):
                us[f] = u[i-f-1]
        
            y[i] = (-sum(denominador * ys )) + sum(numerador * us)
            erro = referencia - y[i-1]
            u[i] = (r0*erro) + (r1*erro1)

            if (u[i]>= saturacao):
                u[i]= saturacao
            
            if (u[i]<= 0):
                u[i] = 0
            erro2 = erro1
            erro1 = erro      
# controlador PI
    if (controladores == 2):
        PI = kp*(1 + 1/(s*ti))
        sys3 = (sys1*PI)/(1+sys1*PI)
        d = damp(sys3)
        tau = 10000
        tau0 = 0
        tau1 = 0
        zeta = d[1][0:20]
        wo = d[0][0:20]
        zetawo = zeta*wo

        for i in range(0,len(zetawo)):
            tau0 = 1/zetawo[i]
            if (zetawo[i] !=0) :
                tau0 = 1/zetawo[i]
            if (tau0 > tau1):
                tau1 = tau0
            if (tau0 < tau):
                tau = tau0

        tempo = tau1*10

        if (amostragemop == 0):
            T1 = (1/tau) * 200
            T = (2*3.14)/T1

        sys2 = c2d( sys1 , T )
        denominador = sys2.den[0][0][1:20]
        numerador = sys2.num[0][0][0:20]
        ys = np.zeros(len(denominador), dtype=float)
        us = np.zeros(len(numerador), dtype=float)
        t = np.arange(0, tempo, T)
        y = np.zeros(len(t), dtype=float)
        u = np.zeros(len(t), dtype=float)
        r0 = float(kp*(ti +T)/ti)
        r1 = float(-kp)
           
        for i in range(1, len(t)):
            for x in range(0,len(denominador)):
                ys[x] = y[i-x-1]
       
            for f in range(0,len(numerador)):
                us[f] = u[i-f-1]
        
            y[i] = (-sum(denominador * ys )) + sum(numerador * us)
            erro = referencia - y[i-1]
            u[i] = u[i-1] + (r0*erro) + (r1*erro1)

            if (u[i]>= saturacao):
                u[i]= saturacao
            
            if (u[i]<= 0):
                u[i] = 0
            erro2 = erro1
            erro1 = erro       
    
    # CONTROLADOR P
    if (controladores == 1):
        P = kp
        sys3 = (sys1*P)/(1+sys1*P)
        d = damp(sys3)
        tau = 10000
        tau0 = 0
        tau1 = 0
        zeta = d[1][0:20]
        wo = d[0][0:20]
        zetawo = zeta*wo

        for i in range(0,len(zetawo)):
            tau0 = 1/zetawo[i]
            if (zetawo[i] !=0) :
                tau0 = 1/zetawo[i]
            if (tau0 > tau1):
                tau1 = tau0
            if (tau0 < tau):
                tau = tau0

        tempo = tau1*10

        if (amostragemop == 0):
            T1 = (1/tau) * 200
            T = (2*3.14)/T1

        sys2 = c2d( sys1 , T )
        denominador = sys2.den[0][0][1:20]
        numerador = sys2.num[0][0][0:20]
        ys = np.zeros(len(denominador), dtype=float)
        us = np.zeros(len(numerador), dtype=float)
        t = np.arange(0, tempo, T)
        y = np.zeros(len(t), dtype=float)
        u = np.zeros(len(t), dtype=float)

        for i in range(1, len(t)):
            for x in range(0,len(denominador)):
                ys[x] = y[i-x-1]
       
            for f in range(0,len(numerador)):
                us[f] = u[i-f-1]
        
            y[i] = (-sum(denominador * ys )) + sum(numerador * us)

            erro = referencia - y[i-1]

            u[i] =  (kp*erro) 

            if (u[i]>= saturacao):
                u[i]= saturacao
            
            if (u[i]<= 0):
                u[i] = 0

            erro2 = erro1
            erro1 = erro   

    y2 = [float(i) for i in y]
    u2 = [float(i) for i in u]
    t2 = [float(i) for i in t]
    
    equacao2 = str(sys3)
    equacao2 = equacao2.split('\n')

    if type(kp) == type(np.zeros([1])):
        kp = kp.tolist()
    if type(td) == type(np.zeros([1])):
        td = td.tolist()
    if type(ti) == type(np.zeros([1])):
        ti = ti.tolist()

    response = {
        "newsaida": y2,
        "newcontrole": u2,
        "newG": equacao2,
        "newtempo": t2,
        "newamostragem": T,
        "newkp": kp,
        "newti": ti,
        "newtd": td,
        "newsaturacao": saturacao,
        "newcontrole1": controladores,
        "newreferencia": referencia
    }

    return JsonResponse(response)