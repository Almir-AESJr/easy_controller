from email import header
from http.client import HTTPResponse
from turtle import shape, st
from urllib import response

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render

import control
import control.matlab as conmat
import logging
import json
import numpy as np
from decimal import *
import collections.abc
import scipy

class Inicio(TemplateView):
    template_name = "templates/inicio.html"

def HomeView(request):
    return render(request, 'templates/home.html', {})

def IndexView(request):
    return render(request, 'templates/index.html', {})

def CadastroView(request):
    return render(request, 'templates/cadastro.html', {})

def SobreView(request):
    return render(request, 'templates/sobre.html', {})

def TutorialView(request):
    return render(request, 'templates/tutorial.html', {})

"""---------------Controlador LQR---------------"""

@method_decorator(csrf_exempt, name='dispatch')
class EasyControllerLqr(View):
    logging.basicConfig(level=logging.DEBUG)

    def options(self, request, *args, **kwargs):
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Allow-Headers': '*'
        }
        return JsonResponse({}, status=200, safe=True, headers=headers)

    def post(self, request):
        class NumpyArrayEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, np.ndarray):
                    return obj.tolist()
                return json.JSONEncoder.default(self, obj)

        data = json.loads(request.body)
        matrizQ = np.array(data.get('Q'), dtype=float)
        matrizR = np.array(data.get('R'), dtype=float)
        matrizA = np.array(data.get('A'), dtype=float)
        matrizB = np.array(data.get('B'), dtype=float)
        matrizC = np.array(data.get('C'), dtype=float)
        matrizD = np.array(data.get('D'), dtype=float)
        ci = np.array(data.get('CI'), dtype=float)

        # if np.size(matrizB, 1) > 1:
        #     Dhat = np.concatenate((matrizD, np.zeros((1, np.size(matrizB, 1) - 1))), axis=1)
        # else:
        #     Dhat = matrizD

        if np.size(matrizB, 1) > 1 or np.size(matrizC, 0) > 1:
            # Dhat = np.zeros((1, np.size(matrizB, 1) - 1))
            Dhat = np.zeros((np.size(matrizC, 0), np.size(matrizB, 1)))
        else:
            Dhat = matrizD

        [K, S, E] = control.lqr(matrizA, matrizB, matrizQ, matrizR)
        print(f'----------K {K}')
        auto_val = np.linalg.eigvals(matrizA - matrizB * K)
        print(f'auto_val: {auto_val}, dim: {np.shape(auto_val)}')
        min_auto = min(abs(auto_val))
        print(f'min_auto: {min_auto}')
        max_auto = max(abs(auto_val))
        print(f'max_auto: {max_auto}')
        constMax = (max_auto/min_auto)
        print(f'constMax//: {constMax}')
        T = ((2 * np.pi)/(1000 * min_auto))
        if max_auto == min_auto:
            constMax = constMax * 2
        Tmax = np.floor(((2 * np.pi)/(max_auto)) * (constMax))
        print(f'Tmax: {Tmax}')
        
        # if Tmax < 10:
        #     Tmax = 10
        t = np.arange(0, Tmax + T, T)
        print(f't: {len(t)}')

        Ni = len(t)
        Nx = len(matrizA)
        Nu = np.size(matrizB, 1)
        Ny = np.size(matrizC, 0)

        u = np.zeros((Nu, Nx))
        if Nx == 2:
            x = (ci).T * np.ones((Nx, Nx))
        else:
            x = (ci) * np.ones((Nx, Nx))
        print(f'x inicial: {x}, dim: {np.shape(x)}')
        print(f'CI: {ci}, dim: {np.shape(ci)}')
        y = np.zeros((Ny, Nu))

        for k in range(Nx, Ni):
            
            dx = matrizA @ np.transpose([x[:, k - 1]]) + matrizB @ np.transpose([u[:, k - 1]])
            # print(f'dx: {dx}, dim: {np.shape(dx)}')
            dx = np.reshape(dx, (Nx, 1))
            x_linha = np.transpose([x[:, k - 1]]) + dx * T
            # print(f'x_linha: {x_linha}, dim: {np.shape(x_linha)}')
            x_linha = np.reshape(x_linha, (Nx, 1))
            x = np.concatenate((x, x_linha), axis=1)            
            # y = np.array([np.concatenate((y, matrizC @ np.transpose([x[:, k]])), axis=None)])
            y = np.concatenate((y, matrizC @ np.transpose([x[:, k]])), axis=1)
            # logging.info('y %s, dim %s', y, np.shape(y))
            u_linhaA = np.transpose([x[:, k - 1]])
            # logging.info('u_linhaA %s, dim %s', u_linhaA, np.shape(u_linhaA))
            u_linhaA = np.reshape(u_linhaA, (Nx, 1))
            # logging.info('u_linhaA %s, dim %s', u_linhaA, np.shape(u_linhaA))
            u_linha = - K * u_linhaA
            # logging.info('u_linha %s, dim %s', u_linha, np.shape(u_linha))
            u = np.concatenate((u, u_linha), axis=1)
            # logging.info('u %s, dim %s', u, np.shape(u))

        # logging.info('u %s, dim %s', u, np.shape(u))
        # logging.info('y >> %s,  dim %s', y, np.shape(y))
        yRavel = np.ravel(y)
        # logging.info('yRavel >> %s,  dim %s', yRavel, np.shape(yRavel))
        ySplit = np.split(yRavel, Ny)
        # logging.info('ySplit >> %s,  dim %s', ySplit, np.shape(ySplit))

        encodeY = json.dumps(ySplit, cls=NumpyArrayEncoder)
        encodeU = json.dumps(u, cls=NumpyArrayEncoder)
        encodeK = json.dumps(K, cls=NumpyArrayEncoder)
        encodeNx = json.dumps(Nx, cls=NumpyArrayEncoder)
        encodeNu = json.dumps(Nu, cls=NumpyArrayEncoder)
        encodeNy = json.dumps(Ny, cls=NumpyArrayEncoder)
        encodeT = json.dumps(T, cls=NumpyArrayEncoder)
            
        # logging.info('u %s, dim %s', u, np.shape(u))
        # logging.info('dx %s, dim %s', dx, np.shape(dx))
        # logging.info('x_linha %s', x_linha)
        # logging.info('x %s, dim %s', x, np.shape(x))
        # logging.info('y %s, dim %s', y, np.shape(y))

        reponse = {
            "Yout": encodeY,
            "time": t.tolist(),
            "Uhat": encodeU,
            "K": encodeK,
            "Nx": encodeNx,
            "Nu": encodeNu,
            "Ny": encodeNy,
            "T": encodeT,
        }

        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Allow-Headers': '*'
        }
        response = JsonResponse(reponse, status=201, safe=True, headers=headers)
        return response

