from adafruit_servokit import ServoKit
import time

import servo

kit = ServoKit(channels=16)

servos = []

def init_servos(num_servos):
    for i in range(num_servos):
        servos.append(servo.Servo(i))

def loop():
    while(True):
        for servo in servos:
            servo.zero()
            servo.update_angle()
            print(servo.angle)


init_servos(2)
loop()
