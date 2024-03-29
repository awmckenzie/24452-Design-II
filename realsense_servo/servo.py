from adafruit_servokit import ServoKit
import time
import numpy as np
kit = ServoKit(channels=16)

class Servo:
    def __init__(self, pinout, min_angle):
        self.pinout = pinout

        self.angle = 0
        self.target_angle = 0

        if pinout==2 or pinout==3 or pinout==6 or pinout==7:
            self.mirrored = True
        else:
            self.mirrored = False
        
        self.min_angle = min_angle
        self.max_angle = None

        self.zero_point = 90 # angle for the central position

    def zero(self):
        self.move(self.min_angle)
        self.angle = kit.servo[self.pinout].angle

    def move(self, target_angle):
        if self.mirrored:
                target_angle = -target_angle
        if abs(self.angle - target_angle) > 0.05:
            self.target_angle = self.zero_point + target_angle
            kit.servo[self.pinout].angle = self.target_angle
        self.angle = kit.servo[self.pinout].angle

    def update_angle(self):
        self.angle = kit.servo[self.pinout].angle

def init_servos(servos, num_servos, min_angles, max_angle):
    for i in range(num_servos):
        servos.append(Servo(i, min_angles[i]))

    max_offset = np.max(min_angles)

    for i in range(num_servos):
            servos[i].zero()
            servos[i].update_angle()

            servos[i].max_angle = max_angle - max_offset + servos[i].min_angle
    
    return servos