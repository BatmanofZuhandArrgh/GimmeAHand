import os
import sys
sys.path.append(os.path.dirname(sys.path[0])) #Add the main dir to the import dirs 
print('path: ', sys.path[-1])

import time
from controls.controller import Controller, OFFLINE_DEFAULT_1, OFFLINE_DEFAULT_2, OFFLINE_DEFAULT_3
from motor.motor_utils import Servo

class NaiveController(Controller):
    def __init__(self):
        super().__init__()

    def naive_reach(self):
        self.servos['3'] = self.target_angle3
        time.sleep(2)
        self.servos['2'] = self.target_angle2
        time.sleep(2)

    def naive_retract(self):
        #Return to online default position 
        pass

    def naive_deliver(self):
        
        pass
    
    def naive_return(self):
        pass

    def reset(self):
        # Back to offline default position
        self.servos['2'] = self.target_angle2
        time.sleep(2)

    def grasp(self):
        self.close_ee()

    def execute(self, servo_angles: Servo):
        super().execute(servo_angles)
        print(self.target_angle1, self.target_angle2, self.target_angle3)

        self.servos['1'].angle = self.target_angle1

        self.naive_reach()

        self.grasp()



if __name__ == '__main__':
    controller = NaiveController()
    controller.execute(Servo(0,1,2))