#!/usr/bin/env python
import math
from board import SCL, SDA
import busio
from Adafruit_PCA9685 import PCA9685
#from Adafruit_GPIO import I2C
import time

#import RPi.GPIO as GPIO
#GPIO.setmode(GPIO.BOARD)

def initialize():
   i2c_bus = busio.I2C(SCL, SDA)
   pca = PCA9685()
   pca.set_pwm_freq(100)
   return pca

def steer(pca, angle):
   if angle > 220:
      angle = 220
   if angle < 0:
      angle = 0
   duty = math.floor(((angle//180)*6553)+6553)
   #pca.channels[7].duty_cycle = math.floor(duty)
   print(duty)
   pca.set_pwm(7, 0, 25000)


print("Hi")
pca = initialize()
print("Hi")
steer(pca, 15)
