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
        self.angle = 0

    def move(self, target_angle):
        self.angle = kit.servo[self.pinout].angle
        if abs(self.angle - target_angle) < 0.01:
            self.target_angle = target_angle
        else:
            kit.servo[self.pinout].angle = target_angle
            
    def update_angle(self):
        self.angle = kit.servo[self.pinout].angle



