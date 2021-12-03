from adafruit_servokit import ServoKit
import time
kit = ServoKit(channels=16)

class Servo:
    def __init__(self, pinout, min_angle, max_angle):
        self.pinout = pinout

        self.angle = 0
        self.target_angle = 0

        if pinout % 2 == 0:
            self.mirrored = -1
        else:
            self.mirrored = 1
        
        self.min_angle = min_angle
        self.max_angle = max_angle

    def zero(self):
        kit.servo[self.pinout].angle = 0
        self.angle = 0

    def move(self, target_angle):
        self.angle = kit.servo[self.pinout].angle
        if abs(self.angle - target_angle) > 0.005:
            self.target_angle = target_angle
            kit.servo[self.pinout].angle = self.mirrored * self.target_angle

    def update_angle(self):
        self.angle = kit.servo[self.pinout].angle

def init_servos(servos, num_servos, min_angles, max_angles):
    for i in range(num_servos):
        servos.append(Servo(i, min_angles[i], max_angles[i]))

    for s in servos:
            s.zero()
            s.update_angle()
    
    return servos