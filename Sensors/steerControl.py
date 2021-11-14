import time
import argparse
import math
#AD/Linetrack
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
#Motor
from adafruit_pca9685 import PCA9685
import busio
from board import SCL, SDA
#Ultrasonic
import RPi.GPIO as GPIO
from mod4_funcs import ultrasonic_init as u_init
from mod4_funcs import ultrasonic_read
GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(LED, GPIO.OUT, initial = GPIO.LOW) 


# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

#Ultrasonic INPUT/OUTPUT Pin configuration
TRIG = 16
ECHO = 18

#configuring argparse for commandline arguments
parser = argparse.ArgumentParser(description='Data for this program.')
parser.add_argument('--tim', action='store', type=int, default=10, help='time for program to run record sensor readings')
parser.add_argument('--line_delay', action='store', type=float, default = 0.25, help='sample period')
parser.add_argument('--ultr_delay', action='store', type=float, default = 0.1, help='sample period')
parser.add_argument('--debug', action='store_true', help='specifies if debug statements are printed')
parser.add_argument('--KP', action = 'store', type = float, default = 0, help = 'the proportional control constant')
parser.add_argument('--KI', action = 'store', type = float, default = 0, help = 'the integral control constant')
parser.add_argument('--KD', action = 'store', type = float, default = 0, help = 'the derivative control constant')
args = parser.parse_args()

if args.debug:
  print(f'arguments: {vars(args)}')


#functions

def readTrack(j=5):
    IR = [0]*j
    for i in range(0, j):
        IR[i] = mcp.read_adc(i)
    return IR


def weightedAvg(IR): 
    s = 0 
    w = 0
    weights = list(range(0,len(IR)+1))
    for i in range(len(IR)):
        w =  w + weights[i]*1000*IR[i]
        s =  s + IR[i]
    return w/s

def PID(pos, prev_pos, Kp, Ki, Kd): 
    prop =  pos - 2000
    derv = prop - prev_pos
    inte += prop

    power = prop * Kp +  inte * Ki + derv * Kd

    return power

def Servo_Initialize(): 
    i2c = busio.I2C(SCL, SDA)
    pca = PCA9685(i2c)
    pca.frequency = 100
    return pca

def Wheel_Steer(pca, angle):
    if angle > 180:
        angle = 180
    if angle < 0:
        angle = 0
    duty = floor((angle/180)*270+540)
    pca.set_pwm(7, 0, duty)

#initialization
pca = Servo_Initialize()
u_init(TRIG, ECHO)



start_time = time.time()
cur_time = start_time
line_idx = 0
ultr_idx = 0

while (start_time + args.tim > cur_time):
    #time.sleep(0.01)
    cur_time = time.time()
    if(start_time + line_idx*args.line_delay < cur_time):
      line_idx += 1
      IR = readTrack()
      y = weightedAvg(IR)
      #dist = ultrasonic_read(TRIG, ECHO)
      print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4}'.format(*IR))
      print(y)
    #if(start_time + ultr_idx*args.ultr_delay < cur_time):
    #  ultr_idx += 1
    #  mesg_time = cur_tim
    #  t = round(cur_time - start_time, 2)
      #dist = ultrasonic_read(TRIG, ECHO)
      #print(dist)














#GPIO.cleanup()
