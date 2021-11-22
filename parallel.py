from adafruit_servokit import ServoKit
import time

import servo

kit = ServoKit(channels=16)

servo1 = servo.Servo(0)

def loop():
    while(True):
        servo1.move(180)
        servo1.move(0)

try:
    loop()
except:
    print('done')