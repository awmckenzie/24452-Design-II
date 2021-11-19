
from gpiozero import Servo
from time import sleep

servo = Servo(25)

try:
	while True:
		servo.min()
#		servo.value = 0.5
		sleep(0.5)
		servo.mid()
		sleep(0.5)
		servo.max()
		sleep(0.5)
		#print(servo.angle)
		#sleep(1)
		print("Done")

except KeyboardInterrupt:
	print("Program stopped")

