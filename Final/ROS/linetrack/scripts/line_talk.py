#!/usr/bin/env python
import sys
import time
import argparse
import math
import RPi.GPIO as GPIO
import busio 
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import rospy
from std_msgs.msg import String

#initializing AD
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs =  digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)

#time.sleep(0.5)

def readTrack():
   IR = [0]*5
   offon = [0]*5

   IR[0] = AnalogIn(mcp, MCP.P0).value
   IR[1] = AnalogIn(mcp, MCP.P1).value
   IR[2] = AnalogIn(mcp, MCP.P2).value
   IR[3] = AnalogIn(mcp, MCP.P3).value
   IR[4] = AnalogIn(mcp, MCP.P4).value

   for i in range(5):
      if IR[i] > 10000:
         offon[i] =0
      else:
         offon[i] = 1
   return offon, IR


def talker():
   pub = rospy.Publisher('line_topic', String, queue_size=10)
   rospy.init_node('line_talk', anonymous=True)
   rate = rospy.Rate(10) # 10hz

   i = 0
   while i < 10000:
      print(i)
      i +=1
      binary, analog = readTrack()
      print(binary)
      print(analog)
      pub.publish(str(binary))
      rate.sleep()

if __name__ == '__main__':
   try:
      talker()
   except rospy.ROSInterruptException:
      pass
