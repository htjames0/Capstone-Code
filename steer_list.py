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


#history = [0,0,0,0,0]
#changes = []

def callback(data):
  #global history
  #global changes
  #changes = []

#initialize 
  turn = 0

  read = data.data
  read = [float(read[1]), float(read[4]), float(read[7]), float(read[10]), float(read[13])]
  print(read)

  #history.append(arr)
  #prev = history[-2]

  #for i in range(5):
  #if prev is not read:
  #if True:
  if read[2] == 0 :                                    #it is over the black
   print('I got here 3 = 0')
   if read[1] == 0 and read[3] == 0:                      # good
      turn += 0
   if read[1] == 0 and read[3] == 1:                      # small turn left
      turn += 1
   if read[1] == 1 and read[3] == 0:                      # small turn right
      turn -= 1
  elif read[2] == 1:                                  #it is not over the black
   print('I got here 3 = 1')
   if read[3] == 1 and read[1] == 1:
      if read[0] == 1:
         turn = turn + 3                                  # large turn left
      if read[0] == 0:
         turn = turn - 3                                  # large turn right
   if read[3] == 0 and read[1] == 1:
      turn = turn + 2                                     # medium turn left
   if read[3] == 1 and read[1] == 0:
      turn = turn - 1                                     # medium turn right
   if read[3] == 1 and read[1] == 1 and read[0] == 1 and read[4] == 1:
      turn  = turn   # stop motor for right now might rely on previous  
  else:
      turn += 0

  print("turn: %d" % turn)

  if turn < 0:  # turn right
      print("turn left")
      Wheel_Steer(pca, 135)
  if turn > 0:
      print("turn right")
      Wheel_Steer(pca, 45)
  if turn == 0:
      print("no turn")
      #Wheel_Steer(pca, servo_middle)

  turn = 0
  #last = read 


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
