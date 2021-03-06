
# This example sends commands to two motors on the appropriate pins for H-bridge
# Designed for Pi hardware.

import gpiozero #gpiozero is the chosen library for PWM functionality
from gpiozero import PWMOutputDevice
import time
import RPi.GPIO as GPIO

#info on pins:
#data flow: PWM on secondary
#left in1=5, GPIO 5
#left in2=12, GPIO 12, PWM

#Right in1=6, GPIO 6
#Right in2=13, GPIO 13, PWM

#use this if high/low pins reverse
# leftOutA = PWMOutputDevice(5, active_high=False, frequency=1000,initial_value=0) #green
# leftOutB = PWMOutputDevice(12, active_high=False,frequency=1000,initial_value=0)  #blue
# 
# RightOutA = PWMOutputDevice(6, active_high=False, frequency=1000,initial_value=0)  #grey
# RightOutB = PWMOutputDevice(13, active_high=False, frequency=1000,initial_value=0) #purple

leftOutA = PWMOutputDevice(17, active_high=False, frequency=1000,initial_value=0) 
leftOutB = PWMOutputDevice(18, active_high=False,frequency=1000,initial_value=0)

RightOutA = PWMOutputDevice(22, active_high=False, frequency=1000,initial_value=0)
RightOutB = PWMOutputDevice(23, active_high=False, frequency=1000,initial_value=0)



#channel refers to left(0) or right(1)
def MotorL(speed):
    if speed>0:
        leftOutB.value = speed
        leftOutA.value = 0
    elif speed<0:
        leftOutB.value = 0
        leftOutA.value = (-1*speed) #drive opposite polarity with positive duty cycle
    elif speed==0:
        leftOutB.value = 0
        leftOutA.value = 0

def MotorR(speed):
    if speed>0:
        RightOutB.value = speed
        RightOutA.value = 0
    elif speed<0:
        RightOutB.value = 0
        RightOutA.value = (-1*speed) #drive opposite polarity with positive duty cycle
    elif speed==0:
        RightOutB.value = 0
        RightOutA.value = 0

#Uncomment the section below to run this code by itself!
if __name__ == "__main__":

    while True:  # This loop will drive both motors forwards and backwards, repeatedly
        try:
            print("running")
            MotorL(.6)
            MotorR(.6)
            time.sleep(2)
            MotorR(-.6) 
            MotorL(-.6)
            time.sleep(2)
        except KeyboardInterrupt:
            GPIO.cleanup()
            pass







