#!/usr/bin/env python

import time
import argparse
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
import rospy
from std_msgs.msg import Float64


# ULTRASONIC FUNCTIONS
def ultrasonic_init(Trigger, Echo):
    # set up the input and output pins
    GPIO.setup(Trigger, GPIO.OUT)
    GPIO.output(Trigger, False)
    GPIO.setup(Echo, GPIO.IN)
    # let the sensor initialize
    time.sleep(.5)

def ultrasonic_read(Trigger, Echo):
    maxTime = 0.04 
    # trigger a reading
    GPIO.output(Trigger, True)
    time.sleep(0.00001)
    GPIO.output(Trigger, False)

    # find the start and end of the ultrasonic pulse
    pulse_start = time.time()
    timeout = pulse_start + maxTime
    while GPIO.input(Echo) == 0 and pulse_start < timeout:
        pulse_start = time.time()

    pulse_end = time.time()
    timeout = pulse_end + maxTime
    while GPIO.input(Echo) == 1 and pulse_end < timeout:
        pulse_end = time.time()

    # Speed of sound 34300 cm/sec
    total_distance = (pulse_end - pulse_start) * 34300
    # Divide by 2, account for return trip for signal
    return round(total_distance/2, 1) 
    
#defining Input/Output Pins 
TRIG = 16
ECHO = 18

#initializing Pi GPIO Pins
ultrasonic_init(TRIG, ECHO)

def talker():
   pub = rospy.Publisher('ultra_topic', Float64, queue_size=10)
   rospy.init_node('ultra_talk', anonymous=True)
   rate = rospy.Rate(10) # 10hz
   
   ITER_COUNT = 400
   interval = 0.2
   #DEBUG = False

   #if "-debug" in sys.argv:
   #   DEBUG = True

   while not rospy.is_shutdown():
      while ITER_COUNT > 0:
         ITER_COUNT -= interval
         time.sleep(0.00001)
         dist = ultrasonic_read(TRIG, ECHO)  #distance reading using GPIO from Pi
         #rospy.loginfo(dist)
         print(dist)
         pub.publish(dist)
         rate.sleep()
   GPIO.cleanup()

if __name__ == '__main__':
   try: 
      talker()
   except rospy.ROSInterruptException:
      pass 

GPIO.cleanup()

