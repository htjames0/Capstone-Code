import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
import adafruit_mcp3xxx.analog_in as AnalogIn
import busio
import sys
import time
import argparse
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import math
import RPi.GPIO as GPIO
#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BOARD)

#configuring argparse for commandline arguments
parser = argparse.ArgumentParser(description='Data for this program.')
parser.add_argument('--tim', action='store', type=int, default=10, help='time for program to run record sensor readings')
parser.add_argument('--period', action='store', type=float, default = 0.25, help='sample period')
parser.add_argument('--debug', action='store_true', help='specifies if debug statements are printed')
args = parser.parse_args()

if args.debug:
  print(f'arguments: {vars(args)}')


#functions

#def readTrack(j=5):
#    IR = [0]*j
#    for i in range(j):
#        IR[i] = mcp.read_adc(i)
#    return IR

def readTrack2():
    IR = [0]*5
    IR[0] = AnalogIn(mcp, MCP.P0)
    IR[1] = AnalogIn(mcp, MCP.P1).value
    IR[2] = AnalogIn(mcp, MCP.P2).value
    IR[3] = AnalogIn(mcp, MCP.P3).value
    IR[4] = AnalogIn(mcp, MCP.P4).value

    offon = [0]*5
    for i in range(5):
        if IR[i] > 700:
            offon[i] = 0
        else:
            offon[i] = 1
    return offon, IR 

# Hardware SPI configuration:
#SPI_PORT   = 0
#SPI_DEVICE = 0
#mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs =  digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)


start_time = time.time()
cur_time = start_time
mesg_time = start_time

while (start_time + args.tim > cur_time):
    time.sleep(0.01)
    cur_time = time.time()
    if(mesg_time + args.period < cur_time):
      mesg_time = cur_time
      t = round(cur_time- start_time,2)
      print(AnalogIn(mcp, MCP.P0))
      #offon, IR = readTrack2()
      #w = 0*IR[0] + 1000*IR[1] + 2000*IR[2] + 3000*IR[3] + 4000*IR[4]
      #s = IR[0] + IR[1] + IR[2] + IR[3] + IR[4]
      #y = round(w/s,3) 
      #print('Y = ')
      #print(y)
      #print('IR is:')
      #print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4}'.format(*IR))
      #print('offon is:')
      #print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4}'.format(*offon))
      #print(f"{t}s:\tTMP={TMP_Val},\tRES={RES_Val}")
      #print(f"{t}\tRES={RES_Val}")

#GPIO.cleanup()
