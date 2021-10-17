import numpy as np
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

IR1 = 5
IR2 = 6 
IR3 = 13
IR4 = 26
IR5 = 19

def linetrack_init(IN1, IN2, IN3, IN4, IN5):
   GPIO.setup(IN1, GPIO.IN)
   GPIO.setup(IN2, GPIO.IN)
   GPIO.setup(IN3, GPIO.IN)
   GPIO.setup(IN4, GPIO.IN)
   GPIO.setup(IN5, GPIO.IN)

def linetrack_read(IN1, IN2, IN3, IN4, IN5):
   R1 = GPIO.input(IN1)
   R2 = GPIO.input(IN2)
   R3 = GPIO.input(IN3)
   R4 = GPIO.input(IN4)
   R5 = GPIO.input(IN5)
   return np.array([R1, R2, R3, R4, R5])

linetrack_init(IR1, IR2, IR3, IR4, IR5)

start_time = time.time()
cur_time = start_time
mesg_time = start_time
while(start_time + 30  > cur_time):
   time.sleep(0.01)
   cur_time = time.time()
   if(mesg_time + 0.1 < cur_time):
      mesg_time = cur_time
      distance = linetrack_read(IR1, IR2, IR3, IR4, IR5)
      print(f'{distance}\n')

GPIO.cleanup()
