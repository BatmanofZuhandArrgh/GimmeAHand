import numpy as np
from coord import Coord3D, CoordRobot
from dh_params import RobotDHParams


class RobotCoordTransformer:
    def __init__(self, cam_offset: Coord3D):
        self.cam_offset = cam_offset

    def solve_two_arms_angles(self, a: float, b: float, d: float, h: float) -> (float, float):
        """solve for angles phi_1 (of joint 2) and phi_2 (of joint 3) compared to horizontal
        a*c1 + b*c2 = d
        a*s1 + b*s2 = h
        phi_1: 0 -> 180 degree
        phi_2: -90 -> 90 degree
        always select the solution where phi_1 >= phi_2"""
        s1a = (d*d + h*h + a*a - b*b) / (2*a*np.sqrt(d*d + h*h))
        s2a = (d*d + h*h + b*b - a*a) / (2*b*np.sqrt(d*d + h*h))
        if np.absolute(s1a) > 1 or np.absolute(s2a) > 1:
            return None, None
        alpha = 90.0 - np.rad2deg(np.arctan(h/d))
        phi_1 = 180.0 - np.rad2deg(np.arcsin(s1a)) - alpha
        phi_2 = np.rad2deg(np.arcsin(s2a)) - alpha
        return phi_1, phi_2

    def world_to_robot_coord(self, world_coord: Coord3D) -> CoordRobot:
        """convert world 3D coord (origin at base of camera) to robot operational coord"""
        x1 = world_coord.x + self.cam_offset.x
        y1 = world_coord.y + self.cam_offset.y - RobotDHParams.d(1)
        z1 = world_coord.z + self.cam_offset.z - RobotDHParams.a(0)
        theta_1 = None
        if z1 == 0 and x1 == 0:
            return None
        elif z1 == 0 and x1 < 0:
            theta_1 = 90.0
        elif z1 == 0 and x1 > 0:
            theta_1 = -90.0
        else:
            theta_1 = np.rad2deg(np.arctan(x1/z1))
        a = RobotDHParams.a(2)
        b = RobotDHParams.a(3)
        d = np.sqrt(x1*x1 + z1*z1) + RobotDHParams.a(1)
        h = y1 - RobotDHParams.d(2)
        phi_1, phi_2 = self.solve_two_arms_angles(a, b, d, h)
        if phi_1 is None or phi_2 is None:
            return None
        theta_2 = phi_1 - 90.0
        theta_3 = phi_1 - phi_2
        return CoordRobot(theta_1, theta_2, theta_3)


if __name__ == "__main__":
    robot_coord_transformer = RobotCoordTransformer(cam_offset=Coord3D(0, 0, 0))
    x = int(input("Input x: "))
    y = int(input("Input y: "))
    z = int(input("Input z: "))
    world_coord = Coord3D(x, y, z)
    robot_coord = robot_coord_transformer.world_to_robot_coord(world_coord)
    print(robot_coord)
