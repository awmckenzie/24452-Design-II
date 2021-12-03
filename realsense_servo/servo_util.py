import ipdb
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

def set(angle=0, pinout=-1):
    if pinout == -1:
        for i in range(16):
            kit.servo[i].angle = angle
    else:
        kit.servo[pinout].angle = angle

ipdb.set_trace()