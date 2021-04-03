import numpy as np
import time

# Import internal programs
import L2_heading as heading
import L2_kinematics as kin
import L2_speed_control as sc
import L2_inverse_kinematics as inv
from jelly_bearing import Bearing
import ObstacleAvoidance as oba
from multiprocessing import Process, Queue
import L1_gps as gps
import RPi.GPIO as GPIO


class movement:
    #initializes movement object with 'dest' as goal
    #m2s (motor-to-speech) is queue to pass speech process information
    #s2m (speech-to-motor) is queue to receive information from speech
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

    # stops motors
    def stop(self):
        # needs condition:
        speeds = [0, 0]
        sc.driveOpenLoop(speeds)

    #to test PWM control in a child process
    def test_move(self):
        speeds = [9.7, 9.7]
        sc.driveOpenLoop(speeds)
            

    def launch(self):  # needs to run in while loop every .005 seconds
        # could insert an obstacle avoidance function call here
        #oba.callObstacle()  # pulls in open loop obstacle avoidance code
        currentHeading = heading.whereismyHead()  # gets the direction the robot is facing
        print(currentHeading)
        thetaOffset = self.targetBearing - currentHeading  # calculates theta offset (the difference between the heading and the direction of intention)
        print('offset: ', thetaOffset)
        myThetaDot = thetaOffset * 3.14 / 180 * 2  # attempt centering in 0.5 seconds

        print(myThetaDot)
        myXDot = 0.5  # travel half a meter per second in forward speed
        # BUILD SPEED TARGETS ARRAY
        A = np.array([myXDot, myThetaDot])  # combines xdot and myThetaDot into one array to be passed into inverse kin
        pdTargets = inv.convert(A)  # convert from [xd, td] to [pdl, pdr]
        kin.getPdCurrent()  # capture latest phi dots & update global var
        pdCurrents = kin.pdCurrents  # assign the global variable value to a local var
        print(pdTargets)
        # UPDATES VARS FOR CONTROL SYSTEM
        self.t0 = self.t1  # assign t0
        self.t1 = time.time()  # generate current time
        self.dt = self.t1 - self.t0  # calculate dt
        self.e00 = self.e0  # assign previous previous error
        self.e0 = self.e1  # assign previous error
        self.e1 = pdCurrents - pdTargets  # calculate the latest error
        self.de_dt = (self.e1 - self.e0) / self.dt  # calculate derivative of error

        # CALLS THE CONTROL SYSTEM TO ACTION
        sc.driveClosedLoop(pdTargets, pdCurrents, self.de_dt)  # call the control system
        time.sleep(0.0005)  # very small delay.

    def cleanUp(self):
        self.current.cleanUp()
        #clears out queue
        while not self.s2m.empty():
            self.s2m.get()
        #deletes bearing object from memory
        del self.current

if __name__ == '__main__':
    s2m = Queue()
    m2s = Queue()
    m2m = Queue()
    #test = movement('FERM',speech_to_move,move_to_speech,move_to_main)
    gps.connectGPS()
    #while (1):
    #    test.updateGeo()
    #    test.launch()
    current = movement('TST',m2m, m2s,s2m) #initialize movement object
    Keep_Going = True
    while Keep_Going is not False: #run until Vale arrives at target or is told to stop
        # Check speech-to-motor queue, see if any orders were received
        orders = current.checkQueue()
        if orders == 'STOP':
            #Vale was told to stop. Wait until told something else.
            current.stop()
            Keep_Waiting = True
            while Keep_Waiting is True:
                got = s2m.get() #read speech-to-motor queue
                if got == 'END':
                    Keep_Waiting = False
                    orders = 'END'
                if got == 'RESUME':
                    Keep_Waiting = False
        #Vale was told to reroute or stop running
        if orders == 'END':
            Keep_Going = False
        current.updateGeo() #get current GPS location, update waypts respectively
        current.launch() #hand off to PID and obstacle avoidance code
    # if we've exited the while loop that means we're not moving anymore
    current.stop() # make sure motors have stopped
    current.cleanUp() # delete created objects, save memory
    print("Motor thread ended.")
        
