import control
from control.matlab.timeresp import step
import numpy as np
from control.matlab import *
from scipy import signal
import json

def funcao1 (num,den):
    num = [2]
    den = [1, 2, 1]
    sys1 = tf(num, den) 
    yout, T = step(sys1)
    lista = yout[:]
    lista = str(lista)
    ', '.join(lista)
    lista = json.dumps(lista)
    
    
    return lista

