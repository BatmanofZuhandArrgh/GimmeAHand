import os
import sys
sys.path.append(os.path.dirname(sys.path[0])) #Add the main dir to the import dirs 
print('path: ', sys.path[-1])

import time
from controls.controller import Controller, OFFLINE_DEFAULT_1, OFFLINE_DEFAULT_2, OFFLINE_DEFAULT_3, \
    ONLINE_DEFAULT_2, ONLINE_DEFAULT_3, USER_POSITION_1
from motor.motor_utils import Servo

INTERVAL = 2 #seconds

#Assume no obstruction except for ground
class PlannedController(Controller):
    def __init__(self, sequence):
        super().__init__()
        # Sequence of config to reach from planning
        self.sequence = sequence

    def reset(self):
        #From any (simple) position, back to offline default position from any position
        pass
    
    def execute(self, servo_angles: Servo):
        super().execute(servo_angles)
        print(servo_angles)

        self.end_routine()

    def grasp(self):
        self.close_ee()

if __name__ == '__main__':
    controller = PlannedController()
    controller.execute(Servo(None,None,None))