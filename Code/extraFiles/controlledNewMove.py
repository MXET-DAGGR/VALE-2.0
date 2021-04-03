#written by Jesse Rosart-Brodnitz

import odom as odom
import numpy as np
import time
import L2_heading as heading
import L2_kinematics as kin
import L2_speed_control as sc
import L2_inverse_kinematics as inv
import L1_gps as gps
import obstacleInfluence as oba

import math



# initialize variables for control system



t0 = 0
t1 = 1
e00 = 0
e0 = 0
e1 = 0
dt = 0
de_dt = np.zeros(2) # initialize the de_dt
count = 0

def openInverseDrive(xDot, thetaDot):   #open loop driving function
    dots=np.array([xDot, thetaDot])
    phiDots=inv.sendPdTargets(dots)
    sc.driveOpenLoop(phiDots)
    
    kin.getPdCurrent() # capture latest phi dots & update global var
    pdCurrents = kin.pdCurrents # assign the global variable value to a local var


def drive():
    
    global t0 
    global t1 
    global e00 
    global e0 
    global e1
    global dt 
    global de_dt 
    global count
    
    targetHeading=45#needs to call bearing                      
    #could insert an obstacle avoidance function call here
    #currentHeading= heading.whereismyHead()   #gets the direction the robot is facing
    #if currentHeading is None:h
    currentHeading= heading.whereismyHead()#gps.gpsHeading()
    #print('GPS: ', currentHeading)
   # currentHeading += 90
    if currentHeading < 0:
        currentHeading += 360
    currentHeading=currentHeading%360
    
    print("current: ",currentHeading)
    #print("target: ", targetHeading)
    thetaOffset=round(currentHeading-targetHeading, 0) #targetHeading-currentHeading   #calculates theta offset (the difference between the heading and the direction of intention)
    print("offset: ", thetaOffset)
    #thetaOffset=thetaOffset*np.pi/180
    
    #working function
    #if thetaOffset!=0:
        
    if abs(thetaOffset)>10:#(thetaOffset>10) or (thetaOffset<-10):
        if abs(thetaOffset)<20:
            thetaOffset=thetaOffset*np.pi/180
            openInverseDrive(0, thetaOffset/.5)
            time.sleep(.6)
        else:
            thetaOffset=thetaOffset*np.pi/180
            openInverseDrive(0, thetaOffset)
            time.sleep(1.1)
    else:
        print("now")        
    ###/////new section#////////////////////
    #thetaOff set=math.radians(thetaOffset)
    #openInverseDrive(0,thetaOffset)
    
        myThetaDot = 0 
        #print(myThetaDot)
        myXDot= .397    #travel half a meter per second in forward speed
        # BUILD SPEED TARGETS ARRAY
        A = np.array([ myXDot, myThetaDot])  #combines xdot and myThetaDot into one array to be passed into inverse kin
        pdTargets = inv.convert(A) # convert from [xd, td] to [pdl, pdr]
        #print("targets: ", pdTargets)
        kin.getPdCurrent() # capture latest phi dots & update global var
        pdCurrents = kin.pdCurrents # assign the global variable value to a local var
        #print("Pdcurrents: ", pdCurrents)
        # UPDATES VARS FOR CONTROL SYSTEM
        t0 = t1  # assign t0
        t1 = time.time() # generate current time
        dt = t1 - t0 # calculate dt
        e00 = e0 # assign previous previous error
        e0 = e1  # assign previous error
        e1 = pdCurrents - pdTargets # calculate the latest error
        de_dt = (e1 - e0) / dt # calculate derivative of error
        
        # CALLS THE CONTROL SYSTEM TO ACTION
        sc.driveClosedLoop(pdTargets, pdCurrents, de_dt)  # call the control system
        time.sleep(.1) # very small delay.
        oba.callObstacle()    #pulls in open loop obstacle avoidance code

    return()

if __name__ == "__main__":
    gps.connectGPS()

    while(1):
        drive()



        
        
        
    
        
    

