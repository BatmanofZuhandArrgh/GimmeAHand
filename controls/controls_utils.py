import time

def run_motor(servo_motor, target_angle, current_angle = None,  interval = 0.03):
    '''
    Move a motor gradually, defined by time interval per degree rotated
    servo_motor     : adafruit_motor servo object
    target_angle    : target angle for motor (degree)
    interval        : time interval between each change of 1 degree
    current_angle   : since the adafruit_motor.servo api can only read the motor's current angle if it was used to move the motor there, 
                        not when the motor is resting or moved by hand
                        we'd need to input current angle in such case, to decrease the chance of sudden jerk of movement towards current_angle   
    '''
    if servo_motor.angle == None and current_angle == None:
        #Move right away to target angle if the motor is in relaxed position
        servo_motor.angle = target_angle 
        time.sleep(1)
        return
    
    if current_angle != None: current_angle = servo_motor.angle

    if not servo_motor.angle:
        if abs(current_angle - servo_motor.angle)>5:
            #If reading from servo motor is too different from each other
            raise ValueError('Flagging input current angle is not closed to readings from motor')

    for i in range(current_angle, target_angle):
        servo_motor.angle = i
        time.sleep(interval)