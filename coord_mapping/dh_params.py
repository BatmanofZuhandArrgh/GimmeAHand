from typing import NamedTuple


class DHParams(NamedTuple):
    """a_{i-1}, alpha_{i-1}, d_{i} (theta is declared in coord.py)"""
    a:     float  # mm
    alpha: float  # degree
    d:     float  # mm


class RobotDHParams:
    dh_params_list: list[DHParams] = [
        DHParams(a = 39.56, alpha =   0.0, d = 50.4),
        DHParams(a =  21.0, alpha =  90.0, d = 13.0),
        DHParams(a = 100.0, alpha = 180.0, d =  0.0),
        DHParams(a = 250, alpha =   0.0, d =  0.0), #TODO: may have to readjust, full length 262.9, 207.9 from z3 to point-of-contact with obj to be grasped
    ]

    @staticmethod
    def a(i_minus_1: int) -> float:
        return RobotDHParams.dh_params_list[i_minus_1].a

    @staticmethod
    def alpha(i_minus_1: int) -> float:
        return RobotDHParams.dh_params_list[i_minus_1].alpha

    @staticmethod
    def d(i: int) -> float:
        return RobotDHParams.dh_params_list[i - 1].d
