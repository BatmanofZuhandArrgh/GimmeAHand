import numpy as np
from coord import Coord3D, CoordRobot
from dh_params import RobotDHParams


class RobotCoordTransformer:
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
        """convert world 3D coord to robot operational coord"""
        x1 = world_coord.x
        y1 = world_coord.y - RobotDHParams.d(1)
        z1 = world_coord.z - RobotDHParams.a(0)
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

    def robot_to_world_coord(self, robot_coord: CoordRobot) -> Coord3D:
        """convert robot operational coord to world 3D coord"""
        phi_1 = robot_coord.theta_2 + 90.0
        phi_2 = phi_1 - robot_coord.theta_3
        a = RobotDHParams.a(2)
        b = RobotDHParams.a(3)
        d = a * np.cos(np.deg2rad(phi_1)) + b * np.cos(np.deg2rad(phi_2))
        h = a * np.sin(np.deg2rad(phi_1)) + b * np.sin(np.deg2rad(phi_2))
        x = -1 * (d - RobotDHParams.a(1)) * np.sin(np.deg2rad(robot_coord.theta_1))
        y = h + RobotDHParams.d(2) + RobotDHParams.d(1)
        z = -1 * (d - RobotDHParams.a(1)) * np.cos(np.deg2rad(robot_coord.theta_1)) + RobotDHParams.a(0)
        return Coord3D(x, y, z)

    def is_above_ground(self, robot_coord: CoordRobot) -> bool:
        """check if robot config coord is above ground"""
        world_coord = self.robot_to_world_coord(robot_coord)
        return world_coord.y >= 0


if __name__ == "__main__":
    robot_coord_transformer = RobotCoordTransformer()
    x = int(input("Input x: "))
    y = int(input("Input y: "))
    z = int(input("Input z: "))
    world_coord = Coord3D(x, y, z)
    robot_coord = robot_coord_transformer.world_to_robot_coord(world_coord)
    print(robot_coord)
