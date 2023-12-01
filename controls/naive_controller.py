import os
import sys
sys.path.append(os.path.dirname(sys.path[0])) #Add the main dir to the import dirs 
print('path: ', sys.path[-1])

import time
from controls.controller import Controller, OFFLINE_DEFAULT_1, OFFLINE_DEFAULT_2, OFFLINE_DEFAULT_3, \
    ONLINE_DEFAULT_2, ONLINE_DEFAULT_3, USER_POSITION_1
from controls.controls_utils import run_motor
from motor.motor_utils import Servo

INTERVAL = 2 #seconds

#Assume no obstruction except for ground
class NaiveController(Controller):
    def __init__(self):
        super().__init__()

    def naive_reach(self):
        # From the offline default position 2 and 3, reach towards the target obj
        '''
        self.servos['3'].angle = self.target_angle3
        time.sleep(INTERVAL)
        self.servos['2'].angle = self.target_angle2
        time.sleep(INTERVAL)
        '''
        
        run_motor(self.servos['3'], target_angle=self.target_angle3, current_angle=OFFLINE_DEFAULT_3)
        run_motor(self.servos['2'], target_angle=self.target_angle2, current_angle=OFFLINE_DEFAULT_2)

    def naive_retract(self):
        #After grasping, return to online default position 
        '''
        self.servos['3'].angle = ONLINE_DEFAULT_3
        time.sleep(INTERVAL)
        self.servos['2'].angle = ONLINE_DEFAULT_2
        time.sleep(INTERVAL)
        '''
        run_motor(self.servos['2'], target_angle=ONLINE_DEFAULT_2)
        run_motor(self.servos['3'], target_angle=ONLINE_DEFAULT_3)


    def naive_deliver(self):
        #From online default position, turn to the user and deliver the target obj
        '''
        self.servos['1'].angle = USER_POSITION_1
        time.sleep(INTERVAL)
        '''
        run_motor(self.servos['1'], target_angle=USER_POSITION_1)

        self.open_ee()
        time.sleep(INTERVAL)
    
    def naive_return(self):
        #After delivering, return to offline default position
        '''
        self.servos['1'].angle = OFFLINE_DEFAULT_1
        time.sleep(INTERVAL)
        '''
        run_motor(self.servos['1'], target_angle=OFFLINE_DEFAULT_1)
        
        self.all_motor_relax()

    def reset(self):
        #From any (simple) position, back to offline default position from any position
        #Possibly causes huge torque requirements at servo 2, really bad
        self.servos['2'].angle = OFFLINE_DEFAULT_2
        time.sleep(INTERVAL)

        self.servos['3'].angle = OFFLINE_DEFAULT_3
        time.sleep(INTERVAL)

        self.servos['1'].angle = OFFLINE_DEFAULT_1
        time.sleep(INTERVAL)

        self.all_motor_relax()
    
    def execute(self, servo_angles: Servo):
        super().execute(servo_angles)
        print(self.target_angle1, self.target_angle2, self.target_angle3)

        # Turning the robot towards the target object
        '''
        self.servos['1'].angle = self.target_angle1
        time.sleep(INTERVAL)
        '''
        run_motor(self.servos['1'], target_angle=self.target_angle1, current_angle=OFFLINE_DEFAULT_1)

        self.naive_reach()

        self.grasp()

        self.naive_retract()

        self.naive_deliver()

        self.naive_return()

        self.end_routine()

    def grasp(self):
        self.close_ee()

if __name__ == '__main__':
    controller = NaiveController()
    controller.execute(Servo(None,None,None))