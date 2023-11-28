from typing import NamedTuple


class CoordPixel(NamedTuple):
    """Pixel coordinate (u: left->right, v: top->bottom)"""
    u: int  # pixel
    v: int  # pixel


class Coord3D(NamedTuple):
    """3D coordinate (x: left->right, y: bottom->top, z: far->near)"""
    x: float  # mm
    y: float  # mm
    z: float  # mm


class CoordRobot(NamedTuple):
    """Operational coordinate of robot (angles of the motors)
    theta_1: zero at middle, counter-clockwise is positive direction
    theta_2: zero at vertical, spin from front to back is positive direction
    theta_3: zero when the two arms are aligned, spin from back to front is positive direction"""
    theta_1: float  # degree
    theta_2: float  # degree
    theta_3: float  # degree
