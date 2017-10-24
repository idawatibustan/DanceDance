#!/usr/bin/env python

import serial
import time

test=serial.Serial("/dev/ttyACM0",9600)
if(test.isOpen() == False):
    test.open()

print "ready: serial isopen = ", test.isOpen()
try:
    print "waiting"
    while True:
        for i in range(5):
             line = test.readline()
             print str(i) ,line
        time.sleep(1)
                
except KeyboardInterrupt:
    pass # do cleanup here

test.close()