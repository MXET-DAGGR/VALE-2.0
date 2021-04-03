# Example to read left and right encoders on SCUTTLE.
# Left has address 40 and right has 41
# Code for Pi setup.

import smbus
import time
import numpy as np # use numpy to build the angles array

bus=smbus.SMBus(1)

encL  = 0x40 # encoder i2c address
encR = 0x41 # encoder i2c address (this encoder has A1 pin pulled high)
global go0
global go1
go0 = False
go1 = False
global tick0
global tick1
tick0 = False
tick1 = False

def read():
    #try:
    global tick0
    global tick1
    global go0
    global go1
    x = bus.read_byte_data(encL,0xFE)
    x = ((x << 8) | (x >> 8)) & 0xFFFF
    meas = ((x & 0xFF00) >> 2) | ( x & 0x3F)
    angle0 = meas*0.0219/2 # convert to degrees
    if angle0 <= 15 and go0 == True:
        tick0 = tick0^True
        go0 = False
    if 20 < angle0:
        go0 = True
    if tick0 == True:
        angle0 = angle0 + 180
    #elif go0 == False and tick0 == False:
    #    angle0 = angle0 +180  
        
    #except:
    #    print('Warning (I2C): Could not read left encoder')
    #    angle0 = 0
    #try:
    x = bus.read_byte_data(encR,0xFE)
    print
    x = ((x << 8) | (x >> 8)) & 0xFFFF
    meas = ((x & 0xFF00) >> 2) | ( x & 0x3F)
    angle1 = meas*0.0219/2 # convert to degrees
    if angle1 <= 15 and go1 == True:
        tick1 = tick1^True
        go1 = False
    if 20 < angle1:
        go1 = True
    if tick1 == True:
        angle1 = angle1 + 180
    #elif go1 == False and tick1 == False:
    #    angle1 = angle1 +180  
        
    #except:
    #    print('Warning (I2C): Could not read right encoder')
    #    angle1 = 0
    angles = np.array([angle0,angle1])
    return angles
    

if __name__ == "__main__":

# UNCOMMENT THIS SECTION TO USE ENCODER_EX2.PY AS A STANDALONE PROGRAM
# ------------------------------------------------------------------------------
    while 1:
         encValues = read()# read the values.  Reading will only change if you move the motors
         # round the values and print them separated by a tab
         print("Left: ",round(encValues[0],3),"\t","Right: ",round(encValues[1],3))
         print("Tick0: ", tick0, "\tTick1: ", tick1)

         time.sleep(0.1)

