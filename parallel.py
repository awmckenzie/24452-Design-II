from adafruit_servokit import ServoKit
import time

import servo

kit = ServoKit(channels=16)

servo1 = servo.Servo(0)

def loop():
    while(True):
        servo1.zero()
        time.sleep(1)
        servo1.update_angle()
        print(servo1.angle)
        servo1.move(180)
        time.sleep(1)
        servo1.update_angle()
        print(servo1.angle)
        servo1.move(0)
        time.sleep(1)
        servo1.update_angle()
        print(servo1.angle)

try:
    loop()
except:
    print('done')