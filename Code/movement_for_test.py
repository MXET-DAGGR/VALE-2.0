# movement.py          In Progress
#Authors: Jesse Rosart-Brodnits and Evan Maraist
#Emails: Evan Maraist: emaraist1357@gmail.com
#TEAM BAST - ESET 420 Capstone


# Code purpose: Closed loop driving based on heading deviances.
# this code reads values from the magnetomer and calls for the direction
# the robot needs to go. The difference between those two is passed in as a
# thetadot into inverse kinematics. A speed profile is built off of these. Obstacle avoidance is tied in next

# Import external libraries
import time

# Import internal programs
from Bearing import Bearing


class movement:
    #initializes movement object with 'dest' as goal
    #m2s (motor-to-speech) is queue to pass speech process information
    #s2m (speech-to-motor) is queue to receive information from speach
    def __init__(self,dest,m2m,m2s,s2m):
        self.dest = dest
        self.current = Bearing(self.dest)
        self.m2m = m2m
        self.m2s = m2s
        self.s2m = s2m

    #looks to see if the s2t has sent anything
    def checkQueue(self):
        got = None
        if self.s2m.empty() is False:
            got = self.s2m.get()
        if got == 'STOP':
            return 'STOP'
        if got == 'RESUME':
            return 'RESUME'
        if got == 'END':
            return 'END'

if __name__ == '__main__':
    while (1):
        print("This isn't meant to be run.")