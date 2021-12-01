import numpy as np
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

# set angle to zero
kit.servo[6].angle = 0
kit.servo[7].angle = 0

# a = np.array([[1,2,3,4,5,6], [7,8,9,10,11,12]])

# filter = np.hsplit(a, 2)

# print(filter)
