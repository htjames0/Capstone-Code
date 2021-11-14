import time
import argparse
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import math
#import RPi.GPIO as GPIO
#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BOARD)

#DEFINING PINS
#LED = 11 #GPIO 17

#GPIO.setup(LED, GPIO.OUT, initial = GPIO.LOW) 

#configuring argparse for commandline arguments
parser = argparse.ArgumentParser(description='Data for this program.')
parser.add_argument('--tim', action='store', type=int, default=10, help='time for program to run record sensor readings')
parser.add_argument('--period', action='store', type=float, default = 0.25, help='sample period')
parser.add_argument('--debug', action='store_true', help='specifies if debug statements are printed')
args = parser.parse_args()

if args.debug:
  print(f'arguments: {vars(args)}')


#functions

def readTrack(j=5):
    IR = [0]*j
    for i in range(j):
        IR[i] = mcp.read_adc(i)
    return IR


#def weightedAvg(IR): 
#    sum = 0 
#    w_sum = 0
#    weights = list(range(0,len(IR)+1)*1000
#
#    for i in range(0, len(IR)):
#        w_sum  = w_sum + weight[i]*IR[i]
#        sum = sum + IR[i]
#
#
#
#
#    return w/s

def PID(pos, prev_pos, Kp, Ki, Kd): 
    prop =  pos - 2000
    derv = prop - prev_pos
    inte += prop

    power = prop * Kp +  inte * Ki + derv * Kd

    return power

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))


start_time = time.time()
cur_time = start_time
mesg_time = start_time

while (start_time + args.tim > cur_time):
    time.sleep(0.01)
    cur_time = time.time()
    if(mesg_time + args.period < cur_time):
      mesg_time = cur_time
      t = round(cur_time- start_time,2)
      IR = readTrack()
      w = 0*IR[0] + 1000*IR[1] + 2000*IR[2] + 3000*IR[3] + 4000*IR[4]
      s = IR[0] + IR[1] + IR[2] + IR[3] + IR[4]
      y = round(w/s,3) 
      print('Y = ')
      print(y)
      print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4}'.format(*IR))
      #print(f"{t}s:\tTMP={TMP_Val},\tRES={RES_Val}")
      #print(f"{t}\tRES={RES_Val}")

#GPIO.cleanup()
