
import RPi.GPIO as GPIO
import time
from datetime import datetime
import argparse
import csv
import sys
import board
import busio
import serial
import adafruit_bme680
from adafruit_pm25.uart import PM25_UART


parser = argparse.ArgumentParser(description='Environmental data logger')
parser.add_argument('--runtime', type=int, default=120, help='Duration to run the script in seconds.')
parser.add_argument('--interval', type=int, default=10, help='Interval for recording data in seconds.')
parser.add_argument('--output', type=str, default='environment_data.csv', help='Filename for saving the output in CSV format.')
args = parser.parse_args()

sensor_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor_pin, GPIO.IN)
radiation_count = 0


i2c = board.I2C()
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)
bme680.sea_level_pressure = 1013.25

uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)
pm25 = PM25_UART(uart, reset_pin=None)

def event_detected(channel):
    global radiation_count
    radiation_count += 1

GPIO.add_event_detect(sensor_pin, GPIO.BOTH, callback=event_detected, bouncetime=50)

def file_exists(filepath):
    try:
        with open(filepath, 'r'):
            return True
    except FileNotFoundError:
        return False

def main_loop():
    write_headers = not file_exists(args.output)
    start_time = time.time()
    initial_time = start_time

    with open(args.output, 'a', newline='') as file:
        writer = csv.writer(file)
        headers = ['Timestamp', 'Radiation Counts', 'Temperature (C)', 'Gas (ohm)', 'Humidity (%)', 'Pressure (hPa)', 'Altitude (m)', 'PM1 (std)', 'PM2.5 (std)', 'PM10 (std)']
        if write_headers:
            writer.writerow(headers)

        while True:
            current_time = time.time()
            if args.runtime > 0 and (current_time - initial_time) > args.runtime:
                break
            if current_time - start_time >= args.interval:
                try:
                  
                    weather_data = [bme680.temperature, bme680.gas, bme680.relative_humidity, bme680.pressure, bme680.altitude]
                    aq_data = pm25.read()
                    aq_data_list = [aq_data["pm10 standard"], aq_data["pm25 standard"], aq_data["pm100 standard"]]
                  
                    radiation_count = 0
                    writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), radiation_count] + weather_data + aq_data_list)
                    
                    start_time = current_time
                except RuntimeError as e:
                    print(f"Error reading from sensor: {e}")

try:
    main_loop()
except KeyboardInterrupt:
    print("Program terminated by user.")
finally:
    GPIO.cleanup()
