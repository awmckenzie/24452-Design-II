import threading
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
from time import sleep

# setup thread
class myThread (threading.Thread):
   def __init__(self, index, name):
      threading.Thread.__init__(self)
      self.i = index
      self.name = name
   def run(self):
      print ("Starting " + self.name)
      moveServo(self.i, 2)
      print ("Exiting " + self.name)

def moveServo(index, delay):
   try:
      while True:
         kit.servo[index].angle = 180
         kit.servo[index+1].angle = 180
         sleep(delay)
         kit.servo[index].angle = 90
         kit.servo[index+1].angle = 90
         sleep(delay)
         kit.servo[index].angle = 0
         kit.servo[index+1].angle = 0
         sleep(delay)
   except:
      GPIO.cleanup()

# Create new threads
thread1 = myThread(0, "Servo-0")
# thread2 = myThread(1, "Servo-1")
thread3 = myThread(2, "Servo-2")
# thread4 = myThread(3, "Servo-3")
thread5 = myThread(4, "Servo-4")
# thread6 = myThread(5, "Servo-5")
thread7 = myThread(6, "Servo-6")
# thread8 = myThread(7, "Servo-7")

# Start new Threads
thread1.start()
# thread2.start()
thread3.start()
# thread4.start()
thread5.start()
# thread6.start()
thread7.start()
# thread8.start()