"""---------------Controlador LQI---------------"""

@method_decorator(csrf_exempt, name='dispatch')
class EasyControllerLqi(View):
    logging.basicConfig(level=logging.DEBUG)

    def options(self, request, *args, **kwargs):
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Allow-Headers': '*'
        }
        return JsonResponse({}, status=200, safe=True, headers=headers)

    def post(self, request):
        class NumpyArrayEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, np.ndarray):
                    return obj.tolist()
                elif isinstance(obj, np.integer):
                    return int(obj)
                return json.JSONEncoder.default(self, obj)

        data = json.loads(request.body)
        matrizQ = np.array(data.get('Q'), dtype=float)
        matrizR = np.array(data.get('R'), dtype=float)
        matrizA = np.array(data.get('A'), dtype=float)
        matrizB = np.array(data.get('B'), dtype=float)
        matrizC = np.array(data.get('C'), dtype=float)
        matrizD = np.array(data.get('D'), dtype=float)
        ci = np.array(data.get('CI'), dtype=float)

        
        # Ahat = np.concatenate(((np.concatenate((matrizA, np.zeros((np.size(matrizA, 0), 1))), axis=1)), (
        #     np.concatenate((-matrizC, np.zeros((np.size(matrizC, 0), 1))), axis=1))), axis=0)
        Ahat = np.concatenate(((np.concatenate((matrizA, np.zeros((np.size(matrizA, 0), np.size(matrizC, 0)))), axis=1)), (
            np.concatenate((-matrizC, np.zeros((np.size(matrizC, 0), np.size(matrizC, 0)))), axis=1))), axis=0)
        logging.info('Dados Ahat >> %s', Ahat)
        Bhat = np.concatenate((matrizB, np.zeros((np.size(matrizC, 0), np.size(matrizB, 1)))), axis=0)
        logging.info('Dados Bhat >> %s', Bhat)
        Chat = np.concatenate((matrizC, np.zeros((np.size(matrizC, 0), 3))), axis=1)
        logging.info('Dados Chat >> %s', Chat)
        logging.info('Dados matrizC >> %s', matrizC)
        logging.info('Dados matrizQ >> %s', matrizQ)
        logging.info('Dados matrizR >> %s', matrizR)

        if np.size(matrizB, 1) > 1:
            Dhat = np.zeros((np.size(Chat, 0), np.size(Bhat, 1)))
        else:
            Dhat = matrizD        


        logging.info('Dados Dhat >> %s', Dhat)
        Nx = len(matrizA)
        print(f'----------Nx: {Nx}, dim: {np.shape(Nx)}')
        Nu = np.size(matrizB, 1)
        Ny = np.size(matrizC, 0)

        # q = np.eye(9)
        # r = np.eye(2)*1000
        # logging.info('Dados matrizQ >> %s, %s', q, r)
        # ia = np.zeros((1,Nx))
        # [Kf, Sf, Ef] = conmat.lqr(matrizA, matrizB, q, r, integral_action=ia)
        # print(f'-----Kf {Kf}')
        # a = np.array([[0, 1.0000, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, -9.8000, 0, 0, 0, 0], [0, 0, 0, 1.0000, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0,
        #              0, 1.0000, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [-1.0000, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, -1.0000, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, -1.0000, 0, 0, 0, 0]])
        [Ke, S, E] = control.lqr(Ahat, Bhat, matrizQ, matrizR)
        print(f'Ke {Ke}')
        Ki = Ke[0:Nu, Nx:Nx+Ny]
        print(f'Ki {Ki}')
        K = Ke[:, 0:Nx]
        print(f'K {K}')

        auto_val = np.linalg.eigvals(matrizA - (matrizB @ K))
        print(f'----------auto_val: {auto_val}, dim: {np.shape(auto_val)}')
        min_auto = min(abs(auto_val))
        print(f'min_auto {min_auto}')
        max_auto = max(abs(auto_val))
        print(f'max_auto {max_auto}')
        T = ((2 * np.pi)/(1000 * min_auto))
        constMax = (max_auto/min_auto)
        print(f'constMax//: {constMax}')
        
        if constMax < max_auto/2:
            constMax = (max_auto/min_auto)*2
        elif constMax > 5 * max_auto:
            constMax = (max_auto/min_auto)*1.5
            
        if max_auto == min_auto:
            constMax = constMax * 4
        print(f'constMax//: {constMax}')
        Tmax = np.floor(((2 * np.pi)/(max_auto)) * (constMax))
        print(f'Tmax//: {Tmax}')
        t = np.arange(0, Tmax + T, T)

        Ni = len(t)
        print(f'----------Ni: {Ni}, dim: {np.shape(Ni)}')
        Nx = len(matrizA)
        print(f'----------Nx: {Nx}, dim: {np.shape(Nx)}') 
        Nu = np.size(matrizB, 1)
        Ny = np.size(matrizC, 0)

        u = np.zeros((Nu, Nx))
        x = (ci) * np.ones((Nx, Nx))
        print(f'x inicial {x}')
        # xhat = np.zeros((Nx, Nx))
        # ref_drone = np.array([[1, 1, 1], [0.5, 1, 1], [0, 1, 1]])
        # ref = ref_drone @ np.ones((Ny, Ni))
        ref = np.ones((Ny, Ni))
        print(f'ref: {ref}')
        y = np.zeros((Ny, Nx))
        int_e = 0

        # sys = control.StateSpace(matrizA, matrizB, matrizC, Dhat)

        if Nu == Ny:
            Ki = Ki.T

        for k in range(Nx, Ni):
            
            # print(f'----------k: {k}, dim: {np.shape(k)}') 
            dx = matrizA @ np.transpose([x[:, k - 1]]) + matrizB @ np.transpose([u[:, k - 1]])
            # print(f'----------dx: {dx}, dim: {np.shape(dx)}')          
            dx = np.reshape(dx, (Nx, 1))            
            x_linha = np.transpose([x[:, k - 1]]) + dx * T
            # print(f'----------x_linha: {x_linha}, dim: {np.shape(x_linha)}')
            x_linha = np.reshape(x_linha, (Nx, 1))
            # print(f'dx: {dx}, dim: {np.shape(dx)}')
            x = np.concatenate((x, x_linha), axis=1)
            # print(f'----------x: {x}, dim: {np.shape(x)}')
            y = np.concatenate((y, matrizC @ np.transpose([x[:, k]])), axis=1)
            # print(f'----------y: {y}, dim: {np.shape(y)}')
            # print(f'----------ref: {ref}, dim: {np.shape(ref)}') 

            e = np.transpose([ref[:, k - 1] - y[:, k - 1]])
            # print(f'e: {e}, dim: {np.shape(e)}')
            int_e = int_e + e * T
            # print(f'int_e: {int_e}, dim: {np.shape(int_e)}')
            u_linhaA = np.transpose([x[:, k - 1]])
            # u_linhaA = np.reshape(u_linhaA, (2, 1))
            # logging.info('u_linhaA %s, dim %s', u_linhaA, np.shape(u_linhaA))
            u_linha = - K * u_linhaA - Ki * int_e
            # logging.info('u_linha %s, dim %s', u_linha, np.shape(u_linha))
            # logging.info('u %s, dim %s', u, np.shape(u))
            u = np.concatenate((u, u_linha), axis=1)
            # logging.info('u %s, dim %s', u, np.shape(u))

        yRavel = np.ravel(y)
        # logging.info('yRavel >> %s', yRavel)
        ySplit = np.split(yRavel, Ny)
        # logging.info('ySplit %s, dim %s', ySplit, np.shape(ySplit))           
        
        # x_LQI = np.split(xRavel, 2 * cols)
        # logging.info('XSLQI >> %s', x_LQI)

        # logging.info('int_e %s, dim %s', int_e, np.shape(int_e))
        # logging.info('u %s, dim %s', u, np.shape(u))
        # # logging.info('dx %s, dim %s', dx, np.shape(dx))
        # logging.info('x_linha %s', x_linha)
        # logging.info('x %s', x)
        # logging.info('y %s, dim %s', y, np.shape(y))

        encodeY = json.dumps(ySplit, cls=NumpyArrayEncoder)
        encodeU = json.dumps(u, cls=NumpyArrayEncoder)



        #         ssResponseLQI = control.StateSpace(Ahat - Bhat * K, Bhat_cols[n], c, matrizD)
        #         logging.info('cols >> %s, StateSpace >> %s', n, ssResponseLQI)

        #         [wn, zeta, poles] = control.damp(ssResponseLQI)
        #         logging.info('wn >> %s, zeta >> %s', wn, zeta)
        #         for i in wn:
        #             timeconst = 1/(zeta*wn)
        #             timeconst = np.ceil(timeconst)
        #         logging.info('timeconst %s', timeconst)
        #         timeSimLQI = 5 * max(timeconst)
        #         timeLQI = np.arange(0, timeSimLQI + .05, .05, dtype=float)
        #         logging.info('time %s, size_time %s', timeLQI, len(timeLQI))

        #         out_yLQI, timeLQI, out_xLQI = conmat.lsim(ssResponseLQI, 1, timeLQI)
        #         logging.info('out_xLQI >> %s', out_xLQI)
        #         logging.info('out_yLQI >> %s', out_yLQI)

        #         stepYLQI = []
        #         for i in out_yLQI:
        #             if isinstance(i, collections.abc.Sequence):
        #                 stepYLQI.append(float("{:.4f}".format(i[0])))
        #             else:
        #                 stepYLQI.append(float("{:.4f}".format(i)))

        #         outY_totalLQI.append(stepYLQI)
        #     # logging.info('Y_TOTAL >> %s', outY_totalLQI)
        #     # logging.info('stepYLQR >> %s', stepYLQI)

        #     stepXLQI.append(out_xLQI)
        #     logging.info('stepXLQR >> %s', stepXLQI)

        # for i in range(0, cols):
        #     transp_x_LQI = -K * stepXLQI[i].transpose()
        #     logging.info('stepXLQI >> %s', stepXLQI[i])
        #     logging.info('transp_XLQI >> %s', transp_x_LQI)
        #     control_sig.append(transp_x_LQI)
        # logging.info('control_sig >> %s', control_sig)

        # xRavel = np.ravel(control_sig)
        # logging.info('XL >> %s', xRavel)

        # if cols > 1:
        #     x_LQI = np.split(xRavel, 2 * cols)
        #     logging.info('XSLQI >> %s', x_LQI)
        # else:
        #     x_LQI = np.split(xRavel, cols)
        #     logging.info('XSLQI >> %s', x_LQI)

        # encodeLQIresponse = json.dumps(x_LQI, cls=NumpyArrayEncoder)
        # logging.info('encode %s', encodeLQIresponse)

        encodeK = json.dumps(K, cls=NumpyArrayEncoder)
        encodeKi = json.dumps(Ki, cls=NumpyArrayEncoder)
        encodeNx = json.dumps(Nx, cls=NumpyArrayEncoder)
        encodeNu = json.dumps(Nu, cls=NumpyArrayEncoder)
        encodeNy = json.dumps(Ny, cls=NumpyArrayEncoder)
        encodeT = json.dumps(T, cls=NumpyArrayEncoder)
            

        reponse = {
            "Yout": encodeY,
            "time": t.tolist(),
            "Uhat": encodeU,
            "K": encodeK,
            "Ki": encodeKi,
            "Nx": encodeNx,
            "Nu": encodeNu,
            "Ny": encodeNy,
            "T": encodeT,
        }

        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Allow-Headers': '*'
        }
        response = JsonResponse(reponse, status=201,
                                safe=True, headers=headers)
        return response


