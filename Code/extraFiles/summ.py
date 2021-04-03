#import all the functions
#import L1_motors as mot
#import L2_k1nematics as kin
#import L2_log as log
import L2_speed_control as speed_con
import csv
import numpy as np
import time
#import L2_heading as head
import L1_odomEncoders as enc
import math




#the goal of this is to get the position and summarize all the informationa bout the robot
# summary matrix:
# The size of X is 1 column wide
# and 3+2*n rows high, where n 
# is the number of landmarks. 
# position of robot (x,y,ø)
# x and y of each landmark. 



#steps:
#compare to L1 file, refernce at each stp to compare. 

wait = .02

# define robot geometry
R = 0.041 # wheel radius
L = 0.201 # half of the wheelbase
N=2*np.pi##divisons per rotation
res = (359/2**14) # resolution of the encoders
roll = int(359/res) # variable for rollover logic   #16384
gap = 0.5 * roll # degress specified as limit for rollover



#things trying now:

#steps:
  #move the .0219 to after travel is declared
  #take into account rollerover to reset oda readings
  #remove the -1 being multipled onto the travL

def task1(x, y, ø):
    #ø=ø*180/np.pi   #converts to degrees

    encoders = enc.read()
    degL0 = round(encoders[0],1)
    degR0 = round(encoders[1],1)
    t1 = time.time()    # time.time() reports in seconds
                  
    time.sleep(wait)                #delay set forth in header
    
    encoders = enc.read()           # grabs the current encoder readings in degrees
    degL1 = round(encoders[0],1)    # rounded reading in degrees.
    degR1 = round(encoders[1],1)
    t2 = time.time()
    
    
    global deltaT
    deltaT = round((t2 - t1),3)

    travL=(degL1-degL0)
    if( (-travL) >= gap): # if movement is large (has rollover)
        travL = (degL1 - degL0 + roll) # forward rollover
    if( travL >= gap):
        travL = (degL1 - degL0 - roll) # reverse rollover
    
    
    
    travR=(degR1-degR0)
    if( (-travR) >= gap): # if movement is large (has rollover)
        travR = (degL1 - degL0 + roll) # forward rollover
    if( travR >= gap):
        travR = (degR1 - degR0 - roll) # reverse rollover
    travL=.0219*travL
    travR=.0219*travR 
    
    
    
    travL=(-travL)
    
    travL=travL*np.pi/180
    travR=travR*np.pi/180
 
    
    travL=np.round(travL, 3)
    travR=np.round(travR, 3)

    dL=distanceTraveled(travL, N, R)        #calls funciton to get distance moved on each wheel

    dR=distanceTraveled(travR, N, R)

    ø=ø*np.pi/180   #converts to rads

    w=positionUpdate(dL, dR, L, x, y, ø)
    
    s=summary(w)
    return(s)
    
def summary(coordinates):  #summarizes information in array
    summInfo=coordinates #np.append(coordinates, orientation())
    return(summInfo)
def distanceTraveled(traveled, divPerRot, radius):
    D=2*np.pi*radius*(traveled/divPerRot) #gets distanced travled. to be used on each travel

    #D=D*39.3701 #converts to inches for debugging. 
    return(round(D, 4))
    
def positionUpdate(dLeft, dRight, length, oldX, oldY, oldø):        #theta needs to be in rads here     #5:56 pm
    

    dCenter = (dLeft+dRight)/2
    deltø = (R*(dRight-dLeft))/(2*length)
    
    xPrime =oldX + dCenter*math.cos(oldø)
    yPrime =oldY + dCenter*math.sin(oldø)
    #phiPrime=phi+oldø
    #print(oldø)
    newTheta=oldø+deltø
    #print(newTheta)
    # print(oldø)
    # print(phiPrime)
    #phiPrime=phiPrime*180/np.pi #converts to degrees
    newTheta=round((newTheta*180/np.pi),2)
    
    xPrime =round(xPrime, 3)
    yPrime=round(yPrime, 3)
   # phiPrime=checkAngle(phiPrime)
    #phiPrime=round(phiPrime, 3)
    #posUpd = np.array([xPrime, yPrime, phiPrime])  #builds array of values
    
    
   # newTheta=checkAngle(newTheta)
    newTheta=round(newTheta, 3)
    posUpd = np.array([xPrime, yPrime, newTheta])  #builds array of values

    
    return(posUpd)
    
