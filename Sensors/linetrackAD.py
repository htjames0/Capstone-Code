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
      IR1 = mcp.read_adc(0) #read c0
      IR2 = mcp.read_adc(1)
      IR3 = mcp.read_adc(2)
      IR4 = mcp.read_adc(3)
      IR5 = mcp.read_adc(4)
      IR6 = mcp.read_adc(5)
      t = round(cur_time- start_time,2)

      print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
      #print(f"{t}s:\tTMP={TMP_Val},\tRES={RES_Val}")
      print(f"{t}\tRES={RES_Val}")

GPIO.cleanup()
