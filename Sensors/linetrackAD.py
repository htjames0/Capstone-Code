import time
import argparse
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

#DEFINING PINS
LED = 11 #GPIO 17

GPIO.setup(LED, GPIO.OUT, initial = GPIO.LOW) 

#configuring argparse for commandline arguments
parser = argparse.ArgumentParser(description='Data for this program.')
parser.add_argument('--tim', action='store', type=int, default=10, help='time for program to run record sensor readings')
parser.add_argument('--period', action='store', type=float, default = 0.25, help='sample period')
parser.add_argument('--debug', action='store_true', help='specifies if debug statements are printed')
args = parser.parse_args()

if args.debug:
  print(f'arguments: {vars(args)}')


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
      IR = [0]*5
      for i in range(5): 
        IR[i] = mcp.read_adc(i)
      t = round(cur_time- start_time,2)
      y = (0*IR[0] + 1000*IR[1] + 2000*IR[2] + 3000*IR[3] + 4000*IR[4])/(IR[0] + IR[1] + IR[2] + IR[3] + IR[4])
      print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4}'.format(*IR))
      print(y)
      #print(f"{t}s:\tTMP={TMP_Val},\tRES={RES_Val}")
      #print(f"{t}\tRES={RES_Val}")

GPIO.cleanup()
