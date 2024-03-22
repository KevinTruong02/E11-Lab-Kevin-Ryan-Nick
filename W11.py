import RPi.GPIO as GPIO
import time
from datetime import datetime
import argparse
import csv  # Import the CSV module for handling CSV file operations

# Setup command line arguments
parser = argparse.ArgumentParser(description='Radiation event logger')
parser.add_argument('--runtime', type=int, default=120, help='Duration to run the script in seconds.')
parser.add_argument('--interval', type=int, default=10, help='Interval for recording counts in seconds.')
# Change default filename to raw_source.csv for CSV format output
parser.add_argument('--output', type=str, default='raw_source.csv', help='Filename for saving the output in CSV format.')
args = parser.parse_args()

# GPIO setup
sensor_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor_pin, GPIO.IN)

# Variables for event counting
count = 0

# Callback function to execute on GPIO edge detection
def event_detected(channel):
    global count
    count += 1
    print(f"Event detected at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Setup event detection with both edges and reduced bouncetime
GPIO.add_event_detect(sensor_pin, GPIO.BOTH, callback=event_detected, bouncetime=50)

# Check if the file exists to determine if headers should be written
def file_exists(filepath):
    try:
        with open(filepath, 'r'):
            return True
    except FileNotFoundError:
        return False

# Function to handle the main loop and data logging
def main_loop():
    global count
    start_time = time.time()
    initial_time = start_time
    # Check if we need to write headers (file does not exist)
    write_headers = not file_exists(args.output)
    while True:
        current_time = time.time()
        if args.runtime > 0 and (current_time - initial_time) > args.runtime:
            break
        if current_time - start_time >= args.interval:
            print(f"Counts in the last {args.interval} seconds: {count}")
            # Open the file in append mode and use the csv.writer to write data
            with open(args.output, 'a', newline='') as file:
                writer = csv.writer(file)
                # Write headers if the file was just created
                if write_headers:
                    writer.writerow(['Timestamp', 'Counts'])
                    write_headers = False  # Ensure headers are not written again
                writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), count])
            count = 0
            start_time = current_time

try:
    main_loop()
except KeyboardInterrupt:
    print("Program terminated by user.")
finally:
    GPIO.cleanup()

