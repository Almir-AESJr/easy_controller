from django.http import JsonResponse
from control.matlab import*
import numpy as np
import sys
import json


def dadosmatriz(request):
    m1 = request.GET.get('m1')
    
   
    """numerador = request.GET.get('matrizA')
    denominador = request.GET.get('denominador'
    denominador = denominador.split(',')
    numerador = numerador.split(',')
    numerador2 = []
    denominador2 = []
    for i in numerador:
        numerador2.append(float(i))
    for i in denominador:
        denominador2.append(float(i))
    #numerador = numerador.replace('"','')
    #denominador = denominador.replace('"','')
    #denominador = denominador.split(',')
    #numerador = numerador.split(',')
    #num = [1]
    #den = [1,2,3]
    sys1 = tf(numerador2, denominador2)
    
   

    equacao = str(sys1)
    equacao = equacao.split('\n')
    #equacao = equacao.split('')
    #equacao = json.dumps(equacao) 
    yout, T = step(sys1)
    lista = yout[:]
    lista2 = []
    T2 = []

    for i in lista:
        lista2.append(i)
    for i in T:
        T2.append(i)
    lista2 = json.dumps(lista2)
    lista2 = lista2.split(',')
    T2 = json.dumps(T2)
    T2 = T2.split(',')
    x = T2
    y = lista2
    
    
    
    response = {

        
        "newY": (y),
        "newX" : (x),
        "newEquacao" : (equacao),
        "newdenominador" : (denominador2),
        "newnumerador" : (numerador2)
        #"newDenominador": float(denominador)*5
        #"newDenominador" :  tf([numerador],[denominador])

    }"""

    return JsonResponse(m1)
