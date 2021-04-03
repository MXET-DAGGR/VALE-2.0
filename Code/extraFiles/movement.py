# movement.py          In Progress
#Authors:  Evan Maraist and Jesse Rosart-Brodnitz
#Emails: Evan Maraist: emaraist1357@gmail.com
#TEAM BAST - ESET 420 Capstone


# Code purpose: Closed loop driving based on heading deviances.
# this code reads values from the magnetomer and calls for the direction
# the robot needs to go. The difference between those two is passed in as a
# thetadot into inverse kinematics. A speed profile is built off of these. Obstacle avoidance is tied in next

# Import external libraries
import numpy as np
import time

# Import internal programs
from multiprocessing import Queue
import L2_heading as heading
import L2_kinematics as kin
import L2_speed_control as sc
import L2_inverse_kinematics as inv
from Bearing import Bearing
#import ObstacleAvoidance as oba
import obstacleInfluence as oba
import multiprocessing


class movement:
    #initializes movement object with 'dest' as goal
    #m2s (motor-to-speech) is queue to pass speech process information
    #s2m (speech-to-motor) is queue to receive information from speach
    #m2m (motor-to-main) is queue to pass information to main
    def __init__(self,dest,m2m, m2s,s2m):
        self.dest = dest
        self.current = Bearing(self.dest)
        self.m2m = m2m
        self.m2s = m2s
        self.s2m = s2m
        #initialize variables for control system
        self.t0 = 0
        self.t1 = 1
        self.e00 = 0
        self.e0 = 0
        self.e1 = 0
        self.dt = 0
        self.de_dt = np.zeros(2)  # initialize the de_dt
        self.count = 0

    #looks to see if the s2t has sent anything
    def checkQueue(self):
        got = None
        if self.s2m.empty() is False:
            got = self.s2m.get()
        if got == 'STOP':
            self.stop()
            return 'STOP'
        if got == 'RESUME':
            return 'RESUME'
        if got == 'END':
            return 'END'


    #updates current location, checks if waypt has been reached, updates target bearing
    def updateGeo(self):
        self.current.getLoc()
        self.current.checkWaypt()
        if self.current.arrived == True:
            self.stop()
            self.m2s.put('ARRIVED')
            self.m2m.put('ARRIVED')
        self.targetBearing = self.current.getBearing()
        print("Current Waypt: ",self.current.currentWaypt[1])
        print("Current Loc: ", self.current.currentLoc)

    # stops motors
    def stop(self):
        # needs condition:
        speeds = [0, 0]
        sc.driveOpenLoop(speeds)


    def launch(self):  # needs to run in while loop every .005 seconds
        #targetHeading = 130  # needs to call bearing

        # could insert an obstacle avoidance function call here
        # oba.callObstacle()    #pulls in open loop obstacle avoidance code
        currentHeading = heading.whereismyHead()  # gps.gpsHeading()
        #print('GPS: ', currentHeading)
        # currentHeading += 90
        if currentHeading < 0:
            currentHeading += 360
        print("current Heading: ", currentHeading)
        # print("target: ", targetHeading)
        # if currentHeading > 180:
        #   currentHeading = currentHeading - 180
        thetaOffset = round(currentHeading - self.targetBearing,
                            0)  # targetHeading-currentHeading   #calculates theta offset (the difference between the heading and the direction of intention)
        print("offset: ", thetaOffset)
        # thetaOffset=thetaOffset*np.pi/180

        # working function
        # if thetaOffset!=0:

        if abs(thetaOffset) > 10:  # (thetaOffset>10) or (thetaOffset<-10):
            if abs(thetaOffset) < 20:
                thetaOffset = thetaOffset * np.pi / 180
                self.openInverseDrive(0, thetaOffset / .5)
                time.sleep(.5)
            else:
                thetaOffset = thetaOffset * np.pi / 180
                self.openInverseDrive(0, thetaOffset)
                time.sleep(1)
        ###/////new section#////////////////////
        # thetaOffset=math.radians(thetaOffset)
        # openInverseDrive(0,thetaOffset)

        myThetaDot = 0
        # print(myThetaDot)
        myXDot = .397  # travel half a meter per second in forward speed
        # BUILD SPEED TARGETS ARRAY
        A = np.array([myXDot, myThetaDot])  # combines xdot and myThetaDot into one array to be passed into inverse kin
        pdTargets = inv.convert(A)  # convert from [xd, td] to [pdl, pdr]
        # print("targets: ", pdTargets)
        kin.getPdCurrent()  # capture latest phi dots & update global var
        pdCurrents = kin.pdCurrents  # assign the global variable value to a local var
        # print("Pdcurrents: ", pdCurrents)
        # UPDATES VARS FOR CONTROL SYSTEM
        self.t0 = self.t1  # assign t0
        self.t1 = time.time()  # generate current time
        self.dt = self.t1 - self.t0  # calculate dt
        self.e00 = self.e0  # assign previous previous error
        self.e0 = self.e1  # assign previous error
        self.e1 = pdCurrents - pdTargets  # calculate the latest error
        self.de_dt = (self.e1 - self.e0) / self.dt  # calculate derivative of error

        # CALLS THE CONTROL SYSTEM TO ACTION
        oba.callObstacle()    #pulls in open loop obstacle avoidance code
        sc.driveClosedLoop(pdTargets, pdCurrents, self.de_dt)  # call the control system
        time.sleep(.1)  # very small delay.

    def openInverseDrive(self, xDot, thetaDot):  # open loop driving function
        dots = np.array([xDot, thetaDot])
        phiDots = inv.sendPdTargets(dots)
        sc.driveOpenLoop(phiDots)

        kin.getPdCurrent()  # capture latest phi dots & update global var
        pdCurrents = kin.pdCurrents  # assign the global variable value to a local var

        # time.sleep(1)
        # sc.driveOpenLoop([0,0])

    def cleanUp(self):
        self.current.cleanUp()
        #clears out queue
        while not self.s2m.empty():
            self.s2m.get()
        #deletes bearing object from memory
        del self.current

if __name__ == '__main__':
    T1 = Queue()
    T2 = Queue()
    T3 = Queue()
    move_test = movement('THOM',T1,T2,T3)
    while (1):
        move_test.updateGeo()
        move_test.launch()