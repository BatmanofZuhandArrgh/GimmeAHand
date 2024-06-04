import time

from board import SCL, SDA
import busio

from motor.motor_utils import Servo

from adafruit_motor import servo
from adafruit_pca9685 import PCA9685

MIN_PULSE = 400
MAX_PULSE = 2700 #2400
MAX_DEGREE = 208

# Angles of joints when default offline (resting, not holding anything) and online (carrying the bottle)
OFFLINE_DEFAULT_1 = 103
OFFLINE_DEFAULT_2 = 180
OFFLINE_DEFAULT_3 = 60
OFFLINE_DEFAULT_4 = 75

ONLINE_DEFAULT_2 = 200 #180
ONLINE_DEFAULT_3 = 80 #110 #when online 2 = 180, 80 is horizontal 
ONLINE_DEFAULT_4 = 75

# Assumed position of the user
USER_POSITION_1 = 150

INTERVAL = 0.5 #seconds

class Controller:
    def __init__(self) -> None:

        #See pca_motor_test for specifics
        i2c = busio.I2C(SCL, SDA)
        
        self.pca = PCA9685(i2c)
        self.pca.frequency = 50

        #Channels on the pca9685, depends on io pins connected
        index0 = 0 *4
        index1 = 1 *4
        index2 = 2 *4
        index3 = 3 *4
        
        
        self.motor_ids = ['1', '2', '3', 'ee'] #ee for end-effector
        self.servos = {k:None for k in self.motor_ids}
        self.servos['1'] = servo.Servo(self.pca.channels[index0], min_pulse=MIN_PULSE, max_pulse=MAX_PULSE, actuation_range=MAX_DEGREE)
        self.servos['2'] = servo.Servo(self.pca.channels[index1], min_pulse=MIN_PULSE, max_pulse=MAX_PULSE, actuation_range=MAX_DEGREE)
        self.servos['3'] = servo.Servo(self.pca.channels[index2], min_pulse=MIN_PULSE, max_pulse=MAX_PULSE, actuation_range=MAX_DEGREE)
        self.servos['ee']= servo.Servo(self.pca.channels[index3], min_pulse=MIN_PULSE, max_pulse=MAX_PULSE, actuation_range=MAX_DEGREE)

        self.target_angle1 = None
        self.target_angle2 = None
        self.target_angle3 = None

    def get_angles(self):
        for key in self.servos:
            print('Servo ', key, self.servos[key].angle, ' degrees')

    def reset(self):
        pass

    def execute(self, servo_angles: Servo):
        self.target_angle1 = servo_angles.servo1
        self.target_angle2 = servo_angles.servo2
        self.target_angle3 = servo_angles.servo3

    def grasp(self):
        pass

    def end_routine(self):
        # Turn off pca 
        self.pca.deinit()

    def motor_relax(self, motor_id):
        self.servos[motor_id].angle = None
        
    def all_motor_relax(self):
        for i in self.motor_ids:
                print(i)
                self.servos[i].angle = None
                time.sleep(1)

    def open_ee(self):
        self.servos['ee'].angle = 50 # max opening

    def close_ee(self):
        self.servos['ee'].angle = 90 # max closing

    def go_online(self):
        self.servos['2'].angle = ONLINE_DEFAULT_2
        time.sleep(INTERVAL)
        
        self.servos['3'].angle = ONLINE_DEFAULT_3
        time.sleep(INTERVAL)
        
        self.servos['1'].angle = OFFLINE_DEFAULT_1
        time.sleep(INTERVAL)    
        
        self.open_ee()
        time.sleep(INTERVAL)    

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
