from adafruit_servokit import ServoKit
import time
kit = ServoKit(channels=16)

class Servo:
    def __init__(self, pinout):
        self.pinout = pinout

        self.angle = 0
        self.target_angle = 0

    def zero(self):
        kit.servo[self.pinout].angle = 90
        self.angle = 90

    def move(self, target_angle):
        self.angle = kit.servo[self.pinout].angle
        if abs(self.angle - target_angle) < 0.005:
            self.target_angle = target_angle
        else:
            kit.servo[self.pinout].angle = target_angle

    def update_angle(self):
        self.angle = kit.servo[self.pinout].angle

def init_servos(servos, num_servos):
    for i in range(num_servos):
        servos.append(Servo(i))

    for s in servos:
            s.zero()
            s.update_angle()
    
    return servos