#import motor shit
#calibaret magnetometer
import L1_magnetometer as mag                                      # retrieve magnetometer info
import numpy as np                                  # library for math operations
import time                                       # library for time access
import L2_speed_control as sc
import L1_motors as m


highX=0
lowX=0
highY=0
lowY=0
speeds=[1,-1]

#data = np.take(mag.magRead(), [0, 1]) 

if __name__ == "__main__":
    print("10 sec delay")
    time.sleep(10)
    m.MotorL(1) # send command to motors
    m.MotorR(-1) # send command to motors
    time.sleep(1)
    for t in range (0,60):
        print("calibrating magnetometer")
        
        magXYZ=mag.magRead();
       # print("x: {0:2.2f}, y: {1:2.2f}, z: {2:2.2f} uTesla".format(magXYZ[0],magXYZ[1],magXYZ[2]))
        if(magXYZ[0] > highX):
            highX = magXYZ[0]
            
        if(magXYZ[1] > highY):
            highY = magXYZ[0]
          
        if(magXYZ[0] < lowX):
            lowX = magXYZ[1]
            
        if(magXYZ[1] < lowY):
            lowY = magXYZ[1]
    
        time.sleep(.5)
        
    m.MotorL(-1) # send command to motors
    m.MotorR(1) # send command to motors
    time.sleep(1)
    for t in range (0,60):
        print("calibrating magnetometer")
        
        magXYZ=mag.magRead();
       # print("x: {0:2.2f}, y: {1:2.2f}, z: {2:2.2f} uTesla".format(magXYZ[0],magXYZ[1],magXYZ[2]))
        if(magXYZ[0] > highX):
            highX = magXYZ[0]
            
        if(magXYZ[1] > highY):
            highY = magXYZ[1]
          
        if(magXYZ[0] < lowX):
            lowX = magXYZ[0]
            
        if(magXYZ[1] < lowY):
            lowY = magXYZ[1]
    
        time.sleep(.5) 
    m.MotorL(0) # send command to motors
    m.MotorR(0) # send command to motors    
    print("X low: ", lowX, "X high: ", highX, "Y low: ", lowY, "Y high: ", highY)
    print("Please enter these values into L2_heading.py")
