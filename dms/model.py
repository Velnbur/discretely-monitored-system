from dataclasses import dataclass, field
from typing import Callable, List, Union, Optional

import numpy as np
import numpy.typing as npt
import sympy as s
from sympy.parsing.sympy_parser import parse_expr


@dataclass
class ModelConfig:
    T: float = 5  # end of the monitored time interval [0,T]
    A: float = 0  # left boundary of the monitored space interval [A,B]
    B: float = 20  # right boundary of the monitored space interval [A,B]
    # C: float = 0  # left boundary of the monitored space interval [C,D]
    # D: float = 20  # right boundary of the monitored space interval [C,D]

    L0: int = 3  # number of points on the initial space and time intervals
    Lg: int = 5  # number of points on the boundary space and time intervals

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


ArrayOrFloat = Union[float, npt.ArrayLike]


class MonitoredModel:
    config: ModelConfig

    G: Callable[
        [ArrayOrFloat, ArrayOrFloat, float, float],
        float,
    ]
<<<<<<< HEAD
    __y_xt: Callable[[float, float], float]
=======
    y_xt: Callable[[float, float], float]
>>>>>>> 06bc119 (Add surface plot for comparison of results)
    __u_xt: Callable[[float, float], float]

    __u: Optional[tuple[npt.ArrayLike, npt.ArrayLike]] = None

    def __init__(self, config: ModelConfig) -> None:
        self.__xi_0 = np.linspace(config.A, config.B, num=config.L0)  # t=0
        self.__ti_0 = np.zeros(config.L0)
        # self.x2i_0 = np.linspace(config.C, config.D, num=config.L0)

        self.__xi_g = np.linspace(config.A, config.B, num=config.Lg)
        self.__ti_g = np.linspace(0, config.T, num=config.Lg)
        # self.x2i_g = np.linspace(config.C, config.D, num=config.Lg)

        self.config = config

        x, t = s.symbols("x t")
        x_, t_ = s.symbols("x_ t_")

        g = parse_expr(config.g)
        y = parse_expr(config.y)
        u = parse_expr(config.u)

        self.G = s.lambdify([x, t, x_, t_], g)
<<<<<<< HEAD
        self.__y_xt = s.lambdify([x, t], y)
=======
        self.y_xt = s.lambdify([x, t], y)
>>>>>>> 06bc119 (Add surface plot for comparison of results)
        self.__u_xt = s.lambdify([x, t], u)

    @property
    def xi_0(self) -> npt.ArrayLike:
        return self.__xi_0

    @property
    def ti_0(self) -> npt.ArrayLike:
        return self.__ti_0

    @property
    def xi_m0(self) -> npt.ArrayLike:
        return self.__xi_0

    @property
    def ti_m0(self) -> npt.ArrayLike:
        return self.__ti_0

    @property
    def xi_mg(self) -> npt.ArrayLike:
        return self.__xi_g

    @property
    def ti_mg(self) -> npt.ArrayLike:
        return self.__ti_g

    def y(self, x: float, t: float) -> float:
<<<<<<< HEAD
        return self.y_inf(x, t) + self._y_0(x, t) + self._y_g(x, t)
=======
        a = self.y_inf(x, t)
        b = self._y_0(x, t)
        c = self._y_g(x, t)

        return a + b + c
