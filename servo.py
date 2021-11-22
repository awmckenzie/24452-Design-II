from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

class Servo:
    def __init__(self, pinout):
        self.pinout = pinout
        self.state = 0
        self.angle = 0
        self.time = 0
        self.throttle = 1

    def zero(self):
        kit.servo[self.pinout].angle = 0

    def move(self, angle):
        if self.state == 0:
            kit.continuous_servo[self.pinout].throttle = self.throttle

    def update_angle(self):
        self.angle = kit.servo[self.pinout].angle



