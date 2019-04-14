#https://www.modmypi.com/blog/ds18b20-one-wire-digital-temperature-sensor-and-the-raspberry-pi

#os enables 1-Wire drivers and interface with sensor, time allows Pi to define time.

import os
import time

#load drivers
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#define sensor output file (the w1_slave file) as defined above.
temp_sensor = '/sys/bus/w1/devices/28-031297799716/w1_slave'

#define variable for raw temperature value (temp_raw); process it, we open, read, record.
#Use the return function here, in order to recall at a later stage.
def temp_raw():
    f = open(temp_sensor, 'r')
    lines = f.readlines()
    f.close()
    return lines

#check variable for errors. Strip 1st line except for the last 3 digits, check for the YES signal,
#indicating a successful temp reading: whilst the reading does not equal YES, sleep for 0.2s and repeat.
def read_temp():
    lines = temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = temp_raw()

#proceed to 2nd line of output, find output t=, check for errors, strip the output of the t= phrase
#to leave just the temperature numbers,
#run 2 calculations to give Celsius and Fahrenheit.
    temp_output = lines[1].find('t=')
    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

#loop process and output temperature data every 1 second.

while True:
        print(read_temp())
        time.sleep(1)