"""---------------Controlador LQG---------------"""

@method_decorator(csrf_exempt, name='dispatch')
class EasyControllerLqg(View):
    logging.basicConfig(level=logging.DEBUG)

    def options(self, request, *args, **kwargs):
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Allow-Headers': '*'
        }
        return JsonResponse({}, status=200, safe=True, headers=headers)

    def post(self, request):
        class NumpyArrayEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, np.ndarray):
                    return obj.tolist()
                elif isinstance(obj, np.integer):
                    return int(obj)
                return json.JSONEncoder.default(self, obj)

        data = json.loads(request.body)
        matrizQ = np.array(data.get('Q'), dtype=float)
        matrizR = np.array(data.get('R'), dtype=float)
        matrizQN = np.array(data.get('QN'), dtype=float)
        matrizRN = np.array(data.get('RN'), dtype=float)
        matrizA = np.array(data.get('A'), dtype=float)
        matrizB = np.array(data.get('B'), dtype=float)
        matrizC = np.array(data.get('C'), dtype=float)
        matrizD = np.array(data.get('D'), dtype=float)
        ci = np.array(data.get('CI'), dtype=float)
        logging.info('Initial condition >> %s', ci)
        # logging.info('Dados das matrizRN >> %s', matrizRN)
        
        if np.size(matrizB, 1) or np.size(matrizC, 0) > 1:
            Dhat = np.zeros((np.size(matrizC, 0), np.size(matrizB, 1)))
        else:
            Dhat = matrizD
            
        
        [K, S, E] = control.lqr(matrizA, matrizB, matrizQ, matrizR)
        print(f'-----K: {K}')

        auto_val = np.linalg.eigvals(matrizA - matrizB * K)
        min_auto = min(abs(auto_val))
        max_auto = max(abs(auto_val))
        T = ((2 * np.pi)/(1000 * min_auto))
        constMax = (max_auto/min_auto)
        if max_auto == min_auto:
            constMax = constMax * 4
        print(f'constMax//: {constMax}')
        Tmax = np.floor(((2 * np.pi)/(max_auto)) * (constMax))
        # Tmax = ((2 * np.pi)/(max_auto)) * 4
        t = np.arange(0, Tmax + T, T)

        Ni = len(t)
        Nx = len(matrizA)
        Nu = np.size(matrizB, 1)
        Ny = np.size(matrizC, 0)

        u = np.zeros((Nu, Nx))
        if Nx == 2:
            x = np.transpose(ci) * np.ones((Nx, Nx))
        else:
            x = (ci) * np.ones((Nx, Nx))
        print(f'CI: {x}, dim: {np.shape(x)}')
        xhat = np.zeros((Nx, Nx))
        y = np.zeros((Ny, Nx))
        print(f'y: {y}, dim: {np.shape(y)}')
               
        sys = control.StateSpace(matrizA, matrizB, matrizC, Dhat)
        [L, P, EK] = control.lqe(sys, matrizQN, matrizRN)

        for k in range(Nx, Ni):
            
            dx = matrizA @ np.transpose([x[:, k - 1]]) + matrizB @ np.transpose([u[:, k - 1]])
            # print(f'dx: {dx}, dim: {np.shape(dx)}')
            dx = np.reshape(dx, (Nx, 1))
            x_linha = np.transpose([x[:, k - 1]]) + dx * T
            x_linha = np.reshape(x_linha, (Nx, 1))
            x = np.concatenate((x, x_linha), axis=1)            
            # y = np.array([np.concatenate((y, matrizC @ np.transpose([x[:, k]])), axis=None)])
            y = np.concatenate((y, matrizC @ np.transpose([x[:, k]])), axis=1)
            # print(f'----------y: {y}, dim: {np.shape(y)}')

            dx_hatA = np.transpose([xhat[:, k - 1]])
            dx_hatA = np.reshape(dx_hatA, (Nx, 1))
            # logging.info('dx_hatA %s, dim %s', dx_hatA, np.shape(dx_hatA))
            dx_hatB = matrizB @ np.transpose([u[:, k - 1]])
            # logging.info('dx_hatB %s, dim %s', dx_hatB, np.shape(dx_hatB))
            dx_hatB = np.reshape(dx_hatB, (Nx, 1))
            # logging.info('dx_hatB %s, dim %s', dx_hatB, np.shape(dx_hatB))
            dx_hat = (matrizA - L * matrizC) @ dx_hatA + dx_hatB + L * np.transpose([y[:, k-1]])
            # dx_hat = y[:, k]
            # logging.info('----------dx_hat %s, dim %s', dx_hat, np.shape(dx_hat))
            
            xhat_linhaA = np.transpose([xhat[:, k - 1]])
            xhat_linhaA = np.reshape(xhat_linhaA, (Nx, 1))
            xhat_linha =  xhat_linhaA + dx_hat * T
            xhat = np.concatenate((xhat, xhat_linha), axis=1)
            # logging.info('xhat %s, dim %s', xhat, np.shape(xhat))

            u_linhaA = np.transpose([xhat[:, k - 1]])
            u_linhaA = np.reshape(u_linhaA, (Nx, 1))
            # logging.info('u_linhaA %s, dim %s', u_linhaA, np.shape(u_linhaA))
            u_linha = - K * u_linhaA
            # logging.info('u_linha %s, dim %s', u_linha, np.shape(u_linha))
            u = np.concatenate((u, u_linha), axis=1)
            # logging.info('u %s, dim %s', u, np.shape(u))

        logging.info('dx %s, dim %s', dx, np.shape(dx))
        logging.info('x_linha %s', x_linha)
        logging.info('u %s, dim %s', u, np.shape(u))
        logging.info('x %s', x)
        logging.info('y %s, dim %s', y, np.shape(y))


        encodeY = json.dumps(y, cls=NumpyArrayEncoder)
        encodeU = json.dumps(u, cls=NumpyArrayEncoder)
        encodeK = json.dumps(K, cls=NumpyArrayEncoder)
        encodeL = json.dumps(L, cls=NumpyArrayEncoder)
        encodeNx = json.dumps(Nx, cls=NumpyArrayEncoder)
        encodeNu = json.dumps(Nu, cls=NumpyArrayEncoder)
        encodeNy = json.dumps(Ny, cls=NumpyArrayEncoder)
        encodeT = json.dumps(T, cls=NumpyArrayEncoder)

        
        reponse = {
            "Yout": encodeY,
            # "outY_total": outY_totalLQR,
            "time": t.tolist(),
            "Uhat": encodeU,
            "K": encodeK,
            "L": encodeL,
            "Nx": encodeNx,
            "Nu": encodeNu,
            "Ny": encodeNy,
            "T": encodeT,
        }

        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Allow-Headers': '*'
        }
        response = JsonResponse(reponse, status=201,safe=True, headers=headers)
        return response

