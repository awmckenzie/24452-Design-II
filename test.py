from adafruit_servokit import ServoKit
import time
kit = ServoKit(channels=16)


while(True):
    kit.continuous_servo[0].throttle = 1
    time.sleep(1)
    kit.continuous_servo[0].throttle = -1
    time.sleep(1)
    kit.continuous_servo[0].throttle = 0
    time.sleep(1)