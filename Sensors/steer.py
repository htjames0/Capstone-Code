#!/usr/bin/env python
import math
from board import SCL, SDA
import busio
from Adafruit_PCA9685 import PCA9685
import time


def initialize():
   pca = PCA9685()
   pca.set_pwm_freq(60)
   return pca

def steer(pca, angle):
   if angle > 220:
      angle = 220
   if angle < 0:
      angle = 0
   duty = math.floor(((angle/180)*6553)+6553)
   print(duty)
   pca.set_pwm(7, 0, 40000)


pca = initialize()

servo_min = 150 #hard right
servo_max = 2000 #hard left
servo_middle = 400 
#math.floor((servo_max - servo_min)/2) #middle 
print(servo_middle)

while True: 
    pca.set_pwm(7, 0, servo_min)
    time.sleep(1)
    pca.set_pwm(7, 0, servo_middle)
    time.sleep(1)
    pca.set_pwm(7, 0, servo_max)
    time.sleep(1)
