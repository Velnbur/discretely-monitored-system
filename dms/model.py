import numpy as np
import sympy as s

T = 5
A, B = 0, 20
C, D = 0, 20

L0 = 5
xi_0 = np.linspace(A, B, num=L0)  # t=0
ti_0 = np.zeros(L0)
x2i_0 = np.linspace(C, D, num=L0)

Lg = 3
xi_g = np.linspace(A, B, num=Lg)
ti_g = np.linspace(0, T, num=Lg)
x2i_g = np.linspace(C, D, num=Lg)

M0 = 3
xi_m0 = [1, 2, 5]
ti_m0 = [0, -20, -2]
x2i_m0 = [1.5, 2, 4]

Mg = 5
xi_mg = [10, 20, 5, 6, 7]
ti_mg = [1, 3, 10, 5, 0]
x2i_mg = [5, 11, 2, 6.5, 7]

x, x2, t = s.symbols("x x2 t")
x_, x2_, t_ = s.symbols("x_ x2_ t_")

g = (1 / (-2 * s.pi)) * s.log(1 / s.sqrt((x - x_) ** 2 + (t - t_) ** 2))  # G(x,t,x_,t_)
y = 5 * s.sin(x / 5) + 4 * s.cos(t / 4)
u = -0.2 * s.sin(x / 5) - 0.25 * s.cos(t / 4)

y_xt = s.lambdify([x, t], y)
u_xt = s.lambdify([x, t], u)
G = s.lambdify([x, t, x_, t_], g)


def get_initial_conditions():  # t=0
    Yi_0 = [y_xt(xi_0[i], 0) for i in range(L0)]
    return Yi_0


print(get_initial_conditions())


def get_boundary_conditions():
    Yi_g = [y_xt(xi_g[i], ti_g[i]) for i in range(Lg)]
    return Yi_g


print(get_boundary_conditions())


def y_inf(x, t):
    f = lambda z, y: G(x, t, y, z) * u_xt(y, z)
    # res = scipy.integrate.dblquad(f, 0, self.T, self.A, self.B)[0]
    n = 7
    h_x = (B - A) / n
    h_t = (T - 0) / n
    x = np.linspace(A, B, n + 1)
    t = np.linspace(0, T, n + 1)
    res = (
        h_x
        * h_t
        * np.sum(
            [
                np.sum([f(x[i] - h_x / 2, t[j] - h_t / 2) for i in range(1, n + 1)])
                for j in range(1, n + 1)
            ]
        )
    )
    return res


def Y():
    Yi_0 = get_initial_conditions()
    Yi_g = get_boundary_conditions()
    Y_0 = np.array([[Yi_0[i] - y_inf(xi_0[i], 0)] for i in range(L0)])
    Y_g = np.array([[Yi_g[i] - y_inf(xi_g[i], ti_g[i])] for i in range(Lg)])
    res = np.block([[Y_0], [Y_g]])
    return res


def A_matrix():
    A_11 = np.array(
        [[G(xi_0[j], 0, xi_m0[i], ti_m0[i]) for i in range(M0)] for j in range(L0)]
    )
    A_12 = np.array(
        [[G(xi_0[j], 0, xi_mg[i], ti_mg[i]) for i in range(Mg)] for j in range(L0)]
    )
    A_21 = np.array(
        [
            [G(xi_g[j], ti_g[j], xi_m0[i], ti_m0[i]) for i in range(M0)]
            for j in range(Lg)
        ]
    )
    A_22 = np.array(
        [
            [G(xi_g[j], ti_g[j], xi_mg[i], ti_mg[i]) for i in range(Mg)]
            for j in range(Lg)
        ]
    )
    res = np.block([[A_11, A_12], [A_21, A_22]])
    return res


nu = np.ones((M0 + Mg, 1))

A_matrix_ins = A_matrix()
print(f"A={A_matrix_ins}")
pinv_A_matrix = np.linalg.pinv(A_matrix_ins)

Y_vec = Y()
print(f"{Y_vec=}")

u = np.dot(pinv_A_matrix, (Y_vec - np.dot(A_matrix_ins, nu))) + nu
print(f"{u=}")

assert np.allclose(A_matrix @ u, Y_vec)
