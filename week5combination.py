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


def parse_arguments():
    run_time = 30  # Default run time is 30 seconds
    filename = "sensor_data.csv"  # Default filename

    if len(sys.argv) > 1:
        run_time = int(sys.argv[1])

    if len(sys.argv) > 2:
        filename = sys.argv[2]

    return run_time, filename


i2c = board.I2C()
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)
bme680.sea_level_pressure = 1013.25

uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)
pm25 = PM25_UART(uart, reset_pin=None)


run_time, filename = parse_arguments()
file = open(filename, "w", newline='')
writer = csv.writer(file)


weather_headers = ["Time", "Temperature (C)", "Gas (ohm)", "Humidity (%)", "Pressure (hPa)", "Altitude (m)"]
aq_headers = ["Time", "PM1 (std)", "PM2.5 (std)", "PM10 (std)"]
writer.writerow(weather_headers + aq_headers)

start_time = time.time()
while (time.time() - start_time) < run_time:
    try:
        
        weather_data = [time.time(), bme680.temperature, bme680.gas, bme680.relative_humidity, bme680.pressure, bme680.altitude]

        
        aq_data = pm25.read()
        aq_data_list = [aq_data["pm10 standard"], aq_data["pm25 standard"], aq_data["pm100 standard"]]

   
        writer.writerow(weather_data + aq_data_list)

       
        print("Weather Data:", weather_data)
        print("Air Quality Data:", aq_data_list)

    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        continue

    time.sleep(1)


file.close()