#!/usr/bin/env python
import math
from board import SCL, SDA
import busio
from Adafruit_PCA9685 import PCA9685
#from Adafruit_GPIO import I2C
import time

import RPi_GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

def initialize():
   i2c_bus = busio.I2C(5, 3)
   pca = PCA9685(i2c_bus)
   pca.frequency = 100
   return pca

def steer(pca, angle):
   if angle > 220:
      angle = 220
   if angle < 0:
      angle = 0
   duty = ((angle/180)*6553)+6553
   pca.channels[7].duty_cycle = math.floor(duty)

print("Hi")
pca = initialize()
print("Hi")
steer(pca, 220)
