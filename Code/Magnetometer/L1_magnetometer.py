#Author: Jesse Rosart-Brodnitz
#Contact: jorbaustin@gmail.com

#function to read magnetometer over I2C
#returns unfiltered xyz
#address is 0x1e
#requires adafruit_lis2mdl libbrary

import time
import board
import busio
import adafruit_lis2mdl


i2c=busio.I2C(board.SCL, board.SDA)  #reads from i2c ports   

sensor=adafruit_lis2mdl.LIS2MDL(i2c) #declares device within library and means of connection

def magRead():#callable function to return raw magnet readings
    mag_x, mag_y, mag_z = sensor.magnetic#reads from sensor
    mag=[mag_x, mag_y, mag_z]#assings to array for storage
    return(mag)#

if __name__ == "__main__":
    while True:
        magXYZ=magRead();
        print("x: {0:2.2f}, y: {1:2.2f}, z: {2:2.2f} uTesla".format(magXYZ[0],magXYZ[1],magXYZ[2]))
        time.sleep(.5)
