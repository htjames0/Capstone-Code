#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import math
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
import time

def Servo_Motor_Initialization():
   i2c_bus = busio.I2C(SCL, SDA)
   pca = PCA9685(i2c_bus)
   pca.frequency = 100
   print("initialized")
   return pca

def Steering(pca, angle, i):
   if angle > 150:
      angle = 150
   if angle < 30:
      angle = 30
   duty = ((angle / 180) * 6553) + 6553
   pca.channels[i].duty_cycle = math.floor(duty)
   print("Steering set up")

pca = Servo_Motor_Initialization()
Steering(pca, 120, 0)
Steering(pca, 50, 2)
Steering(pca, 90, 4)
history = ["[0 0 0 0 0]"]
changes = []

def callback(data):
   global history
   global changes
   history.append(data.data)
   changes = []
   turn = 0

   current = data.data
   last = history[-2]

   #print(last)
   #print(current)
   #print("--------")

   for i in range (10):
      change = ''
      if last[i] is not current[i]:
         sensor = ""
         if i == 1:
            sensor = "1"
         elif i == 3:
            sensor = "2"
         elif i == 5:
            sensor = "3"
         elif i == 7:
            sensor = "4"
         elif i == 9:
            sensor = "5"
         change = sensor + str(current[i])
         changes.append(change)
   if changes:
      print(changes)

   for i in range(len(changes)):
      if current[5] == "1":
         if changes[i] == "51" or changes[i] == "10":
            turn += 1
         elif changes[i] == "11" or changes[i] == "50":
            turn -= 1
      elif current[5] == "0":
         if changes[i] == "51" or changes[i] == "41":
            turn += 1
         elif changes[i] == "21" or changes[i] == "11":
            turn -= 1
         elif changes[i] == "50" and data.data == ["0 0 0 0 0"]:
            turn += 1
         elif changes[i] == "10" and data.data == ["0 0 0 0 0"]:
            turn -= 1

   print("turn: ", turn)
   if turn < 0:
      print("turn left", turn)
      Steering(pca, 120, 4)
   elif turn > 0:
      print("turn right", turn)
      Steering(pca, 70, 4)

   last = current

def listener():
   # In ROS, nodes are uniquely named. If two nodes with the same
   # name are launched, the previous one is kicked off. The
   # anonymous=True flag means that rospy will choose a unique
   # name for our 'listener' node so that multiple listeners can
   # run simultaneously.
   rospy.init_node('steering', anonymous=True)
   rospy.Subscriber("chatter", String, callback)
   # spin() simply keeps python from exiting until this node is stopped
   rospy.spin()

if __name__ == '__main__':
   listener()
