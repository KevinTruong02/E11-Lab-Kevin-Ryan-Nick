import csv
import time

meta_data= ["Time", "PM1", "PM2.5", "PM10"]

file = open("aq_data.csv", "w", newline='')

writer= csv.writer(file)
writer.writerow(meta_data)


# SPDX-License-Identifier: MIT

"""
Example sketch to connect to PM2.5 sensor with UART.
"""

import time
import board
import busio
import serial
from adafruit_pm25.uart import PM25_UART

reset_pin = None

uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)

pm25 = PM25_UART(uart, reset_pin)

print("Found PM2.5 sensor, reading data...")

start_time = time.time() 
while True:
    try:
        aqdata = pm25.read()
    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        continue
    datalist= [time.time(), aqdata["pm10 standard"], aqdata["pm25 standard"], aqdata["pm100 standard"]]
    writer.writerow(datalist)
    print()
    print("Concentration Units (standard)")
    print("---------------------------------------")
    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 standard"], aqdata["pm25 standard"], aqdata["pm100 standard"])
    )
    print("Concentration Units (environmental)")
    print("---------------------------------------")
    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 env"], aqdata["pm25 env"], aqdata["pm100 env"])
    )
    #print("---------------------------------------")
    #print("Particles > 0.3um / 0.1L air:", aqdata["particles 03um"])
    #print("Particles > 0.5um / 0.1L air:", aqdata["particles 05um"])
    #print("Particles > 1.0um / 0.1L air:", aqdata["particles 10um"])
    #print("Particles > 2.5um / 0.1L air:", aqdata["particles 25um"])
    #print("Particles > 5.0um / 0.1L air:", aqdata["particles 50um"])
    #print("Particles > 10 um / 0.1L air:", aqdata["particles 100um"])
    #print("---------------------------------------")

    elapsed_time = time.time() - start_time
    print(elapsed_time)
    if elapsed_time >= 30:
        print("30 seconds elapsed. Exiting loop.")
        break

    time.sleep(1)  


