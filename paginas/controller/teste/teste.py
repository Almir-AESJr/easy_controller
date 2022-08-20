from re import I
from typing import Container
from unittest.mock import MagicMixin
import control
from control.matlab.timeresp import step
import numpy as np
from control.matlab import *
from scipy import signal
import matplotlib.pyplot as plt
import json
import numpy

sys1 = tf([2], [1,4,6,4,1])
yout, tem = step(sys1)
dy1 = np.zeros(len(yout))
dy2 = np.zeros(len(tem))
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
T = tem[conta4]-L

kp = 1.2*T/(K*L)
Ti = 2*L
Td = L/2

print(kp)
print(Ti)
print(Td)
