import RPi.GPIO as GPIO
import time
from datetime import datetime
import argparse
import csv  

parser = argparse.ArgumentParser(description='Radiation event logger')
parser.add_argument('--runtime', type=int, default=120, help='Duration to run the script in seconds.')
parser.add_argument('--interval', type=int, default=10, help='Interval for recording counts in seconds.')
parser.add_argument('--output', type=str, default='raw_source.csv', help='Filename for saving the output in CSV format.')
args = parser.parse_args()

sensor_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor_pin, GPIO.IN)

count = 0

def event_detected(channel):
    global count
    count += 1
    print(f"Event detected at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

GPIO.add_event_detect(sensor_pin, GPIO.BOTH, callback=event_detected, bouncetime=50)

def file_exists(filepath):
    try:
        with open(filepath, 'r'):
            return True
    except FileNotFoundError:
        return False

def main_loop():
    global count
    start_time = time.time()
    initial_time = start_time
    write_headers = not file_exists(args.output)
    while True:
        current_time = time.time()
        if args.runtime > 0 and (current_time - initial_time) > args.runtime:
            break
        if current_time - start_time >= args.interval:
            print(f"Counts in the last {args.interval} seconds: {count}")
            with open(args.output, 'a', newline='') as file:
                writer = csv.writer(file)
                if write_headers:
                    writer.writerow(['Timestamp', 'Counts'])
                    write_headers = False 
                writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), count])
            count = 0
            start_time = current_time

try:
    main_loop()
except KeyboardInterrupt:
    print("Program terminated by user.")
finally:
    GPIO.cleanup()

