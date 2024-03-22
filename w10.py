import RPi.GPIO as GPIO
import time
from datetime import datetime
import argparse


parser = argparse.ArgumentParser(description='Radiation event logger')
parser.add_argument('--runtime', type=int, default=120, help='Duration to run the script in seconds. Default is 120 seconds.')
parser.add_argument('--interval', type=int, default=10, help='Interval for recording counts in seconds is now used for detailed event logging, not just summary counts.')
parser.add_argument('--output', type=str, default='radiation_counts.txt', help='Filename for saving the output.')
args = parser.parse_args()


sensor_pin = 17 
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


count = 0
events = []


def event_detected(channel):
    global count, events
    count += 1
    event_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    events.append(f"{event_time}, Event\n")
    print(f"Event detected at: {event_time}")


GPIO.add_event_detect(sensor_pin, GPIO.FALLING, callback=event_detected, bouncetime=10)  # Further reduced bouncetime for sensitivity


def log_events():
    with open(args.output, 'a') as file:
        for event in events:
            file.write(event)


def main_loop():
    initial_time = time.time()
    try:
        while True:
            current_time = time.time()
            if args.runtime > 0 and (current_time - initial_time) > args.runtime:
                break
    finally:
        log_events()  # Log events at the end or on interrupt

try:
    main_loop()
except KeyboardInterrupt:
    print("Program terminated by user.")
finally:
    GPIO.cleanup() 
