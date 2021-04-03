# movement.py          In Progress
#1234
# Code purpose: Closed loop driving based on heading deviances.
#this code reads values from the magnetomer and calls for the direction
#the robot needs to go. The difference between those two is passed in as a
#thetadot into inverse kinematics. A speed profile is built off of these. Obstacle avoidance is tied in next

# Import external libraries
import numpy as np
import time

# Import internal programs
import L2_heading as heading
import L2_kinematics as kin
import L2_speed_control as sc
import L2_inverse_kinematics as inv
# import bearing as bearing   @Evan
#import ObstacleAvoidance as oba
import L1_gps as gps

# initialize variables for control system

lastPosition=0
lastHeading=0
t0 = 0
t1 = 1
e00 = 0
e0 = 0
e1 = 0
dt = 0
de_dt = np.zeros(2) # initialize the de_dt
count = 0



def initRun():
    time.sleep(8)
    for x in range (0,50):
        currentHeading=gps.gpsHeading()
        speeds=[14,14]
        sc.driveOpenLoop(speeds)
        print("iteration: ",x)
        time.sleep(.06)
    print("did you fail?")
    currentHeading=gps.gpsHeading()

def stop():   #stops motors
    #needs condition:
    speeds=[0,0]
    sc.driveOpenLoop(speeds)
    
def launch():   #needs to run in while loop every .005 seconds
    global t0 
    global t1 
    global e00 
    global e0 
    global e1
    global dt 
    global de_dt 
    global count
    global lastHeading
    global lastPosition
    
#     if lastHeading== None:
#         lastHeading=0
    
#     currentPosition = gps.readPosition() 
#     if currentPosition != lastPosition:
#         currentHeading=gps.gpsHeading()
#         if currentHeading>0:
#             lastHeading=currentHeading
#             print("Heading: ", currentHeading)
#         else:
#             currentHeading=lastHeading
#             print("Heading: ", currentHeading)
        
    currentHeading=heading.whereismyHead()#gps.gpsHeading()
    
    targetHeading=90 #needs to call bearing                      
    #could insert an obstacle avoidance function call here
    #oba.callObstacle()    #pulls in open loop obstacle avoidance code
    #currentHeading= heading.whereismyHead()   #gets the direction the robot is facing
    #if currentHeading is None:

    thetaOffset=targetHeading - currentHeading#targetHeading-currentHeading   #calculates theta offset (the difference between the heading and the direction of intention)
    #thetaOffset = currentHeading - targetHeading
# if thetaOffset < -180:
#     thetaOffset=thetaOffset+360
    
    print("offset: ", thetaOffset)
    myThetaDot = thetaOffset * (np.pi/180)*2 # attempt centering in 0.5 seconds
    
    #print(myThetaDot)
    myXDot= .5    #travel half a meter per second in forward speed
    # BUILD SPEED TARGETS ARRAY
    A = np.array([ myXDot, myThetaDot])  #combines xdot and myThetaDot into one array to be passed into inverse kin
    pdTargets = inv.sendPdTargets(A) # convert from [xd, td] to [pdl, pdr]

    #pdTargets[0]=pdTargets[0]/9.75
    #pdTargets[1]=pdTargets[1]/9.75
    kin.getPdCurrent() # capture latest phi dots & update global var
    pdCurrents = kin.pdCurrents # assign the global variable value to a local var
    print("currents: ",pdCurrents)
    print("targets: ",pdTargets)
    #pdTargets=[.1,-1]
#     if (pdTargets[0] < pdTargets[1]):
#         print("adjusting left")
#     if (pdTargets[0] > pdTargets[1]):
#         print("adjusting right")
    
    # UPDATES VARS FOR CONTROL SYSTEM
    t0 = t1  # assign t0
    t1 = time.time() # generate current time
    dt = t1 - t0 # calculate dt
    e00 = e0 # assign previous previous error
    e0 = e1  # assign previous error
    e1 = pdCurrents - pdTargets# calculate the latest error
    de_dt = (e1 - e0) / dt # calculate derivative of error
    
    # CALLS THE CONTROL SYSTEM TO ACTION
    sc.driveClosedLoop(pdTargets, pdCurrents, de_dt)  # call the control system
    time.sleep(.05) # very small delay. (was .0005)
    return()

if __name__ == "__main__":

    gps.connectGPS()
    print('connected')
    #lastHeading=0
    #initRun()
    while(1):
        launch()