>>>>>>> 06bc119 (Add surface plot for comparison of results)

    @property
    def y_0(self) -> npt.ArrayLike:
        return np.array([self._y_0(self.__xi_0[i], 0) for i in range(self.config.L0)])

    @property
    def y_g(self) -> npt.ArrayLike:
        return np.array(
            [self._y_g(self.__xi_g[i], self.__ti_g[i]) for i in range(self.config.Lg)]
        )

    def _y_0(self, x: float, t: float) -> float:
        u_0 = self._u_0()

        return sum(
            [
<<<<<<< HEAD
                self.G(x, t, self.__xi_0[i], self.__ti_0[i]) * u_0[i]
=======
                self.G(x, t, self.config.xi_m0[i], self.config.ti_m0[i]) * u_0[i][0]
>>>>>>> 06bc119 (Add surface plot for comparison of results)
                for i in range(self.config.M0)
            ]
        )

    def _y_g(self, x: float, t: float) -> float:
        u_G = self._u_g()

        assert len(u_G) == self.config.Mg, f"{len(u_G)} != {self.config.Mg}"

        return sum(
            [
<<<<<<< HEAD
                self.G(x, t, self.__xi_g[i], self.__ti_g[i]) * u_G[i]
=======
                self.G(x, t, self.config.xi_mg[i], self.config.ti_mg[i]) * u_G[i][0]
>>>>>>> 06bc119 (Add surface plot for comparison of results)
                for i in range(self.config.Mg)
            ]
        )

    def _u_0(self) -> npt.ArrayLike:
        return self._u()[0]

    def _u_g(self) -> npt.ArrayLike:
        return self._u()[1]

    def _u(self) -> tuple[npt.ArrayLike, npt.ArrayLike]:
        """Find u vector and return u_0, u_G subvectors of it"""

        if self.__u is not None:
            return self.__u

        nu = np.ones((self.config.M0 + self.config.Mg, 1))

        A_matrix = self._A_matrix()
        A_matrix_inv = np.linalg.pinv(A_matrix)

        Y_vec = self._Y()

        u = np.dot(A_matrix_inv, (Y_vec - np.dot(A_matrix, nu))) + nu

        assert np.allclose(A_matrix @ u, Y_vec)

        u_0 = u[: self.config.M0]
        u_G = u[self.config.M0 :]

        self.__u = (u_0, u_G)

        return u_0, u_G

    def _get_initial_conditions(self):
<<<<<<< HEAD
        Yi_0 = [self.__y_xt(self.__xi_0[i], 0) for i in range(self.config.L0)]
=======
        Yi_0 = [self.y_xt(self.__xi_0[i], 0) for i in range(self.config.L0)]
>>>>>>> 06bc119 (Add surface plot for comparison of results)
        return Yi_0

    def _get_boundary_conditions(self):
        Yi_g = [
<<<<<<< HEAD
            self.__y_xt(self.__xi_g[i], self.__ti_g[i]) for i in range(self.config.Lg)
=======
            self.y_xt(self.__xi_g[i], self.__ti_g[i]) for i in range(self.config.Lg)
>>>>>>> 06bc119 (Add surface plot for comparison of results)
        ]
        return Yi_g

    def y_inf(self, x: npt.ArrayLike, t: npt.ArrayLike) -> float:
        """
        :param x: array of x values
        :param t: array of t values
        :return: Value of the integral:

        .. math::
            \\int_{0}^{T} \\int_{A}^{B} G(x,t,y,z) u(y,z) dy dz
        """

        f = lambda x_, t_: self.G(x, t, t_, x_) * self.__u_xt(t_, x_)

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
            [[Yi_0[i] - self.y_inf(self.__xi_0[i], 0)] for i in range(self.config.L0)]
        )
        Y_g = np.array(
            [
                [Yi_g[i] - self.y_inf(self.__xi_g[i], self.__ti_g[i])]
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
                    self.G(
                        self.__xi_0[j], 0, self.config.xi_m0[i], self.config.ti_m0[i]
                    )
                    for i in range(self.config.M0)
                ]
                for j in range(self.config.L0)
            ]
        )
        A_12 = np.array(
            [
                [
                    self.G(
                        self.__xi_0[j], 0, self.config.xi_mg[i], self.config.ti_mg[i]
                    )
                    for i in range(self.config.Mg)
                ]
                for j in range(self.config.L0)
            ]
        )
        A_21 = np.array(
            [
                [
                    self.G(
                        self.__xi_g[j],
                        self.__ti_g[j],
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
                        self.__xi_g[j],
                        self.__ti_g[j],
                        self.config.xi_mg[i],
                        self.config.ti_mg[i],
                    )
                    for i in range(self.config.Mg)
                ]
                for j in range(self.config.Lg)
            ]
        )

        return np.block([[A_11, A_12], [A_21, A_22]])
