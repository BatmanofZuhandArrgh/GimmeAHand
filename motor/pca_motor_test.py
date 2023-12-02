#For testing and tuning purposes

# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time

from board import SCL, SDA
import busio

# Import the PCA9685 module. Available in the bundle and here:
#   https://github.com/adafruit/Adafruit_CircuitPython_PCA9685
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685

i2c = busio.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c)
# You can optionally provide a finer tuned reference clock speed to improve the accuracy of the
# timing pulses. This calibration will be specific to each board and its environment. See the
# calibration.py example in the PCA9685 driver.
# pca = PCA9685(i2c, reference_clock_speed=25630710)
pca.frequency = 50

# To get the full range of the servo you will likely need to adjust the min_pulse and max_pulse to
# match the stall points of the servo.
# This is an example for the Sub-micro servo: https://www.adafruit.com/product/2201
# servo7 = servo.Servo(pca.channels[7], min_pulse=580, max_pulse=2350)
# This is an example for the Micro Servo - High Powered, High Torque Metal Gear:
#   https://www.adafruit.com/product/2307
# servo7 = servo.Servo(pca.channels[7], min_pulse=500, max_pulse=2600)
# This is an example for the Standard servo - TowerPro SG-5010 - 5010:
#   https://www.adafruit.com/product/155
# servo7 = servo.Servo(pca.channels[7], min_pulse=400, max_pulse=2400)
# This is an example for the Analog Feedback Servo: https://www.adafruit.com/product/1404
# servo7 = servo.Servo(pca.channels[7], min_pulse=600, max_pulse=2500)
# This is an example for the Micro servo - TowerPro SG-92R: https://www.adafruit.com/product/169
# servo7 = servo.Servo(pca.channels[7], min_pulse=500, max_pulse=2400)

# The pulse range is 750 - 2250 by default. This range typically gives 135 degrees of
# range, but the default is to use 180 degrees. You can specify the expected range if you wish:
# servo7 = servo.Servo(pca.channels[7], actuation_range=135)
#servo7 = servo.Servo(pca.channels[0]) #, min_pulse=400, max_pulse=240)
# 205 - 460

# 3 things to calib acturation_range = 180 (default), min_pulse 400 and max_pulse 2400 for MG9965R
# max_pulse can go to 2500 or more
MIN_PULSE = 400
MAX_PULSE = 2400
index1 = 1 *4
index2 = 2 *4
index3 = 3 *4
servo1 = servo.Servo(pca.channels[index1], min_pulse=MIN_PULSE, max_pulse=MAX_PULSE) #actuation range
servo2 = servo.Servo(pca.channels[index2], min_pulse=MIN_PULSE, max_pulse=MAX_PULSE)
servo3 = servo.Servo(pca.channels[index3], min_pulse=MIN_PULSE, max_pulse=MAX_PULSE)

# We sleep in the loops to give the servo time to move into position.
'''
servo3.angle=50
time.sleep(2)
servo2.angle =40 #Input is actual degree
time.sleep(2)
servo1.angle =180 #Input is actual degree
time.sleep(2)
'''

'''
for i in range(180):
    print(i)
    servo.angle = i
    #print('servo',servo.angle)
    time.sleep(0.03)
'''

'''
print('servo1', servo1.angle)
print('servo2', servo2.angle)
print('servo3', servo3.angle)
'''

# Relax Servo
'''
servo1.angle = None
servo2.angle = None
servo3.angle = None
'''

# Write function to convert 3D to 2D
def get_2d_from_3d(x, y, z):
    return None, None

# 3D coordinates
x = None
y = None
z = None

# Step 1: Go to default position
servo3.angle = 50
time.sleep(1)
servo0.angle = 103
time.sleep(1)
servo1.angle = 180
time.sleep(1)
servo2.angle = 60
time.sleep(1)

# Step 2: Turn towards the bottle
servo0.angle = None 
time.sleep(1)

# Step 3: Convert 3D bottle coordinates to 2D coordinates for servo1 and servo2
servo1_deg, servo2_deg = get_2d_from_3d(x,y,z)

# Step 4: Turn (Use planning)
def plan_and_move(servo1_deg, servo2_deg):
    return None

# Step 5: Grap
servo3.angle = 90
time.sleep(1)

# Step 6: Move bottle to default position
servo1.angle = 180
time.sleep(1)
servo2.angle = 60
time.sleep(1)

# Step 7: Turn to designated position
servo0.angle = 180
time.sleep(1)

# Step 8: Release bottle
servo3.angle = 50
time.sleep(1)

'''
Default: servo0 = 103, servo1 = 180, servo2 = 60, servo3 = 50
Servo 0: for the default set, straight ahead, basic position is deg = 103
Servo 1: min deg = 45 (if no obstruction), default = max = 180 
Servo 2: 
Servo 3 (end effector): max deg = 90 (close), min deg = 50 (open)

Limit 1:
Realistically, Servo 1 = 60 and Servo 2 = 180 touches ground (max stretch)
Servo 2 must be at 180 first
If servo 2 wants to reduce, Servo 1 must increase

Limit 2:
Another config: servo1 = 180 (max) and servo2 = 40 (min)

'''







#for i in [0, 30, 45, 60]:
#    servo7.angle = i
 #   time.sleep(1)
#for i in range(180):
#    servo7.angle = 180 - i
#    time.sleep(0.03)

# You can also specify the movement fractionally.
#fraction = 0.0
#while fraction < 1.0:
#    servo7.fraction = fraction
#    fraction += 0.01
#    time.sleep(0.03)

pca.deinit()
