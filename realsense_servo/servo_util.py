import ipdb
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

ipdb.set_trace()
def set(angle = 0, pinout = None):
    if pinout == None:
        for i in range(16):
            kit.servo[i].angle = angle
    else:
        kit.servo[pinout].angle = angle
