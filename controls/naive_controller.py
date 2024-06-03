import os
import sys
sys.path.append(os.path.dirname(sys.path[0])) #Add the main dir to the import dirs 
print('path: ', sys.path[-1])

import time
from controls.controller import Controller, OFFLINE_DEFAULT_1, OFFLINE_DEFAULT_2, OFFLINE_DEFAULT_3, \
    ONLINE_DEFAULT_2, ONLINE_DEFAULT_3, USER_POSITION_1, INTERVAL
from controls.controls_utils import run_motor
from motor.motor_utils import Servo #, robot_coord_to_servo
#from coord_mapping.robot_coord_transform import RobotCoordTransformer

INTERVAL = 0.5 #seconds

#Assume no obstruction except for ground
class NaiveController(Controller):
    def __init__(self):
        super().__init__()
    
    def segmented_reach(self, num_intervals = 10):
        '''
        For motor 2 and 3, move in a segmented way to reduce jerk motion and induce small changes, 
        leading to require less reaching precision (does that make sense? 
        basically, the ee is missing the object by really small diff by now, 
        so gently grasping it in a ziczac way so the bottle would slide into the ee is useful) 
        '''

        seg_seq_2 = []
        seg_seq_3 = []
        for i in range(0, num_intervals):
            seg_seq_2.append(ONLINE_DEFAULT_2 + (self.target_angle2 -  ONLINE_DEFAULT_2)*i/num_intervals)
            time.sleep(0.1)
            seg_seq_3.append(ONLINE_DEFAULT_3 + (self.target_angle3 -  ONLINE_DEFAULT_3)*i/num_intervals)
            time.sleep(0.1)
            
        seg_seq_2.append(self.target_angle2)
        seg_seq_3.append(self.target_angle3)
        print('2: ',seg_seq_2)
        print('3: ',seg_seq_3)
        
        for i in range(len(seg_seq_2)-1):
                run_motor(self.servos['3'], target_angle=seg_seq_3[i+1], current_angle=seg_seq_3[i], interval = 0.05)
                time.sleep(0.1)
                run_motor(self.servos['2'], target_angle=seg_seq_2[i+1], current_angle=seg_seq_2[i], interval = 0.05)
                time.sleep(0.1)
                
    def naive_reach(self):
        # From the offline default position 2 and 3, reach towards the target obj
  
        self.servos['2'].angle = self.target_angle2
        time.sleep(INTERVAL)
        #self.servos['3'].angle = self.target_angle3
        #time.sleep(INTERVAL)
        
        run_motor(self.servos['3'], target_angle=self.target_angle3, current_angle=ONLINE_DEFAULT_3, interval = 0.05)
        time.sleep(INTERVAL)  
        
        '''
        run_motor(self.servos['3'], target_angle=self.target_angle3, current_angle=OFFLINE_DEFAULT_3)
        time.sleep(INTERVAL)
        run_motor(self.servos['2'], target_angle=self.target_angle2, current_angle=OFFLINE_DEFAULT_2)
        time.sleep(INTERVAL)
        '''
        
    def naive_retract(self):
        #After grasping, return to online default position 
        self.servos['3'].angle = ONLINE_DEFAULT_3
        time.sleep(INTERVAL)
        self.servos['2'].angle = ONLINE_DEFAULT_2
        time.sleep(INTERVAL)
        '''
        run_motor(self.servos['2'], target_angle=ONLINE_DEFAULT_2)
        time.sleep(INTERVAL)
        run_motor(self.servos['3'], target_angle=ONLINE_DEFAULT_3)
        time.sleep(INTERVAL)
        '''

    def naive_deliver(self):
        #From online default position, turn to the user and deliver the target obj
        self.servos['1'].angle = USER_POSITION_1
        time.sleep(INTERVAL)
        '''
        run_motor(self.servos['1'], target_angle=USER_POSITION_1)
        '''
        self.servos['3'].angle = 100
        time.sleep(INTERVAL)
        self.servos['2'].angle = 150
        time.sleep(INTERVAL)
        #self.servos['3'].angle = None
        #time.sleep(3 * INTERVAL)
        self.open_ee()
        time.sleep(INTERVAL)
        
        self.servos['2'].angle = ONLINE_DEFAULT_2
        self.servos['3'].angle = ONLINE_DEFAULT_3
        time.sleep(INTERVAL +1)
    
    def naive_return(self):
        #After delivering, return to offline default position
        self.servos['1'].angle = OFFLINE_DEFAULT_1
        time.sleep(INTERVAL)
        
        self.go_offline()
        '''
        run_motor(self.servos['1'], target_angle=OFFLINE_DEFAULT_1)
        '''
        self.all_motor_relax()

    def go_offline(self):
        #From any (simple) position, back to offline default position from any position
        #Possibly causes huge torque requirements at servo 2, really bad
        
        self.servos['3'].angle = OFFLINE_DEFAULT_3
        time.sleep(INTERVAL)
        
        self.servos['2'].angle = OFFLINE_DEFAULT_2
        time.sleep(INTERVAL)
        
        self.servos['1'].angle = OFFLINE_DEFAULT_1
        time.sleep(INTERVAL)
        
        self.close_ee()
        time.sleep(INTERVAL)
        
    def go_online(self):
        self.servos['2'].angle = ONLINE_DEFAULT_2
        time.sleep(INTERVAL)
        
        self.servos['3'].angle = ONLINE_DEFAULT_3
        time.sleep(INTERVAL)
        
        self.servos['1'].angle = OFFLINE_DEFAULT_1
        time.sleep(INTERVAL)  
        
    def execute(self, servo_angles: Servo):
        super().execute(servo_angles)
        print(self.target_angle1, self.target_angle2, self.target_angle3)
        self.go_online()
        self.open_ee()
        time.sleep(INTERVAL)
        
        # Turning the robot towards the target object
        self.servos['1'].angle = self.target_angle1
        time.sleep(INTERVAL)
        
        print('angle servo 1')
        
        #self.naive_reach()
        self.segmented_reach()
        print('reach')
        time.sleep(INTERVAL)
        
        self.grasp()
        print('grasp')
        time.sleep(INTERVAL)
        
        self.naive_retract()
        print('retract')
        time.sleep(INTERVAL)
        
        self.naive_deliver()
        print('deviver')
        time.sleep(INTERVAL)
        
        self.naive_return()
        print('return')
        time.sleep(INTERVAL)
        
        self.all_motor_relax()
        print('relax')
        self.end_routine()

    def grasp(self):
        self.close_ee()

if __name__ == '__main__':
    controller = NaiveController()
    controller.execute(Servo(None,None,None))
