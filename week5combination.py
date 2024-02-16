# -*- coding: utf-8 -*-
"""week5combination.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1h-QGc3Sr0-JrWFH5MN7WIDHgveIK_nS9
"""

import sys
import csv
import time
import board
import busio
import serial
import adafruit_bme680
from adafruit_pm25.uart import PM25_UART

# Function to parse command-line arguments
def parse_arguments():
    run_time = 30  # Default run time is 30 seconds
    filename = "sensor_data.csv"  # Default filename

    if len(sys.argv) > 1:
        run_time = int(sys.argv[1])

    if len(sys.argv) > 2:
        filename = sys.argv[2]

    return run_time, filename

# Create sensor objects
i2c = board.I2C()
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)
bme680.sea_level_pressure = 1013.25

uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)
pm25 = PM25_UART(uart, reset_pin=None)

# Initialize CSV file and writer
run_time, filename = parse_arguments()
file = open(filename, "w", newline='')
writer = csv.writer(file)

# Write headers
weather_headers = ["Time", "Temperature (C)", "Gas (ohm)", "Humidity (%)", "Pressure (hPa)", "Altitude (m)"]
aq_headers = ["Time", "PM1 (std)", "PM2.5 (std)", "PM10 (std)"]
writer.writerow(weather_headers + aq_headers)

start_time = time.time()
while (time.time() - start_time) < run_time:
    try:
        # Read data from weather sensor
        weather_data = [time.time(), bme680.temperature, bme680.gas, bme680.relative_humidity, bme680.pressure, bme680.altitude]

        # Read data from air quality sensor
        aq_data = pm25.read()
        aq_data_list = [aq_data["pm10 standard"], aq_data["pm25 standard"], aq_data["pm100 standard"]]

        # Write combined data to CSV
        writer.writerow(weather_data + aq_data_list)

        # Print data (optional)
        print("Weather Data:", weather_data)
        print("Air Quality Data:", aq_data_list)

    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        continue

    time.sleep(1)

# Close the CSV file
file.close()