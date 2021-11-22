from adafruit_servokit import ServoKit
import time
import random

import servo

kit = ServoKit(channels=16)

actuators = 8
servos = []
servo_targets = [0, 0, 0, 0, 0, 0, 0, 0] # 0 to 180 degrees
depths = [0, 0, 0, 0, 0, 0, 0, 0] # 600 to 2000 mm
depth_refresh = 0.07 # ~15 Hz

min_range = 600
max_range = 2000

def fake_input(time):
    if (round(time,2) - round(time)) % depth_refresh == 0:
        for i in range(actuators):
            depths[i] = random.randint(min_range, max_range)
            servo_targets[i] = 180 * (depths[i] - min_range) / (max_range - min_range)
        print(depths)


def init_servos(num_servos):
    for i in range(num_servos):
        servos.append(servo.Servo(i))

    for s in servos:
            s.move(0)
            s.get_angle()
            print(s.angle)

def poll():
    while(True):
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
