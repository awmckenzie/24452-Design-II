import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)
pwm=GPIO.PWM(3, 50)
pwm.start(0)

def SetAngle(angle):
	duty = angle / 18 + 2
	GPIO.output(3, True)
	pwm.ChangeDutyCycle(duty)
	sleep(1)
	GPIO.output(3, False)
	pwm.ChangeDutyCycle(0)

SetAngle(90) 
print("angle is 90")

SetAngle(180)
print("angle is 180")

SetAngle(0)
print("angle is 0")

pwm.stop()
GPIO.cleanup()
