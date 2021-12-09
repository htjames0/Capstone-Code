#!/usr/bin/env python
import math
from board import SCL, SDA
import busio
from Adafruit_PCA9685 import PCA9685
import time


def Servo_Initialize():
   pca = PCA9685()
   pca.set_pwm_freq(100)
   return pca

def Wheel_Steer(pca, angle):
   if angle > 180:
      angle = 180
   if angle < 0:
      angle = 0
   print(angle)
   duty = math.floor(((angle/180)*270)+540)
   pca.set_pwm(8, 0, duty)


pca = Servo_Initialize()

servo_min = 540 #hard right
servo_max = 810 #hard left
servo_middle = math.floor((servo_max - servo_min)/2) #middle

print('The hard right PWM is 540')
print('The hard left PWM is 810')
print('The middle PWM is: %d' % servo_middle)

while True:
   #pca.set_pwm(7, 0, servo_middle)
   Wheel_Steer(pca, 180)
   time.sleep(1)
   #pca.set_pwm(7, 0, servo_max)
   Wheel_Steer(pca, 0)
   time.sleep(1)

#for i in range(0, 2000, 30):
#   pca.set_pwm(7, 0, i)
#   time.sleep(1) 
#   print(i)