def checkAngle(theta):
    if theta >= 0:
        while theta>=180:
            theta=theta-180
        return(theta)
    if theta <= 0:
        while theta<=-180:
            theta=theta+180
        return(theta)    
        
    

    
  #//////////////start of unused block here\\\\\\\\\\\\\\\\\\\\\\\\#  
def posX(deltT, xtdot, x1):     #unused
    x2=(xtdot * deltT + x1)
    #print(x2)
    xpos=x1+x2
    return xpos
    

def shorty(theta1, theta2, time1, time2):    #function to get phidot
    phidot=(theta2-theta1)/(time2-time1)
    return(phidot)
    
    
    
    ###################
def never(thetaL1, thetaL2, thetaR1, thetaR2, time1, time2):      #gets Xdot
    
    phidotR=shorty(thetaR1, thetaR2, time1, time2)    #gets phiR
    phidotL=shorty(thetaL1, thetaL2, time1, time2)    #gets phiL
    xdot=(R/2)*(phidotL + phidotR)             #gets Xdot
    xdot=np.round(xdot, decimals=3)
    return xdot
    
def scar(thetaL1, thetaL2, thetaR1, thetaR2, time1, time2):                                  #gets thetadot
    phidotR=shorty(thetaR1, thetaR2, time1, time2)    #gets phiR
    phidotL=shorty(thetaL1, thetaL2, time1, time2)    #gets phiL
    thetadot=(R/(2*L))*(phidotR-phidotL)      #gets thetadot
    thetadot=np.round(thetadot, decimals=3)
    return thetadot
#//////////////end of unused block here\\\\\\\\\\\\\\\\\\\\\\\\#    
    
# def orientation():
#     axes = head.getXY() # call xy function
#     axesScaled = head.scale(axes) # perform scale function
#     h = head.getHeading(axesScaled) # compute the heading
#     headingDegrees = round((h*180/np.pi),1)   #rounding
#     bearing = np.array([headingDegrees])
#     return(bearing)
    #Tells you which way the robot is going
    # print("bearing is", bearing)
    # if -15 <= bearing <= 15:
    #     print('North')
    # elif 82 <= bearing < 98:
    #     print('East')
    # elif -98 <= bearing < -82:  #262, 278
    #     print('West')
    # elif 172 <= bearing < -172: #172, 188
    #     print('South')
    #     ####Precision increase
    # if -53 <= bearing <= -37:   #307, 323
    #     print('North West')
    # elif 37 <= bearing < 53:
    #     print('North East')
    # elif 127 <= bearing < 143:
    #     print('South East')
    # elif -143 <= bearing < -127:      #217, 233
    #     print('South West')






def portRun():
    
    y=0
    lilah = 0       #initilization for x
    padme=0         #initilization for y
    charla = 0    #initilization for ø, in degrees
    while 1:
        y=task1(padme, lilah, charla)
        np.set_printoptions(suppress=True)
        
        #print(y)    #prints x,y,ø
    
        #print(y[0])
        #variables for reinsertion
        padme=y[0]  
        lilah=y[1]
        charla=y[2]
        return(y)
            
            #log.csv_write(y)   #function to write to the csv file referenced in l2_log.py
            #heading=orientation()
            #print(heading)
            #time.sleep(0.25)
#while 1:
# x=portRun()
# print(x[0])
    
    
    # x=orientation()
    # print(x)
    
y=0
lilah = 0       #initilization for x
padme=0         #initilization for y
charla = 0     #initilization for ø, in degrees
while 1:
    y=task1(padme, lilah, charla)
    np.set_printoptions(suppress=True)
    
    padme=y[0]  
    lilah=y[1]
    charla=y[2]
    print(y)