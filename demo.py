import threading
import random
from gpiozero import Servo
from time import sleep

intelDepth = [20., 34.] # assume inches
pins = [23, 18]
minDepth = 10;
maxDepth = 100;
val = -1;

# setup thread
class myThread (threading.Thread):
   def __init__(self, index, name):
      threading.Thread.__init__(self)
      self.i = index
      self.name = name
   def run(self):
      print ("Starting " + self.name)
      servo = Servo(pins[self.i])
      moveServo(servo, self.name, 2)
      GPIO.cleanup()
      print ("Exiting " + self.name)

def moveServo(servo, name, delay):
   # val = intelDepth[i] / (maxDepth - minDepth) - 1 #random factor to convert depth to servo angle. -1 <= val <= 1, angle = 0 corresponds to val = -1
   # if val > 1: val = 1
   # elif val < -1: val = -1
   try:
      while True:
         servo.value = generateDepth()
         sleep(delay)
   except:
      GPIO.cleanup()

# function for generating random intel depth
def generateDepth():
   return random.uniform(-1,0)

# Create new threads
thread1 = myThread(0, "Servo-0")
thread2 = myThread(1, "Servo-1")

# Start new Threads
thread1.start()
thread2.start()
