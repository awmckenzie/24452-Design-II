from adafruit_servokit import ServoKit
import time
import random

import servo

kit = ServoKit(channels=16)

actuators = 2
servos = []
servo_targets = [0, 0, 0, 0, 0, 0, 0, 0] # 0 to 180 degrees
depths = [0, 0, 0, 0, 0, 0, 0, 0] # 600 to 2000 mm
depth_refresh = 0.07 # ~15 Hz

min_range = 600
max_range = 2000

servo_pos_zero = True
def fake_input(time):
    for i in range(actuators):
        if servo_pos_zero:
            servo_targets[i] = 0
        else:
            servo_targets[i] = 180
        servo_pos_zero = not servo_pos_zero

    #print(round(time,2) - round(time))
    """
    if (round(round(time,2) - round(time),2)) % depth_refresh == 0:
        for i in range(actuators):
            depths[i] = random.randint(min_range, max_range)
            servo_targets[i] = round(180 * (depths[i] - min_range) / (max_range - min_range))
        print(depths)
        #print(servo_targets)
        #print()
    """
    


def init_servos(num_servos):
    for i in range(num_servos):
        servos.append(servo.Servo(i))

    for s in servos:
            s.zero()
            s.update_angle()
            #print(s.angle)

def poll():

    servo[0].move(0)
    servo[0].move(180)
    servo[0].move(0)
    servo[0].move(180)
    servo[0].move(0)
    servo[0].move(180)
    servo[0].move(0)
    servo[0].move(180)
    servo[0].move(0)
    servo[0].move(180)
    
    while(False):
        fake_input(time.time())
        
        for i in range(actuators):
            servos[i].move(servo_targets[i])

        # time.sleep(1)

        # for servo in servos:
        #     servo.move(180)
        #     servo.update_angle()
        #     print(servo.angle)

        # time.sleep(1)

init_servos(8)
poll()
