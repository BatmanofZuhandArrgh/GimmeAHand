from typing import NamedTuple
from coord_mapping.coord import CoordRobot

class Servo(NamedTuple):
    """Inputs for servos"""
    servo1: float  # degree
    servo2: float  # degree
    servo3: float  # degree

def robot_coord_to_servo(coord_robot: CoordRobot):
    theta_1, theta_2, theta_3 = coord_robot

    # Value of turn_dir is either 1 or -1
    turn_dir_1 = 1
    turn_dir_2 = 1
    turn_dir_3 = -1

    # Offsets
    servo1_offset = 103
    servo2_offset = 158 
    servo3_offset = 180

    servo1 = servo1_offset + turn_dir_1*theta_1
    servo2 = servo2_offset + turn_dir_2*theta_2
    servo3 = servo3_offset + turn_dir_3*theta_3

    if servo1 < 0 or servo1 > 180:
        return None
    if servo2 < 60 or servo2 > 180:
        return None
    if servo3 < 50 or servo3 > 180:
        return None
    
    return Servo(servo1, servo2, servo3)
