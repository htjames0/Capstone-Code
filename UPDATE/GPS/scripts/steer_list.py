#!/usr/bin/env python
import rospy
from std_msgs.msg import String
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
   duty = math.floor(((angle/180)*270)+540)
   pca.set_pwm(7, 0, duty)


pca = Servo_Initialize()

servo_min = 540 #hard right
servo_max = 810 #hard left
servo_middle = math.floor((servo_max - servo_min)/2) #middle

#print('The hard right PWM is 540')
#print('The hard left PWM is 810')
#print('The middle PWM is: %d' % servo_middle)


history = [0,0,0,0,0]
#changes = []

def callback(data):
  #global history
  #global changes
  #changes = []

#initialize 
  turn = 0

  str = (data.data)
  arr = str.split()
  read = arr
  print(read)

  history.append(arr)
  prev = history[-2]
   
  #for i in range(5):
  if prev is not read:
      if read[3] == 0:                                    #it is over the black
         if read[4] == 0 and read[2] == 0:                      # good
            turn += 0
         if read[4] == 0 and read[2] == 1:                      # small turn left
            turn += 1
         if read[4] == 1 and read[2] == 0:                      # small turn right
            turn -= 1
      elif read[3] == 1:                                  #it is not over the black
         if read[4] == 1 and read[2] == 1:
            if read[1] == 1:
               turn = turn + 3                                  # large turn left
            if read[1] == 0:
               turn = turn - 3                                  # large turn right
         if read[4] == 0 and read[2] == 1:
            turn = turn + 2                                     # medium turn left
         if read[4] == 1 and read[2] == 0:
            turn = turn - 1                                     # medium turn right
         if read[4] == 1 and read[2] == 1 and read[1] == 1 and read[5] == 1:
            turn  = turn   # stop motor for right now might rely on previous  
  else:
      turn += 0

  print("turn: %d" % turn)

  if turn < 0:  # turn right
      print("turn right")
      Wheel_Steer(pca, )
  if turn > 0:
      print("turn left")
      Wheel_Steer(pca, )
  if turn == 0:
      print("no turn")
      Wheel_Steer(pca, servo_middle)


  last = read 


def listener():
   rospy.init_node('steer_list', anonymous = True)
   rospy.Subscriber('line_topic', String, callback)
   rospy.spin()

if __name__ == '__main__':
   listener()

#pca.set_pwm(7,0, 0)
#while True:
    #pca.set_pwm(7, 0, servo_middle)
#    Wheel_Steer(pca, 0)
#    time.sleep(1)
    #pca.set_pwm(7, 0, servo_max)
#    Wheel_Steer(pca, 180)
#    time.sleep(1)


#figuring out max and min PWM for servo
#for i in range(540, 810, 10): 
#    print(i)
#    pca.set_pwm(7, 0, i)
#    time.sleep(1)
