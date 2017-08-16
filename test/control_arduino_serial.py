import time

import serial

"""
Code for testing bluetooth connection to arduino. It's not used in the application 
TODO : to be deteled later
"""

class Arduino_Connection:
    def __init__(self, serial_address, baude_rate):
        self.serial_address = serial_address
        self.baude_rate = baude_rate
        # self.ser =  serial.Serial('/dev/ttyACM0', 9600)
        self.ser = serial.Serial(self.serial_address, self.baude_rate)

    def forward(self):
        self.ser.write('F')

    def backward(self):
        self.ser.write('B')

    def stop(self):
        self.ser.write('S')

    def right(self):
        self.ser.write('R')

    def left(self):
        self.ser.write('L')


# ard = Arduino_Connection('/dev/ttyACM0', 9600)
ard = Arduino_Connection('/dev/rfcomm1', 38400)

while True:
    ard.forward()
    time.sleep(1)
    ard.backward()
    time.sleep(1)
    ard.right()
    time.sleep(1)
    ard.left()
    time.sleep(1)
    ard.stop()
    time.sleep(1)
