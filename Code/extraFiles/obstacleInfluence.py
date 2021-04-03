 #primary obstacle avoidance for VALE
#utilizes open loop drive and bounding circles

import L2_vector as vector
import numpy as np
from math import *
import time
import L2_speed_control as sc
import L1_motors as m
import csv
import L2_kinematics as kin
import L2_inverse_kinematics as inv
import math


def drive(xDot, thetaDot):   #open loop driving function
    thetaDot=math.radians(thetaDot)
    dots=np.array([xDot, thetaDot])
    phiDots=inv.sendPdTargets(dots)
    sc.driveOpenLoop(phiDots)
    
def stop():
    drive(0,0)
    return()

def go_front():
    drive(.397, 0)
    return()
def go_left():
    
    drive(0, -90)
    time.sleep(1)
    go_front()
    time.sleep(1)
    drive(0, 90)
    time.sleep(1)
    return()
    
def go_right():
    drive(0, 90)
    time.sleep(1)
    go_front()
    time.sleep(1)
    drive(0, -90)
    time.sleep(1)
    return()

#avoidance speed measures
#lefts

    

def avoid(why):   #bounding circle method obstacle avoidance
    
    #print("starting Obstacle Avoidance")
    for i in why:       #process through each element in the array
        n = np.array(why)
    d=n[0]          #set the distance to be equal to d
    theta=n[1]          #set theta to be equal to ø
    print(theta)
   
    if theta>-45 and theta<45:      #check for valid range by making sure numbers within 45 and -45
        if d<2:             #checks to see if Distance is less than 2 m     know whether to react or not
            print("starting Obstacle Avoidance")
            if theta >0:
                go_left()
            else:
                go_right()
                
    return

def callObstacle():                 #function to call obstacle avoidance from another program
    obs = vector.getNearest()       #pulls Lidar data to find closest vector
    avoid(obs)
    return()

if __name__ == "__main__":
    
    
    while(1):
        #go_front()
        #go_front()  #move forward
        #go_left()
        callObstacle()
        stop()
        time.sleep(.125)                #small time delay. 



