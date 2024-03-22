# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rwcdHwTGBf5LxqE1HSQtXt5VmTet0RJW
"""

# -*- coding: utf-8 -*-
"""W10.ipynb
Automatically generated by Colaboratory.
Original file is located at
    https://colab.research.google.com/drive/1ECHHEzBeE0oT5IFSLb6Cs4Vw79Iw9tBr
"""

import RPi.GPIO as GPIO
import time
from datetime import datetime
import argparse

# Setup command line arguments
parser = argparse.ArgumentParser(description='Radiation event logger')
parser.add_argument('--runtime', type=int, default=120, help='Duration to run the script in seconds. Default is 120 seconds.')
parser.add_argument('--interval', type=int, default=10, help='Interval for recording counts in seconds. Default is 10 seconds.')
parser.add_argument('--output', type=str, default='radiation_counts.txt', help='Filename for saving the output.')
args = parser.parse_args()

# GPIO setup
sensor_pin = 17  # Change according to your sensor connection
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Variables for event counting
count = 0
start_time = time.time()

# Callback function to execute on GPIO falling edge detection
def event_detected(channel):
    global count
    count += 1
    print(f"Event detected at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Setup event detection
GPIO.add_event_detect(sensor_pin, GPIO.FALLING, callback=event_detected, bouncetime=100)

# Function to handle the main loop and data logging
def main_loop():
    global count, start_time
    initial_time = time.time()
    while True:
        current_time = time.time()
        # Check if the runtime limit has been reached
        if args.runtime > 0 and (current_time - initial_time) > args.runtime:
            break
        # Check if the count interval has been reached
        if current_time - start_time >= args.interval:
            print(f"Counts in the last {args.interval} seconds: {count}")
            with open(args.output, 'a') as file:
                file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, Counts: {count}\n")
            count = 0  # Reset the count after logging
            start_time = current_time  # Reset the start time for the next interval

try:
    main_loop()
except KeyboardInterrupt:
    print("Program terminated by user.")
finally:
    GPIO.cleanup()  # Clean up GPIO to ensure we reset the pin configurations