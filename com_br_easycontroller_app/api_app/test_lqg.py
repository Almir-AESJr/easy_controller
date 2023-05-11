import control 
import numpy as np
import matplotlib.pyplot as plt

A = np.array([[0, 1], [-2, -1]])
B = np.array([[1], [0]])
C = np.array([[1, 0]])
D = 0
Q = np.eye(2)
R = np.eye(1)
QK = np.eye(1)
RK = 1

# sys = control.StateSpace(A, B, C, D)
# print(sys)
cols = len(B[0])
matrizB_cols = np.split(B, cols, axis=1)
[K, S, E] = control.lqr(A, B, Q, R)
# [L, P, EK] = control.lqe(sys, QK, RK)

auto_val = np.linalg.eigvals(A - B * K)
# print(auto_val)
min_auto = min(abs(auto_val))
# print(np.pi)
max_auto = max(abs(auto_val))
# print(max_auto)

T = ((2 * np.pi)/(1000 * min_auto))
# print(T)
Tmax = ((2 * np.pi)/(max_auto)) * 4
# print(Tmax)
t = np.arange(0, Tmax + T, T)
# t_linha = t.reshape((1, len(t)))
print(np.shape(t))
Ni = len(t)
# print(Ni)
Nx = len(A)
# print(Nx)
Nu = np.size(B, 1)
# print(Nu)
Nc = np.size(C, 0)
# print(Nc)

u = np.zeros((Nu, Nx))
print(f'u: {u}')
x = np.array([[1], [0]]) * np.ones((Nx, Nx))
# xu = np.transpose([x[:,1]])
print(f'x: {x}')
# print(A * np.split(x, 2, axis=1) + B * np.split(u, 2, axis=1))
xhat = np.zeros((Nx, Nx))
# print(C * (x[:, 1]))
ref = np.ones((Nc, Ni))
# print(np.shape(ref))

# x1 = np.split(x, Nx, axis=1)

outY_totalLQG = []
control_sig = []
y = np.array([[0, 0]])
for n in range(cols):

    for c in C:
        
        sys = control.StateSpace(A, matrizB_cols[n], c, D)
        [L, P, EK] = control.lqe(sys, QK, RK)
        for k in range(Nx , Ni):
            # print(f'matrizB_cols: {matrizB_cols[n]}')
            # print(f'u[:, k - 1]: {np.asarray([u[:, k - 1]]).T}')
            dx = A @ np.transpose([x[:, k - 1]]) + matrizB_cols[n] @ np.asarray([u[:, k - 1]])
            # print(f'dx: {dx}')
            x_linha = np.transpose([x[:, k - 1]]) + dx * T
            # print(f'x_linha: {x_linha}')
            x = np.concatenate((x, x_linha), axis=1)
            # print(f'x: {x}')
            y = np.array([np.concatenate((y, c @ np.transpose([x[:, k]])), axis=None)])
            # print(f'y: {y}')

            dx_hat = (A - L * c) @ np.transpose([xhat[:, k - 1]]) + matrizB_cols[n] * np.transpose([u[:, k - 1]]) + L * y[:, k ]
            # print(f'dx_hat: {dx_hat}')
            xhat_linha = np.transpose([xhat[:, k - 1]]) + dx_hat * T
            # print(f'xhat_linha: {xhat_linha}, dim: {np.shape(xhat_linha)}')
            xhat = np.concatenate((xhat, xhat_linha), axis=1)
            # print(xhat)
            u_linha = - K @ np.transpose([xhat[:, k - 1]])
            # print(u_linha)
            u = np.concatenate((u, u_linha), axis=1)

            
        y_linha = np.ravel(y)
        uhat = np.ravel(u)
        plt.plot(t, y_linha)
        plt.grid(True)
        plt.show()
        plt.plot(t, uhat)
        plt.grid(True)
        plt.show()
print(f'k: {k}')
print(f't: {t}')
# print(f't_linha: {t_linha}')
print(f'dx: {dx}')
print(f'x: {x}')
print(f'y: {y}')
print(f'dx_hat: {dx_hat}')
print(f'x_hat: {xhat}')
print(f'u: {u}')
