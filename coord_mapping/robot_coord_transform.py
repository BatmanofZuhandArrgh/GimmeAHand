import numpy as np
from coord_mapping.coord import Coord3D, CoordRobot
from coord_mapping.dh_params import RobotDHParams


class RobotCoordTransformer:
    def solve_two_arms_angles(self, a: float, b: float, d: float, h: float) -> (float, float):
        """solve for angles phi_1 (of joint 2) and phi_2 (of joint 3) compared to horizontal 
        phi is used to solve configurations, not to be mistakened for theta
        
        a*c1 + b*c2 = d
        a*s1 + b*s2 = h
        phi_1: 0 -> 180 degree, 0 when arm is front forward horizontal, 90 when it is vertical 
        phi_2: -90 -> 90 degree, 0 when arm is front forward horizontal, 90 when it is vertical 
        always select the solution where phi_1 >= phi_2
        #Please add link explanation
        """ 
        s1a = (d*d + h*h + a*a - b*b) / (2*a*np.sqrt(d*d + h*h)) 
        s2a = (d*d + h*h + b*b - a*a) / (2*b*np.sqrt(d*d + h*h))
        if np.absolute(s1a) > 1 or np.absolute(s2a) > 1:
            return None, None
        alpha = 90.0 - np.rad2deg(np.arctan(h/d))
        phi_1 = 180.0 - np.rad2deg(np.arcsin(s1a)) - alpha
        phi_2 = np.rad2deg(np.arcsin(s2a)) - alpha
        return phi_1, phi_2

    def world_to_robot_coord(self, world_coord: Coord3D) -> CoordRobot:
        """convert target object's world 3D coord to find robot operational coord"""
        """3D coordinate (x: left->right, y: bottom->top, z: far->near)"""
        # Target object coordinate translated to the coordinate system at joint 1
        x1 = world_coord.x
        y1 = world_coord.y - RobotDHParams.d(1) # RobotDHParams.d(1) = 50.4  mm
        z1 = world_coord.z - RobotDHParams.a(0) # RobotDHParams.a(0) = 39.56 mm
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
        phi_1 = robot_coord.theta_2 + 90.0
        phi_2 = phi_1 - robot_coord.theta_3
        a = RobotDHParams.a(2)
        b = RobotDHParams.a(3)
        y3 = RobotDHParams.d(2) + RobotDHParams.d(1) + a * np.sin(np.deg2rad(phi_1))
        y = y3 + b * np.sin(np.deg2rad(phi_2))
        return (y3 >= 0) and (y >= 0)

    def generate_intermediate_coords(self, start: CoordRobot, end: CoordRobot, num_interval: int = 10) -> list[CoordRobot]:
        """generate intermediate points to move the robot"""
        result = [start]
        for i in range(1, num_interval):
            coord = CoordRobot(
                start.theta_1 + (end.theta_1 - start.theta_1) * i / num_interval,
                start.theta_2 + (end.theta_2 - start.theta_2) * i / num_interval,
                start.theta_3 + (end.theta_3 - start.theta_3) * i / num_interval,
            )
            result.append(coord)
        result.append(end)
        return result


if __name__ == "__main__":
    robot_coord_transformer = RobotCoordTransformer()
    x = int(input("Input x: "))
    y = int(input("Input y: "))
    z = int(input("Input z: "))
    world_coord = Coord3D(x, y, z)
    robot_coord = robot_coord_transformer.world_to_robot_coord(world_coord)
    print(robot_coord)
