import numpy as np
from adafruit_servokit import ServoKit
from time import sleep
kit = ServoKit(channels=16)

angle = 45

while True:
  kit.servo[3].angle = 0
  kit.servo[0].angle = angle
  sleep(2)
  kit.servo[2].angle = 0
  kit.servo[1].angle = angle
  sleep(2)
  kit.servo[1].angle = angle
  kit.servo[2].angle = 0
  sleep(2)
  kit.servo[0].angle = angle
  kit.servo[3].angle = 0

# a = np.array([[1,2,3,4,5,6], [7,8,9,10,11,12]])

# filter = np.hsplit(a, 2)

# print(filter)
