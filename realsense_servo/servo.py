from adafruit_servokit import ServoKit
import time
kit = ServoKit(channels=16)

class Servo:
    def __init__(self, pinout, min_angle, max_angle):
        self.pinout = pinout

        self.angle = 0
        self.target_angle = 0

        if pinout==0 or pinout==1 or pinout==4 or pinout==5:
            self.mirrored = True
        else:
            self.mirrored = False
        
        self.min_angle = min_angle
        self.max_angle = max_angle

        self.zero_point = 90 # angle for the central position

    def zero(self):
        kit.servo[self.pinout].angle = self.zero_point
        self.angle = self.zero_point

    def move(self, target_angle):
        if self.mirrored:
                target_angle = -target_angle
        if abs(self.angle - target_angle) > 0.05:
            self.target_angle = self.zero_point + target_angle
            kit.servo[self.pinout].angle = self.target_angle
        self.angle = kit.servo[self.pinout].angle

    def update_angle(self):
        self.angle = kit.servo[self.pinout].angle

def init_servos(servos, num_servos, min_angles, max_angles):
    for i in range(num_servos):
        servos.append(Servo(i, min_angles[i], max_angles[i]))

    for s in servos:
            s.zero()
            s.update_angle()
    
    return servos