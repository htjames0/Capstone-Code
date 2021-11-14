import time
import argparse
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import RPi.GPIO as GPIO
from mod4_funcs import ultrasonic_init as u_init
from mod4_funcs import ultrasonic_read

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED, GPIO.OUT, initial = GPIO.LOW) 


# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

#Ultrasonic INPUT/OUTPUT PIN CONFIG
TRIG = 16
ECHO - 18

#configuring argparse for commandline arguments
parser = argparse.ArgumentParser(description='Data for this program.')
parser.add_argument('--tim', action='store', type=int, default=10, help='time for program to run record sensor readings')
parser.add_argument('--line_delay', action='store', type=float, default = 0.25, help='sample period')
parser.add_argument('--ultr_delay', action='store', type=float, default = 0.1, help='sample period')
parser.add_argument('--debug', action='store_true', help='specifies if debug statements are printed')
parser.add_argument('--KP', action = 'store', type = float, default = 0, help = 'the proportional control constant')
parser.add_argument('--KI', action = 'store', type = float, default = 0, help = 'the integral control constant')
parser.add_argument('--KD', action = 'store', type = float, defualt = 0, help = 'the derivative control constant')
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
    #sum = 0 
    #w_sum = 0
    weights = list(range(0,len(IR)+1)*1000

    #for i in range(len(IR)):
    w =  weights[1]*IR[1] + weights[2]*IR[2] + weights[3]*IR[3] + weights[4]*IR[4] + weights[5]*IR[5]
    s = IR[1] + IR[2] + IR[3] + IR[4] + IR[5]

    return w/s

def PID(pos, prev_pos, Kp, Ki, Kd): 
    prop =  pos - 2000
    derv = prop - prev_pos
    inte += prop

    power = prop * Kp +  inte * Ki + derv * Kd

    return power

def Servo_Initialize(): 
    pca = PCA9685()
    pca.set_pwm+freq(100)
    return pca

def Wheel_Steer(pca, angle):
    if angle > 180:
        angle = 180
    if angle < 0:
        angle = 0
    duty = math.floor((angle/180)*270)+540)
    pac.set_pwm(7, 0, duty)


pca = Servo_Initialize()

start_time = time.time()
cur_time = start_time
mesg_time = start_time

while (start_time + args.tim > cur_time):
    time.sleep(0.01)
    cur_time = time.time()
    if(mesg_time + args.period < cur_time):
      mesg_time = cur_time
      t = round(cur_time- start_time,2)

      #ultrasonic read
      dist = ultrasonic_read(TRIG, ECHO)

      #linetrack read
      IR = readTrack()
      y = weightedAvg(IR)

      #perform PID Logic and stop car if needed
      #if dist < 100: 
        #slow down motor

      #if dist < 25: 
        #stop motor

      #else:          
      y = PID(y, 1, 4, 0, 0)
      Wheel_Steer(pca, y)

      print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4}'.format(*IR))
      print(y)
      #print(f"{t}s:\tTMP={TMP_Val},\tRES={RES_Val}")
      #print(f"{t}\tRES={RES_Val}")

GPIO.cleanup()
