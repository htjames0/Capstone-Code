#!/usr/bin/env python
import math
from board import SCL, SDA
import busio
from Adafruit_PCA9685 import PCA9685
import time


def Servo_Initialize():
   pca = PCA9685()
   pca.set_pwm_freq(60)
   return pca


def Motor_StartUp(pca):
    print('Starting Motor Start Up Sequence')
    #Motor_Speed(pca, 0)
    pca.set_pwm(11, 0, math.floor(.15*4095))
    print('Neutral')
    time.sleep(15)

    pca.set_pwm(11, 0, math.floor(.2*4095))
    print('Forward')
    time.sleep(3)

    pca.set_pwm(11, 0, math.floor(.15*4095))
    print('Neutral')
    time.sleep(3)

    pca.set_pwm(11, 0, math.floor(.1*4095))
    print('Reverse')
    time.sleep(3)

    pca.set_pwm(11, 0, math.floor(.15*4095))
    print('Neutral')
    time.sleep(3)

    print('Start Up Complete')

def Motor_Speed(pca, percent):
    #speed = math.floor(((percent)*3276) + 65535 * 0.15)
    if percent == 1:
        speed = 0.2*4095
    elif percent == -1:
        speed = 0.1*4095
    elif percent == 0:
        speed = 0.15*495
    else: 
        speed = percent * 65535

    speed = math.floor(speed)
    pca.set_pwm(0, 0, speed)
    print(speed)


pca = Servo_Initialize()
Motor_StartUp(pca)

print('')
print('Changing Speeds:')
pca.set_pwm(11,0,math.floor(.25*4095))
time.sleep(10)
pca.set_pwm(11,0,math.floor(.15*4095))


#Motor_Speed(pca, 0.5)
#Motor_Speed(pca, -.12)
#time.sleep(10)
#Motor_Speed(pca, 0.1)
#time.sleep(10)
#Motor_Speed(pca, 0)

'''
motor initialization sequence
pca.set_pwm(0, 0, math.floor(.15*65536))
print('Neutral')
time.sleep(10)
pca.set_pwm(0, 0, math.floor(.2*65536))
print('Forward')
time.sleep(5)
pca.set_pwm(0, 0, math.floor(.1*65536))
print('Reverse')
time.sleep(5)
pca.set_pwm(0, 0, math.floor(.15*65536))
print('Neutral')
time.sleep(5)
Motor_Speed(pca, 0.13)
#while True:
#    pca.set_pwm(0 ,0, math.floor(.2*4096))
'''
