from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

angle = 45
# set angle to 0
kit.servo[0].angle = angle
kit.servo[1].angle = angle
kit.servo[2].angle = 90 - angle
kit.servo[3].angle = 90 - angle
