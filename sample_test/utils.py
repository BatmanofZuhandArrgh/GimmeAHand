from typing import NamedTuple
from cam_calibrate.coord import CoordRobot


class Servo(NamedTuple):
    """Inputs for servos"""
    servo0: float  # degree
    servo1: float  # degree
    servo2: float  # degree

def coord_robot_to_servo(coord_robot: CoordRobot):
    theta_1, theta_2, theta_3 = coord_robot

    # Value of turn_dir is either 1 or -1
    turn_dir_0 = 1
    turn_dir_1 = 1
    turn_dir_2 = -1

    # Offsets
    servo0_offset = 103
    servo1_offset = 160 # Not sure, the value is same as servo value that makes servo 1 go vertical
    servo2_offset = 180

    servo0 = servo0_offset + turn_dir_0*theta_1
    servo1 = servo1_offset + turn_dir_1*theta_2
    servo2 = servo2_offset + turn_dir_2*theta_3

    if servo0 < 0 or servo0 > 180:
        return None
    if servo1 < 60 or servo1 > 180:
        return None
    if servo2 < 40 or servo2 > 180:
        return None
    
    return Servo(servo0, servo1, servo2)