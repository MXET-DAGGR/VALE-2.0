#primary obstacle avoidance for VALE
#utilizes open loop drive and bounding circles
#Author: Jesse Rosart-Brodnitz
#Contact: jorbaustin@gmail.com


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
    m.MotorL(1)
    m.MotorR(1)


#avoidance speed measures
#lefts
def sharpLeft():    #turn left on spot
    print("sharpleft")
    duties = sc.openLoop(-7, 7) # produce duty cycles from the phi dots
    m.MotorL(duties[0]) # send command to motors
    m.MotorR(duties[1]) # send command to motors
    time.sleep(2)
    duties = sc.openLoop(7, 7) # produce duty cycles from the phi dots
    m.MotorL(duties[0]) # send command to motors
    m.MotorR(duties[1]) # send command to motors
    time.sleep(3)
    duties = sc.openLoop(7, -7) # produce duty cycles from the phi dots
    m.MotorL(duties[0]) # send command to motors
    m.MotorR(duties[1]) # send command to motors
    time.sleep(2)
    
def medLeft():              #medium left response
    print("medleft")
    duties = sc.openLoop(2, 7) # produce duty cycles from the phi dots
    m.MotorL(duties[0]) # send command to motors
    m.MotorR(duties[1]) # send command to motors
    time.sleep(2)
    duties = sc.openLoop(7, 7) # produce duty cycles from the phi dots
    m.MotorL(duties[0]) # send command to motors
    m.MotorR(duties[1]) # send command to motors
    time.sleep(2)
    duties = sc.openLoop(7, 2) # produce duty cycles from the phi dots
    m.MotorL(duties[0]) # send command to motors
    m.MotorR(duties[1]) # send command to motors
    time.sleep(2)
    return("medleft")
    
def gradLeft():     #gradual left
    print("gradleft")
    duties = sc.openLoop(5, 7) # produce duty cycles from the phi dots
    m.MotorL(duties[0]) # send command to motors
    m.MotorR(duties[1]) # send command to motors
    time.sleep(3)
    duties = sc.openLoop(7, 7) # produce duty cycles from the phi dots
    m.MotorL(duties[0]) # send command to motors
    m.MotorR(duties[1]) # send command to motors
    time.sleep(3)
    duties = sc.openLoop(7, 5) # produce duty cycles from the phi dots
    m.MotorL(duties[0]) # send command to motors
    m.MotorR(duties[1]) # send command to motors
    time.sleep(3)
    return("gradleft")
#rights
def sharpRight():           #sharp right turn
    print("sharpRight")
    duties = sc.openLoop(7, -7) # produce duty cycles from the phi dots
    m.MotorL(duties[0]) # send command to motors
    m.MotorR(duties[1]) # send command to motors
    time.sleep(2)
    duties = sc.openLoop(7, 7) # produce duty cycles from the phi dots
    m.MotorL(duties[0]) # send command to motors
    m.MotorR(duties[1]) # send command to motors
    time.sleep(3)
    duties = sc.openLoop(-7, 7) # produce duty cycles from the phi dots
    m.MotorL(duties[0]) # send command to motors
    m.MotorR(duties[1]) # send command to motors
    time.sleep(2)
    
def medRight():     #medium right turn
    print("medright")
    duties = sc.openLoop(7, 2) # produce duty cycles from the phi dots
    m.MotorL(duties[0]) # send command to motors
    m.MotorR(duties[1]) # send command to motors
    time.sleep(2)
    duties = sc.openLoop(7, 7) # produce duty cycles from the phi dots
    m.MotorL(duties[0]) # send command to motors
    m.MotorR(duties[1]) # send command to motors
    time.sleep(2)
    duties = sc.openLoop(2, 7) # produce duty cycles from the phi dots
    m.MotorL(duties[0]) # send command to motors
    m.MotorR(duties[1]) # send command to motors
    time.sleep(2)
    return("medright")
    
def gradRight():            #gradual right
    print("gradright")
    duties = sc.openLoop(7, 5) # produce duty cycles from the phi dots
    m.MotorL(duties[0]) # send command to motors
    m.MotorR(duties[1]) # send command to motors
    time.sleep(3)
    duties = sc.openLoop(7, 7) # produce duty cycles from the phi dots
    m.MotorL(duties[0]) # send command to motors
    m.MotorR(duties[1]) # send command to motors
    time.sleep(2)
    duties = sc.openLoop(5, 7) # produce duty cycles from the phi dots
    m.MotorL(duties[0]) # send command to motors
    m.MotorR(duties[1]) # send command to motors
    time.sleep(3)
    return("gradright")

    
    

def boundingCircle(why):   #bounding circle method obstacle avoidance
    
    
    for i in why:       #process through each element in the array
        n = np.array(why)
    d=n[0]          #set the distance to be equal to d
    ø=n[1]          #set theta to be equal to ø
   
    if ø>-45 and ø<45:      #check for valid range by making sure numbers within 45 and -45
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
        go_front()  #move forward
        callObstacle()
        time.sleep(.125)                #small time delay. 

