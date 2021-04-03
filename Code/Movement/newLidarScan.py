#Author: Jesse Rosart-Brodnitz
#Contact: jorbaustin@gmail.com

#Level 1 lidar scanning code. This uses ethernet to communicate with the TiM 781 and 561
#this code replaces the L1_lidar code and can be used in place.
#Any level 2 code that imports the L1_lidar should be updated with newLidarScan instead
#requires the tim561_lidar_driver. This can be sourced at https://github.com/cvra/tim561_lidar_driver
import socket
from sicktim561driver import *
import numpy as np
import time

#scan starts on right of lidar, neg 135

TIM561_START_ANGLE = 2.3561944902   # -135° in rad
TIM561_STOP_ANGLE = -2.3561944902   #  135° in rad

Resolution=.3329


def polarScan():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #creates socket connection
    s.connect(("192.168.0.1", 2112))                   #connects to the lidar over socket
    s.send(b'\x02sEN LMDscandata 1\x03\0')              #send command over socket to gather all the Data output. 

    datagrams_generator = datagrams_from_socket(s)      #sets up data structure for transport

    for i in range(1,3):                                 #for loop to control data collection
        datagram = next(datagrams_generator)  
        decoded = decode_datagram(datagram)
        
        if decoded is not None:

            data=np.transpose(decoded['Data'])           #grabs the distance measurements out of LMDscandata only. 
            dataOut=[]                                   #initialize array to hold angle
            count = 0                                    #initialize count to hold row number
            for q in range(0,811):                       #iterates through each row in array
                count += 1
                j = count
                dataOut=np.append(dataOut, round(((j*Resolution)+(-135)),1))   #calculates angle based on loop count and resolution and inserts into array
            output=np.stack((data, dataOut), axis=1)     #appends the angle to the distance [distance, angle]
            return(output)   

if __name__ == '__main__':
    while(True):
        print(polarScan())
        time.sleep(2)

