import numpy as np
import time
import L1_encoder as enc   #the imported file was provided through the MXET 300 class. 
import math
wait=.02
R = 0.041                                   # radius in meters
L = 0.201                                   # half of wheelbase meters
res = (360/2**14)                           # resolution of the encoders
roll = int(360/res)                         # variable for rollover logic
gap = 0.5 * roll                            # degress specified as limit for rollover
speedRatio=.5

def odometry(xpos, ypos, theta):
    #meters and degrees
    encoders = enc.read()  # grabs the current encoder readings in degrees
    degL0 = round(encoders[0], 1)
    degR0 = round(encoders[1], 1)
    #t0 = time.time()  # time.time() reports in seconds
    #print(encoders)
    time.sleep(wait)  # delay set forth in header

    encoders = enc.read()  # grabs the current encoder readings in degrees
    degL1 = round(encoders[0], 1)  # rounded reading in degrees.
    degR1 = round(encoders[1], 1)
    #t1 = time.time()
    #print(encoders)
    #delT=t1-t0
    travL=getTravel(degL0,degL1)   #gets delta on each wheel in degrees
    travR=getTravel(degR0,degR1)
    travL= -math.radians(travL)
    travR= math.radians(travR)
    distanceL=getDistance(travL, R)   #gets linear distance traveled on each wheel
    distanceR=getDistance(travR, R)   #gets linear distance traveled on each wheel
    center, phi=position(distanceL, distanceR, L)
    odometry=positionUpdate(center, phi, xpos, ypos, theta)
    #print("x: ", odemetry[1)
    #newPosition=updatedPosition
    
    return odometry

def getTravel(deg0, deg1):                  # calculate the delta on Left wheel
    trav = deg1 - deg0                      # reset the travel reading
    if((-trav) >= gap):                     # if movement is large (has rollover)
        trav = (deg1 - deg0 + roll)         # forward rollover
    if(trav >= gap):
        trav = (deg1 - deg0 - roll)         # reverse rollover
    trav=trav*res*speedRatio
    return(trav)
def getDistance(travel, radius):    #gets linear distance traveled on each wheel
    distanceTraveled=radius*travel
    return(distanceTraveled)

def position(distanceTraveledLeft, distanceTraveledRight, length):  #gets 
    dCenter=(distanceTraveledLeft+distanceTraveledRight)/2
    newTheta = (R * (distanceTraveledRight - distanceTraveledLeft)) / (2 * length)
    print(dCenter, newTheta)
    return (dCenter, newTheta)

def positionUpdate(dCenter, newTheta, oldX, oldY, oldTheta):
    updatedX=oldX+math.cos(oldTheta)*dCenter
    updatedY=oldX+math.sin(oldTheta)*dCenter
    newTheta=newTheta+oldTheta
    newTheta=math.degrees(newTheta)
    #newTheta=localizedAngle(newTheta)
    updated=np.round([updatedX, updatedY, newTheta], 3)
    return updated
def localizedAngle(theta):
    if theta >= 0:
        while theta >= 180:
            theta = theta - 180
        return (theta)
    if theta <= 0:
        while theta <= -180:
            theta = theta + 180
        return (theta)


if __name__ == "__main__":
    x=0
    y=0
    theta=0
    while True:
        location=odometry(x,y,theta)
        x=location[0]
        y=location[1]
        theta=location[2]
        print(x,y,theta)
        