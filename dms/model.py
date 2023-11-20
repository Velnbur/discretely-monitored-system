from dataclasses import dataclass, field
from typing import Callable, List, TypeAlias, Union

import numpy as np
import numpy.typing as npt
import sympy as s
from sympy.parsing.sympy_parser import parse_expr


@dataclass
class ModelConfig:
    T: float = 5  # end of the monitored time interval [0,T]
    A: float = 0  # left boundary of the monitored space interval [A,B]
    B: float = 20  # right boundary of the monitored space interval [A,B]
    C: float = 0  # left boundary of the monitored space interval [C,D]
    D: float = 20  # right boundary of the monitored space interval [C,D]

    L0: int = 5  # number of points on the initial space and time intervals
    Lg: int = 3  # number of points on the boundary space and time intervals

    M0: int = 3  # number of points on the initial space and time intervals
    Mg: int = 5  # number of points on the boundary space and time intervals

    xi_m0: List[float] = field(
        default_factory=lambda: [1.0, 2.0, 5.0]
    )  # initial space points of the monitored points
    ti_m0: List[float] = field(
        default_factory=lambda: [
            0.0,
            -20.0,
            -2.0,
        ]
    )  # initial time points of the monitored points

    xi_mg: List[float] = field(
        default_factory=lambda: [
            10.0,
            20.0,
            5.0,
            6.0,
            7.0,
        ]
    )  # boundary space points of the monitored points
    ti_mg: List[float] = field(
        default_factory=lambda: [
            1.0,
            3.0,
            10.0,
            5.0,
            0.0,
        ]
    )  # boundary time points of the monitored points

    g: str = (
        "(1 / (-2 * pi)) * log(1 / sqrt((x - x_) ** 2 + (t - t_) ** 2))"  # G(x,t,x_,t_)
    )
    y: str = "5 * sin(x / 5) + 4 * cos(t / 4)"  # monitored function
    u: str = "-0.2 * sin(x / 5) - 0.25 * cos(t / 4)"  # control function


ArrayOrFloat: TypeAlias = Union[float, npt.ArrayLike]


class MonitoredModel:
    config: ModelConfig

    G: Callable[
        [ArrayOrFloat, ArrayOrFloat, float, float],
        float,
    ]
    y_xt: Callable[[float, float], float]
    u_xt: Callable[[float, float], float]

    def __init__(self, config: ModelConfig) -> None:
        self.xi_0 = np.linspace(config.A, config.B, num=config.L0)  # t=0
        self.ti_0 = np.zeros(config.L0)
        self.x2i_0 = np.linspace(config.C, config.D, num=config.L0)

        self.xi_g = np.linspace(config.A, config.B, num=config.Lg)
        self.ti_g = np.linspace(0, config.T, num=config.Lg)
        self.x2i_g = np.linspace(config.C, config.D, num=config.Lg)

        self.config = config

        x, t = s.symbols("x t")
        x_, t_ = s.symbols("x_ t_")

        g = parse_expr(config.g)
        y = parse_expr(config.y)
        u = parse_expr(config.u)

        self.G = s.lambdify([x, t, x_, t_], g)
        self.y_xt = s.lambdify([x, t], y)
        self.u_xt = s.lambdify([x, t], u)

    def solve(self) -> npt.ArrayLike:
        nu = np.ones((self.config.M0 + self.config.Mg, 1))

        A_matrix = self._A_matrix()
        A_matrix_inv = np.linalg.pinv(A_matrix)

        Y_vec = self._Y()

        u = np.dot(A_matrix_inv, (Y_vec - np.dot(A_matrix, nu))) + nu

        assert np.allclose(A_matrix @ u, Y_vec)

        return u

    def _get_initial_conditions(self):
        Yi_0 = [self.y_xt(self.xi_0[i], 0) for i in range(self.config.L0)]
        return Yi_0

    def _get_boundary_conditions(self):
        Yi_g = [self.y_xt(self.xi_g[i], self.ti_g[i]) for i in range(self.config.Lg)]
        return Yi_g

    def _y_inf(self, x: npt.ArrayLike, t: npt.ArrayLike) -> float:
        """
        :param x: array of x values
        :param t: array of t values
        :return: Value of the integral:

        .. math::
            \\int_{0}^{T} \\int_{A}^{B} G(x,t,y,z) u(y,z) dy dz
        """

        f = lambda x_, t_: self.G(x, t, t_, x_) * self.u_xt(t_, x_)

        # TODO(Velnbur): may be, we should use scipy.integrate.dblquad
        # res = scipy.integrate.dblquad(f, 0, self.T, self.A, self.B)[0] instead of this

        n = 7
        h_x = (self.config.B - self.config.A) / n
        h_t = (self.config.T - 0) / n
        x = np.linspace(self.config.A, self.config.B, n + 1)
        t = np.linspace(0, self.config.T, n + 1)

        return (
            h_x
            * h_t
            * np.sum(
                [
                    np.sum([f(x[i] - h_x / 2, t[j] - h_t / 2) for i in range(1, n + 1)])
                    for j in range(1, n + 1)
                ]
            )
        )

    def _Y(self) -> npt.ArrayLike:
        """
        Calculate Y vector of monitored system to solve the linear system of
        equations to find subvectors u_inf, u_G.

        :return: Y vector
        """

        Yi_0 = self._get_initial_conditions()
        Yi_g = self._get_boundary_conditions()
        Y_0 = np.array(
            [[Yi_0[i] - self._y_inf(self.xi_0[i], 0)] for i in range(self.config.L0)]
        )
        Y_g = np.array(
            [
                [Yi_g[i] - self._y_inf(self.xi_g[i], self.ti_g[i])]
                for i in range(self.config.Lg)
            ]
        )

        return np.block([[Y_0], [Y_g]])

    def _A_matrix(self) -> npt.NDArray:
        """
        Calculate matrix A of the system
        """

        A_11 = np.array(
            [
                [
                    self.G(self.xi_0[j], 0, self.config.xi_m0[i], self.config.ti_m0[i])
                    for i in range(self.config.M0)
                ]
                for j in range(self.config.L0)
            ]
        )
        A_12 = np.array(
            [
                [
                    self.G(self.xi_0[j], 0, self.config.xi_mg[i], self.config.ti_mg[i])
                    for i in range(self.config.Mg)
                ]
                for j in range(self.config.L0)
            ]
        )
        A_21 = np.array(
            [
                [
                    self.G(
                        self.xi_g[j],
                        self.ti_g[j],
                        self.config.xi_m0[i],
                        self.config.ti_m0[i],
                    )
                    for i in range(self.config.M0)
                ]
                for j in range(self.config.Lg)
            ]
        )
        A_22 = np.array(
            [
                [
                    self.G(
                        self.xi_g[j],
                        self.ti_g[j],
                        self.config.xi_mg[i],
                        self.config.ti_mg[i],
                    )
                    for i in range(self.config.Mg)
                ]
                for j in range(self.config.Lg)
            ]
        )

        return np.block([[A_11, A_12], [A_21, A_22]])


if __name__ == "__main__":
    config = ModelConfig()

    model = MonitoredModel(config)

    u = model.solve()

    print(u)