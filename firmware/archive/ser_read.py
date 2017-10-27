#!/usr/bin/env python

import serial
import time

# test=serial.Serial("/dev/ttyACM0",9600) # USB
test = serial.Serial("/dev/ttyAMA0", 9600) # SPI
if(test.isOpen() == False):
    test.open()

try:
    while True:
        for i in range(5):
            line = test.readline()
            print str(i), line
        time.sleep(1)

except KeyboardInterrupt:
    test.close()
    pass # do cleanup here

test.close()
