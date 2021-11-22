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

        time.sleep(1)

        for servo in servos:
            servo.move(180)
            servo.update_angle()
            print(servo.angle)

        time.sleep(1)

init_servos(8)
loop()
