from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

class Servo:
    def __init__(self, pinout):
        self.pinout = pinout
        self.state = 0

        self.angle = 0
        self.target_angle = 0
        
        self.time = 0

    def zero(self):
        kit.servo[self.pinout].angle = 0

    def move(self, angle):
        if self.state == 0:
            self.state = 1
            self.target_angle = angle # accept new target angle    

        else:
            self.angle = kit.servo[self.pinout].angle
            if self.target_angle == self.angle:
                self.state = 0
        
        kit.servo[self.pinout].angle = self.target_angle

    def get_angle(self):
        return kit.servo[self.pinout].angle