"""---------------Controlador LQGI---------------"""

@method_decorator(csrf_exempt, name='dispatch')
class EasyControllerLqgi(View):
    logging.basicConfig(level=logging.DEBUG)

    def options(self, request, *args, **kwargs):
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Allow-Headers': '*'
        }
        return JsonResponse({}, status=200, safe=True, headers=headers)

    def post(self, request):
        class NumpyArrayEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, np.ndarray):
                    return obj.tolist()
                elif isinstance(obj, np.integer):
                    return int(obj)
                return json.JSONEncoder.default(self, obj)

        data = json.loads(request.body)
        matrizQ = np.array(data.get('Q'), dtype=float)
        matrizR = np.array(data.get('R'), dtype=float)
        matrizQN = np.array(data.get('QN'), dtype=float)
        matrizRN = np.array(data.get('RN'), dtype=float)
        matrizA = np.array(data.get('A'), dtype=float)
        matrizB = np.array(data.get('B'), dtype=float)
        matrizC = np.array(data.get('C'), dtype=float)
        matrizD = np.array(data.get('D'), dtype=float)
        ci = np.array(data.get('CI'), dtype=float)

        # from scipy.linalg._solvers import xCondToRGain, xSpacing
        # print(f'xCondToRGain {xCondToRGain}, xSpacing {xSpacing}')

        # reponse1 = {
        #     "xCond": xCondToRGain,
        #     "xSpacing": xSpacing,
        # }

        # # headers1 = {
        # #     'Access-Control-Allow-Origin': '*',
        # #     'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
        # #     'Access-Control-Allow-Headers': '*'
        # # }
        # response1 = JsonResponse(reponse1, status=201, safe=True)
        # return response1

        # Ahat = np.concatenate(((np.concatenate((matrizA, np.zeros((np.size(matrizA, 0), 1))), axis=1)), (
        #     np.concatenate((-matrizC, np.zeros((np.size(matrizC, 0), 1))), axis=1))), axis=0)
        Ahat = np.concatenate(((np.concatenate((matrizA, np.zeros((np.size(matrizA, 0), np.size(matrizC, 0)))), axis=1)), (
            np.concatenate((-matrizC, np.zeros((np.size(matrizC, 0), np.size(matrizC, 0)))), axis=1))), axis=0)
        logging.info('Dados Ahat >> %s', Ahat)
        # Bhat = np.concatenate((matrizB, np.zeros((1, np.size(matrizB, 1)))), axis=0)
        Bhat = np.concatenate((matrizB, np.zeros((np.size(matrizC, 0), np.size(matrizB, 1)))), axis=0)
        logging.info('Dados Bhat >> %s', Bhat)
        Chat = np.concatenate((matrizC, np.zeros((np.size(matrizC, 0), 1))), axis=1)

        if np.size(matrizB, 1) > 1 or np.size(matrizC, 0) > 1:
            # Dhat = np.zeros((1, np.size(matrizB, 1) - 1))
            Dhat = np.zeros((np.size(matrizC, 0), np.size(matrizB, 1)))
        else:
            Dhat = matrizD
        print(f'Dhat {Dhat}, dim: {np.shape(Dhat)}')

        Nx = len(matrizA)
        Nu = np.size(matrizB, 1)
        Ny = np.size(matrizC, 0)

        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Allow-Headers': '*'
        }

        try:
            [Ke, S, E] = control.lqr(Ahat, Bhat, matrizQ, matrizR)
        except:
            return JsonResponse({"error": "0001"}, status=400, safe=True, headers=headers)

        print(f'-----K {Ke}')
        Ki = Ke[0:Nu, Nx:Nx+Ny]
        print(f'Ki {Ki}')
        K = Ke[:, 0:Nx]
        print(f'K {K}')

        auto_val = np.linalg.eigvals(matrizA - matrizB @ K)
        min_auto = min(abs(auto_val))
        print(f'min_auto {min_auto}')
        max_auto = max(abs(auto_val))
        print(f'max_auto {max_auto}')
        T = ((2 * np.pi)/(1000 * min_auto))
        constMax = (max_auto/min_auto)

        if constMax <= max_auto/2:
            constMax = (max_auto/min_auto)*2

        elif constMax > 5 * max_auto:
            constMax = (max_auto/min_auto)*1.5

        if max_auto == min_auto:
            constMax = constMax * 4
        print(f'constMax//: {constMax}')
        Tmax = np.floor(((2 * np.pi)/(max_auto)) * (constMax))
        print(f'Tmax {Tmax}')
        # Tmax = ((2 * np.pi)/(max_auto)) * 4
        t = np.arange(0, Tmax + T, T)

        Ni = len(t)
        
        u = np.zeros((Nu, Nx))
        x = np.transpose(ci) * np.ones((Nx, Nx))
        xhat = np.zeros((Nx, Nx))
        ref = np.ones((Ny, Ni))
        # y = np.zeros((Ny, Nu))
        int_e = 0

        y = np.zeros((Ny, Nx))
        logging.info('----------y %s, dim %s', y, np.shape(y))

        if Nu == Ny:
            Ki = Ki.T
        
        sys = control.StateSpace(matrizA, matrizB, matrizC, Dhat)
        [L, P, EK] = control.lqe(sys, matrizQN, matrizRN)
       

        for k in range(Nx, Ni):
            
            dx = matrizA @ np.transpose([x[:, k - 1]]) + matrizB @ np.transpose([u[:, k - 1]])
            # # print(f'dx: {dx}, dim: {np.shape(dx)}')
            dx = np.reshape(dx, (Nx, 1))
            x_linha = np.transpose([x[:, k - 1]]) + dx * T
            # print(f'dx: {dx}, dim: {np.shape(dx)}')
            x_linha = np.reshape(x_linha, (Nx, 1))
            # print(f'dx: {dx}, dim: {np.shape(dx)}')
            x = np.concatenate((x, x_linha), axis=1)
            # print(f'x: {x}, dim: {np.shape(x)}')
            
            # y = np.array([np.concatenate((y, matrizC @ np.transpose([x[:, k]])), axis=None)])
            y = np.concatenate((y, matrizC @ np.transpose([x[:, k]])), axis=1)

            dx_hatA = np.transpose([xhat[:, k - 1]])
            dx_hatA = np.reshape(dx_hatA, (Nx, 1))
            # logging.info('dx_hatA %s, dim %s', dx_hatA, np.shape(dx_hatA))
            dx_hatB = matrizB @ np.transpose([u[:, k - 1]])
            # logging.info('dx_hatB %s, dim %s', dx_hatB, np.shape(dx_hatB))
            dx_hatB = np.reshape(dx_hatB, (Nx, 1))
            # logging.info('dx_hatB %s, dim %s', dx_hatB, np.shape(dx_hatB))
            # dx_hat = (matrizA - L * matrizC) @ dx_hatA + dx_hatB + L * np.transpose([y[:, k]])
            dx_hat = (matrizA - L * matrizC) @ dx_hatA + dx_hatB + L * np.transpose([y[:, k-1]])
            # logging.info('dx_hat %s, dim %s', dx_hat, np.shape(dx_hat))
            
            xhat_linhaA = np.transpose([xhat[:, k - 1]])
            xhat_linhaA = np.reshape(xhat_linhaA, (Nx, 1))
            xhat_linha =  xhat_linhaA + dx_hat * T
            xhat = np.concatenate((xhat, xhat_linha), axis=1)
            # logging.info('xhat %s, dim %s', xhat, np.shape(xhat))

            # e = ref[:, k -1] - y[:, k -1]
            e = np.transpose([ref[:, k - 1] - y[:, k - 1]])                    
            int_e = int_e + e * T
            u_linhaA = np.transpose([xhat[:, k - 1]])
            u_linhaA = np.reshape(u_linhaA, (Nx, 1))
            # logging.info('u_linhaA %s, dim %s',u_linhaA, np.shape(u_linhaA))
            u_linha = - K * u_linhaA - Ki * int_e
            # logging.info('u %s, dim %s', u, np.shape(u))
            u = np.concatenate((u, u_linha), axis=1)
            # logging.info('u %s, dim %s', u, np.shape(u))

        # logging.info('e %s, dim %s', e, np.shape(e))
        # logging.info('int_e %s, dim %s', int_e, np.shape(int_e))
        # logging.info('u %s, dim %s', u, np.shape(u))
        # logging.info('dx %s, dim %s', dx, np.shape(dx))
        # logging.info('x_linha %s', x_linha)
        # logging.info('x %s', x)
        # logging.info('y %s, dim %s', y, np.shape(y))
        # logging.info('dx_hat %s, dim %s', dx_hat, np.shape(dx_hat))
        # logging.info('xhat_linhaA %s, dim %s', xhat_linhaA, np.shape(xhat_linhaA))
        # logging.info('xhat_linha %s, dim %s', xhat_linha, np.shape(xhat_linha))
        # logging.info('xhat %s, dim %s', xhat, np.shape(xhat))

        # from scipy.linalg._solvers import xCondToRGain, xSpacing
        # print(f'xCondToRGain {xCondToRGain}, xSpacing {xSpacing}')

        encodeY = json.dumps(y, cls=NumpyArrayEncoder)
        encodeU = json.dumps(u, cls=NumpyArrayEncoder)
        encodeK = json.dumps(K, cls=NumpyArrayEncoder)
        encodeKi = json.dumps(Ki, cls=NumpyArrayEncoder)
        encodeL = json.dumps(L, cls=NumpyArrayEncoder)
        encodeNx = json.dumps(Nx, cls=NumpyArrayEncoder)
        encodeNu = json.dumps(Nu, cls=NumpyArrayEncoder)
        encodeNy = json.dumps(Ny, cls=NumpyArrayEncoder)
        encodeT = json.dumps(T, cls=NumpyArrayEncoder)

        reponse = {
            "Yout": encodeY,
            "time": t.tolist(),
            "Uhat": encodeU,
            "K": encodeK,
            "Ki": encodeKi,
            "L": encodeL,
            "Nx": encodeNx,
            "Nu": encodeNu,
            "Ny": encodeNy,
            "T": encodeT,

        }

        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Allow-Headers': '*'
        }
        response = JsonResponse(reponse, status=201,safe=True, headers=headers)
        return response

