from typing import NamedTuple


class CoordPixel(NamedTuple):
    """Pixel coordinate (u: left->right, v: top->bottom)"""
    u: int
    v: int


class Coord3D(NamedTuple):
    """3D coordinate (x: left->right, y: bottom->top, z: far->near)"""
    x: float
    y: float
    z: float
