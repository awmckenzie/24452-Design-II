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
        if round(self.angle) != self.target_angle:
            self.target_angle = angle # accept new target angle    
        
        kit.servo[self.pinout].angle = self.target_angle
        self.angle = kit.servo[self.pinout].angle
        print(round(self.angle), self.target_angle)

    def update_angle(self):
        self.angle = kit.servo[self.pinout].angle