@method_decorator(csrf_exempt, name='dispatch')
class EasyController(View):
    logging.basicConfig(level=logging.DEBUG)

    def options(self, request, *args, **kwargs):
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Allow-Headers': '*'
        }
        return JsonResponse({}, status=200, safe=True, headers=headers)

    def post(self, request):
        data = json.loads(request.body)
        matrizA = np.array(data.get('A'))
        matrizB = np.array(data.get('B'))
        matrizC = np.array(data.get('C'))
        # matrizD = np.array(data.get('D'))
        # matrizD = np.zeros((np.size(matrizC, 0), np.size(matrizB, 1)))
        # if np.size(matrizB, 1) > 1 or np.size(matrizC, 0) > 1:
        #     # Dhat = np.zeros((1, np.size(matrizB, 1) - 1))
        #     matrizD = np.zeros((np.size(matrizC, 0), np.size(matrizB, 1)))
        # else:
        matrizD = np.zeros((1, 1))

        logging.info('Dados das matrizA >> %s', matrizA)
        logging.info('Dados das matrizB >> %s', matrizB)
        logging.info('Dados das matrizC >> %s', matrizC)
        logging.info('Dados das matrizD >> %s', matrizD)

        cols = len(matrizB[0])
        logging.info('cols >> %s', cols)
        matrizB_cols = np.split(matrizB, cols, axis=1)
        logging.info('matrizB_cols >> %s', matrizB_cols)
        outY_total = []

        logging.info('---------------Dinâmica da Planta---------------')

        for n in range (cols):

            logging.info('i >> %s', matrizB_cols[n])

            for c in matrizC:
                logging.info('n >> %s', c)

                ssResponse = control.StateSpace(matrizA, matrizB_cols[n], c, matrizD)
                logging.info('cols >> %s, StateSpace >> %s', n, ssResponse)


                logging.info("----------------------------------------------------------")


                [wn, zeta, poles] = control.damp(ssResponse)
                zeta[zeta != zeta] = 1
                for i in wn:
                    timeconst = 1/(zeta*wn)
                    timeconst = timeconst.round()
                if max(timeconst) == float("inf"):
                    newtimeconst = np.delete(timeconst, np.where(timeconst == float("inf")))
                    print(f'timeconst {newtimeconst}')
                    if len(newtimeconst) == 0:
                        newtimeconst = np.arange(3)
                    timeSim = 5 * max(newtimeconst)
                    print(f'newtimeconst {max(newtimeconst)}')
                else:
                    timeSim = 5 * max(timeconst)
                print(f'timeSim: {timeSim}')
                print(f'zeta: {zeta}')
                print(f'wn: {wn}')
                time = np.arange(0, timeSim, timeSim/200, dtype=float)
                
                out_y, time, out_x = conmat.lsim(ssResponse, 1, time)
                #logging.info('step Y >> %s', out_y)
                #logging.info('step X >> %s', out_x)
                #logging.info('time >> %s', time)

                stepY = []
                for i in out_y:
                    if isinstance(i, collections.abc.Sequence):
                        stepY.append(float("{:.4f}".format(i[0])))
                    else:
                        stepY.append(float("{:.4f}".format(i)))

                #logging.info('Formatted Step Y >> %s', stepY)

                outY_total.append(stepY)
                #logging.info('Y_TOTAL >> %s', outY_total)


        ctrb = conmat.ctrb(matrizA, matrizB)
        control_rank = np.linalg.matrix_rank(ctrb)
        control_rank_result = "O sistema não é controlável"
        if control_rank >= len(matrizA):
            control_rank_result = "O sistema é controlável"

        obsv = conmat.obsv(matrizA, matrizC)
        obsv_rank = np.linalg.matrix_rank(obsv)
        obsv_rank_result = "O sistema não é observável"
        if obsv_rank >= len(matrizA):
            obsv_rank_result = "O sistema é observável"

        reponse = {
            "StateSpace": {
                "A": ssResponse.A.tolist(),
                "B": ssResponse.B.tolist(),
                "C": ssResponse.C.tolist(),
                "D": ssResponse.D.tolist(),
            },
            "stepY": stepY,
            "outY_total": outY_total,
            "time": time.tolist(),
            "control_rank": control_rank_result,
            "obsv_rank": obsv_rank_result
        }
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Allow-Headers': '*'
        }
        response = JsonResponse(reponse, status=201, safe=True, headers=headers)
        return response


