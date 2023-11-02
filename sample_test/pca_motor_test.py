# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
# Source: https://github.com/adafruit/Adafruit_Python_PCA9685/blob/master/examples/simpletest.py
from __future__ import division
import time

# Import the PCA9685 module.
import Adafruit_PCA9685


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Configure min and max servo pulse lengths
servo_min = 100 #150  # Min pulse length out of 4096
servo_max = 600 #600  # Max pulse length out of 4096

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 50       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    print(pulse)
    pwm.set_pwm(channel, 0, pulse)

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

print('Moving servo on channel 0, press Ctrl-C to quit...')

#For hobby motors, people said 
# 1ms : 0 deg
# 1.5ms: 90 deg
# 2 ms : 180 deg
# not working

while True:
    # Move servo on channel O between extremes.
    #pwm.set_pwm(1, 0, servo_min)
    pwm.set_pwm(0, 0, servo_min) #1ms/20ms -> 205/4096 bits
    #set_servo_pulse(0, 1)
    time.sleep(1)
    pwm.set_pwm(0, 0, servo_max)
    #pwm.set_pwm(1, 0, servo_max)
    #set_servo_pulse(0, 2)
    time.sleep(1)
