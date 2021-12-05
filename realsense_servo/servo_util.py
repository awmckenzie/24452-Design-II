import ipdb
from adafruit_servokit import ServoKit
import servo
import config

actuators = 8
servos = []
kit = ServoKit(channels=16)
cfg = config.config()
min_angles = cfg['servo_min_angles']
max_angles = cfg['servo_max_angles']

def set(angle=0, pinout=-1):
    if pinout == -1:
        for i in range(actuators):
            servos[i].move(angle)
    else:
        servos[pinout].move(angle)

servo.init_servos(servos, actuators, min_angles, max_angles)

ipdb.set_trace()