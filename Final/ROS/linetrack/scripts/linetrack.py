#!/usr/bin/env python
from std_msgs.msg import Float32MultiArray
import rospy
import smbus
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

def talker(): 
   pub = rospy.Publisher('linetrack_topic', Float32MultiArray, queue_size=10)
   rospy.init_node('linetrack_talk', anonymous=True)
   rate = rospy.Rate(5)
   while not rospy.is_shutdown():
      mat = Float32MultiArray()
      mat.data = []
      time.sleep(0.1)
      mat.data = linetrack_read(IR1, IR2, IR3, IR4, IR5)
      rospy.loginfo(mat)
      pub.publish(mat)
      rate.sleep


# initializing linetracker
linetrack_init(IR1, IR2, IR3, IR4, IR5)

if __name__ == '__main__':
   try: 
      talker()
   except rospy.ROSInterruptException: 
      pass

GPIO.cleanup()

