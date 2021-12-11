from __future__ import print_function
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import math
import argparse

# this function connects the Pi to the PX4(might not be necessary since a 
# mavlink connection is established on separate terminal)
def connect_to_rover():
    print("Hello Rover")

    connection_string = "/dev/ttyAMA0"                                      #port to connect Pi to PX4 to on UART port

    print('Connecting to vehicle on: %s ...' % connection_string)           #connecting the Pi to px

   # time.sleep(30)
    vehicle = connect(connection_string, wait_ready=True, baud= 921600)
    vehicle.wait_ready(True, raise_exception=False)
    return  vehicle  


#this function arms the vehicle after verifying that it is ready for mission
def arm_rover(vehicle):
    print("Basic pre-arm checks")                                          
    while not vehicle.is_armable:                                       #waiting for vehicle to be ready to arm
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("arming motors")
    vehicle.mode = VehicleMode("GUIDED")                                #set vehicle attribute "mode" to "Guided"
    vehicle.armed = True

    while not vehicle.armed:                                            # Confirm vehicle armed before attempting to take off
        print (" Waiting for arming...")
        time.sleep(1)

    print("Vehicle armed and ready for mission")


#go from current position to a desired location
def go_From_A_To_B(point, vehicle):
    currentLocation = vehicle.location.global_relative_frame
    print("CurrentLocation = %s " % currentLocation)
    nextLocation = LocationGlobalRelative(point[0], point[1],0)        #location in (lat, long, altitude)

    vehicle.simple_goto(nextLocation, 0, 0.5)                           #Go to nextLocation based on the current position 
    while vehicle.mode.name=="GUIDED":                                  #Stop action if we are no longer in guided mode.            
        remainingDistance=get_distance_metres(vehicle.location.global_frame, nextLocation)
        print("Distance to target: ", remainingDistance)
        if remainingDistance<= 0.5:                        #Just below target, in case of undershoot.
            print("Reached target")
            break
        time.sleep(1)


# pass in a route(list of points) for the rover to drive to
def travel_route(route):
    for nextPoint in route:                                             #iterate through waypoints in "route"
        go_From_A_To_B(nextPoint)
    print("reached final destination")


def disarm(vehicle):
    currentLocation = vehicle.location.global_relative_frame
    nextLocation = LocationGlobalRelative(currentLocation[0], currentLocation[1], 0)
    vehicle.simple_goto(nextLocation)
    vehicle.armed = False
    print("Vechicle disarmed")


def cleanUp(vehicle):
    vehicle.clear()
    vehicle.close()

#This function returns the distance in meters from current location to the next location
#coordinate system is based off of WGS84
def get_distance_metres(aLocation1, aLocation2):
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5
