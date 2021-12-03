from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

# set angle to zero
for i in [2,3,6,7]:
  kit.servo[i].angle = 0
for i in [0,1,4,5]:
  kit.servo[i].angle = 0
