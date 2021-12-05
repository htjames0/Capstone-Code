#!/usr/bin/env python

#imports for Ultraonsic - could get rid of argparse
import time
import argparse
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
#from mod4_funcs import ultrasonic_init as u_init
#from mod4_funcs import ultrasonic_read

#imports for talker - could get rid of string
import rospy
#from std_msgs.msg import String
#import RPi.GPIO as GPIO
#import time
import smbus		    #import SMBus module of I2C
#GPIO.setwarnings(False)     # Ignore warning for now
#GPIO.setmode(GPIO.BOARD)    # Use physical pin numberin

# ULTRASONIC FUNCTIONS
def ultrasonic_init(Trigger, Echo):
    # set up the input and output pins
    GPIO.setup(Trigger, GPIO.OUT)
    GPIO.output(Trigger, False)
    GPIO.setup(Echo, GPIO.IN)
    # let the sensor initialize
    time.sleep(.5)

def ultrasonic_read(Trigger, Echo):
    # trigger a reading
    GPIO.output(Trigger, True)
    time.sleep(0.00001)
    GPIO.output(Trigger, False)

    # find the start and end of the ultrasonic pulse
    while GPIO.input(Echo) == 0:
        start_time = time.time()
    while GPIO.input(Echo) == 1:
        end_time   = time.time()

    # Speed of sound 34300 cm/sec
    total_distance = (end_time - start_time) * 34300
    # Divide by 2, account for return trip for signal
    return round(total_distance/2, 1) 

#defining Input/Output Pins 
TRIG = 16
ECHO = 18

#initializing Pi GPIO Pins
ultrasonic_init(TRIG, ECHO)

def talker():
   pub = rospy.Publisher('ultra_topic', float64, queue_size=10)
   rospy.init_node('ultra_talk', anonymous=True)
   rate = rospy.Rate(10) # 10hz
   while not rospy.is_shutdown():
      dist = ultrasonic_read(TRIG, ECHO)  #distance reading using GPIO from Pi
      rospy.loginfo(dist)
      pub.publish(dist)
      rate.sleep()

if __name__ == '__main__':
   try: 
      talker()
   except rospy.ROSInterruptException:
      pass 

GPIO.cleanup()

