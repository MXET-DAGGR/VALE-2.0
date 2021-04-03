#Code writen by: Jesse Rosart-Brodnitz
#email: jorbaustin@gmail.com
#import all functions
import numpy as np
import time
#import L2_heading as head  #the imported file was provided through the MXET 300 class. 
import L1_encoder as enc   #the imported file was provided through the MXET 300 class. 
import math




wait = .05

# define robot geometry. Constants measured from robot
R = 0.041  # wheel radius
L = 0.201  # half of the wheelbase
N = 2 * np.pi  #divisons per rotation
res = (359 / 2 ** 14)  # resolution of the encoders
roll = int(359 / res)  # variable for rollover logic   #16384
gap = 0.5 * roll  # degrees specified as limit for rollover

# things trying now:

def task1(x, y, ø):
    ø = ø * np.pi / 180

    encoders = enc.read()
    #print(encoders)
    
    degL0 = round(encoders[0], 1)
    degR0 = round(encoders[1], 1)
    t1 = time.time()  # time.time() reports in seconds

    time.sleep(wait)  # delay set forth in header

    encoders = enc.read()  # grabs the current encoder readings in degrees
    degL1 = round(encoders[0], 1)  # rounded reading in degrees.
    degR1 = round(encoders[1], 1)
    t2 = time.time()

    global deltaT
    deltaT = round((t2 - t1), 3)
    
    travL = (degL1 - degL0)
    if ((-travL) >= gap):  # if movement is large (has rollover)
        travL = (degL1 - degL0 + roll)  # forward rollover
    if (travL >= gap):
        travL = (degL1 - degL0 - roll)  # reverse rollover

    travR = (degR1 - degR0)
    if ((-travR) >= gap):  # if movement is large (has rollover)
        travR = (degL1 - degL0 + roll)  # forward rollover
    if (travR >= gap):
        travR = (degR1 - degR0 - roll)  # reverse rollover
    travL =travL
    travR =travR

    travL = (-travL)

    travL = travL * np.pi / 180
    travR = travR * np.pi / 180

    travL = np.round(travL, 3)
    travR = np.round(travR, 3)

    dL = distanceTraveled(travL, N, R)  # calls funciton to get distance moved on each wheel

    dR = distanceTraveled(travR, N, R)
    print(dL, dR)
    w = positionUpdate(dL, dR, L, x, y, ø)  #updates position based on initial values and distances traveled

    s = summary(w)
    return (s)


def summary(coordinates):  # summarizes information in array
    #summInfo = np.append(coordinates, orientation())
    #return (summInfo)
    return coordinates

def distanceTraveled(traveled, divPerRot, radius):
    D=radius*traveled
    #D = 2 * np.pi * radius * (traveled / divPerRot)  # gets distanced travled. to be used on each travel
    # D=D*39.3701 #converts to inches for debugging.
    return (D)


def positionUpdate(dLeft, dRight, length, oldX, oldY, oldø):
    dCenter = (dLeft + dRight) / 2
    phi = ((dRight - dLeft)) / (2 * length)
    xPrime = oldX + dCenter * math.cos(oldø)
    yPrime = oldY + dCenter * math.sin(oldø)
    phiPrime = oldø + phi

    phiPrime = phiPrime * 180 / np.pi  # converts to degrees

    xPrime = round(xPrime, 3)
    yPrime = round(yPrime, 3)
    #print("precheck ", phiPrime)
    #phiPrime = checkAngle(phiPrime)
    #print("postcheck ", phiPrime)
    phiPrime = round(phiPrime, 3)
    posUpd = np.array([xPrime, yPrime, phiPrime])  # builds array of values
    return (posUpd)


def checkAngle(theta):  #adjusts angle to keep everything within range. 
    if theta >= 0:
        while theta >= 180:
            theta = theta - 180
        return (theta)
    if theta <= 0:
        while theta <= -180:
            theta = theta + 180
        return (theta)

        ###########





def orientation():
    axes = head.getXY()  # call xy function
    axesScaled = head.scale(axes)  # perform scale function
    h = head.getHeading(axesScaled)  # compute the heading
    headingDegrees = round((h * 180 / np.pi), 2)  # rounding

    if headingDegrees <= 0:
        headingDegrees = headingDegrees + 180

    bearing = np.array([headingDegrees])
    return (bearing)

def portRun():
    while 1:
        y = 0
        x_int = 0  # initial for x
        y_int = 0  # initial for y
        theta_int = 0 # initial for ø, in degrees
        while 1:
            y = task1(x_int, y_int, theta_int)
            np.set_printoptions(suppress=True)

            print("x,y,th", y)  # prints x,y,ø

            # variables for reinsertion
            x_int = y[0]
            y_int = y[1]
            theta_int = y[2]

if __name__ == "__main__":
    portRun()
        
        
        #portRun()
    time.sleep(.1)
        #x=orientation()
        #print(x)
