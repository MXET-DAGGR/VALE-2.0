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




#Get the inital data needed

#The purpose of this function is to stop the robot from moving.
def stop():     #set 0s to both motors
    pdTargets = np.array([0, 0])
def go_front():
    #print("forward")
    sc.driveOpenLoop([7,7]) # produce duty cycles from the phi dots



#avoidance speed measures
#lefts
def sharpLeft():    #turn left on spot
    print("sharpleft")
    
    sc.driveOpenLoop([-7,7]) # produce duty cycles from the phi dots
    time.sleep(4)
    sc.driveOpenLoop([7,7]) # produce duty cycles from the phi dots
    time.sleep(5)
    duties = sc.openLoop(7, -7) # produce duty cycles from the phi dots
    sc.driveOpenLoop([7,-7]) # produce duty cycles from the phi dots
    time.sleep(4)
    
def medLeft():              #medium left response
    print("medleft")
    sc.driveOpenLoop([2,7]) # produce duty cycles from the phi dot
    time.sleep(4)
    sc.driveOpenLoop([7,7]) # produce duty cycles from the phi dots
    time.sleep(5)
    sc.driveOpenLoop([7,7]) # produce duty cycles from the phi dots
    time.sleep(4)
    return("medleft")
    
def gradLeft():     #gradual left
    print("gradleft")
    sc.driveOpenLoop([5,7]) # produce duty cycles from the phi dots
    time.sleep(5)
    sc.driveOpenLoop([7,7]) # produce duty cycles from the phi dots
    time.sleep(5)
    sc.driveOpenLoop([7,5]) # produce duty cycles from the phi dots
    time.sleep(5)
    return("gradleft")
#rights
def sharpRight():           #sharp right turn
    print("sharpRight")
    sc.driveOpenLoop([7,-7]) # produce duty cycles from the phi dots
    time.sleep(4)
    sc.driveOpenLoop([7,7]) # produce duty cycles from the phi dots
    time.sleep(5)
    sc.driveOpenLoop([-7,7]) # produce duty cycles from the phi dots
    time.sleep(4)
    
def medRight():     #medium right turn
    print("medright")
    sc.driveOpenLoop([7,2]) # produce duty cycles from the phi dots
    time.sleep(4)
    sc.driveOpenLoop([7,7]) # produce duty cycles from the phi dots
    time.sleep(4)
    sc.driveOpenLoop([2,7]) # produce duty cycles from the phi dots
    time.sleep(4)
    
    
def gradRight():            #gradual right
    print("gradright")
    sc.driveOpenLoop([7,5]) # produce duty cycles from the phi dots
    time.sleep(5)
    sc.driveOpenLoop([7,7]) # produce duty cycles from the phi dots
    time.sleep(4)
    sc.driveOpenLoop([5,7]) # produce duty cycles from the phi dots
    time.sleep(4)
    return("gradright")

    
    

def boundingCircle(why):   #bounding circle method obstacle avoidance
    
    #print("starting Obstacle Avoidance")
    for i in why:       #process through each element in the array
        n = np.array(why)
    d=n[0]          #set the distance to be equal to d
    ø=n[1]          #set theta to be equal to ø
    print(ø)
   
    if ø>-45 and ø<45:      #check for valid range by making sure numbers within 45 and -45
        print("starting Obstacle Avoidance")

        if d<2:             #checks to see if Distance is less than 2 m     know whether to react or not
            if d>1:         #checks to see if Distance is less than 1 m     #finds range
                if ø<0:     #checks to see if Theta is less than 0.         #checks for right or left
                    gradLeft()     #move the robot right gradually
                else:
                    gradRight()      #move the robot left gradually
            if d<1 and d>.5:        #checks to see if theta is within 1 and .5  Severity check
                if ø<0:             #right or left
                    medLeft()      #medium right
                else:
                    medRight()       #medium left
            if d<.5:                #checks to see within smallest bounding circle      #block motion
                if ø<0:             #checks for right and left
                    sharpLeft()    #sharp right
                else:
                    sharpRight()     #sharp left
    return
    
    print("no object within radius")        #update user on results
    #go_front()
    return

def callObstacle():                 #function to call obstacle avoidance from another program
    obs = vector.getNearest()       #pulls Lidar data to find closest vector
    boundingCircle(obs)
    return()

if __name__ == "__main__":
    while(1):
        go_front()
        #go_front()  #move forward
        callObstacle()
        time.sleep(.125)                #small time delay. 


