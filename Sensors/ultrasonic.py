import time
import argparse
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
from mod4_funcs import ultrasonic_init as u_init
from mod4_funcs import ultrasonic_read

#DEFINE INPUT/OUTPUT PINS
TRIG = 16
ECHO = 18

u_init(TRIG, ECHO)

#configuring argparse for commandline arguments
parser = argparse.ArgumentParser(description='Data for this program.')
parser.add_argument('--tim', action='store', type=int, default=5, help='time for program to run record sensor readings')
parser.add_argument('--delay', action='store', type=float, default = 0.1, help='sample period')
parser.add_argument('--debug', action='store_true', help='specifies if debug statements are printed')
args = parser.parse_args()

start_time = time.time()
cur_time = start_time
mesg_time = start_time

while (start_time + args.tim > cur_time):
    time.sleep(0.01)
    cur_time = time.time()
    if(mesg_time + args.delay < cur_time):
        mesg_time = cur_time
        distance = ultrasonic_read(TRIG, ECHO)
        t = round(cur_time- start_time,2)
        if args.debug: 
            print (f'Distance: {distance:.2f} cm \t Time: {t} seconds')
        else:
            print(f'Distance: {distance:.2f} cm')
GPIO.cleanup()
