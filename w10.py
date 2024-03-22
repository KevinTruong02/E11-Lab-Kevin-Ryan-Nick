import RPi.GPIO as GPIO
import time
from datetime import datetime
import argparse

# Setup command line arguments
parser = argparse.ArgumentParser(description='Radiation event logger')
parser.add_argument('--runtime', type=int, default=120, help='Duration to run the script in seconds.')
parser.add_argument('--interval', type=int, default=10, help='Interval for recording counts in seconds.')
parser.add_argument('--output', type=str, default='radiation_counts.txt', help='Filename for saving the output.')
args = parser.parse_args()

# GPIO setup
sensor_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor_pin, GPIO.IN)  # Removed pull_up_down for demonstration

# Variables for event counting
count = 0

# Callback function to execute on GPIO edge detection
def event_detected(channel):
    global count
    count += 1
    print(f"Event detected at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Setup event detection with both edges and reduced bouncetime
GPIO.add_event_detect(sensor_pin, GPIO.BOTH, callback=event_detected, bouncetime=50)

# Function to handle the main loop and data logging
def main_loop():
    global count
    start_time = time.time()
    initial_time = start_time
    while True:
        current_time = time.time()
        if args.runtime > 0 and (current_time - initial_time) > args.runtime:
            break
        if current_time - start_time >= args.interval:
            print(f"Counts in the last {args.interval} seconds: {count}")
            with open(args.output, 'a') as file:
                file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, Counts: {count}\n")
            count = 0
            start_time = current_time

try:
    main_loop()
except KeyboardInterrupt:
    print("Program terminated by user.")
finally:
    GPIO.cleanup()

