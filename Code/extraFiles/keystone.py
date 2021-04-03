# Author: Evan Maraist
# Email: emaraist1357@gmail.com
# TEAM BAST - ESET 420 Capstone
from Hologram.HologramCloud import HologramCloud
from multiprocessing import Process, Queue
from vale_com import *
import signal
from contextlib import contextmanager
from movement import movement as move_class
import os
import speech_recognition as sr
import L1_gps as gps
import RPi.GPIO as GPIO
import L2_speed_control as sc

global Keep_Going
global Continue_speech

# hologram = HologramCloud(dict(), network='cellular')
# Connect to internet via Nova hologram
def connect():
    gps.connectGPS()
    # commented out if not using Nova
    # result = False
    # while(result == False):
    #   result = hologram.network.connect()


# this process will be responsible for moving Vale to its destination
# def movement(dest, m2m, m2s, s2m):
#    current = move_class(dest,m2m, m2s,s2m) #initialize movement object
#    Keep_Going = True
#    while Keep_Going is not False: #run until Vale arrives at target or is told to stop
#        # Check speech-to-motor queue, see if any orders were received
#        orders = current.checkQueue()
#        if orders == 'STOP':
#            #Vale was told to stop. Wait until told something else.
#            print('Motor received stop.')
#            current.stop()
#            Keep_Waiting = True
#            while Keep_Waiting is True:
#                got = s2m.get() #read speech-to-motor queue
#                if got == 'END':
#                    Keep_Waiting = False
#                    orders = 'END'
#                if got == 'RESUME':
#                   Keep_Waiting = False
#        #Vale was told to reroute or stop running
#        if orders == 'END':
#            Keep_Going = False
#        current.updateGeo() #get current GPS location, update waypts respectively
#        #current.launch() #hand off to PID and obstacle avoidance code
#        current.test_move() #testing multiprocessing PWM control
#    # if we've exited the while loop that means we're not moving anymore
#    current.stop() # make sure motors have stopped
#    current.cleanUp() # delete created objects, save memory
#    print("Motor thread ended.")

# this process will be responsible for listening to a user's input
def user_interface(s2main, s2move, m2s):  # listen for user input and react
    say('The speech thread is running.')

    Continue_speech = True
    while Continue_speech == True:
        print("Speech loop in progress.")
        if m2s.empty() is False:
            status = m2s.get()
            if status == 'ARRIVED':  # Vale has arrived at destination
                say('We have arrived. Thank you for using Vale.')
                break
        print("Checked queue")
        say('Vale is listening for speech input.')
        # listen for 'Hey Vale'
        speech = speech2text(r, talk)
        if hey_Vale(speech) is True:  # User wants to issue input
            say('Hey User')
            s2move.put('STOP')
            listening = True
            while listening is True:  # listen for orders
                speech = speech2text(r, talk)
                orders = command_check(speech)
                if orders == 'stop':  # user said stop, wait for user to say resume
                    listening = False
                if orders == 'resume':  # user wants to resume along path
                    s2move.put('RESUME')
                    listening = False
                if orders == 'reroute' or orders == 'end':  # user wants to input a new destination or is done
                    s2move.put('END')
                    s2main.put('REROUTE')
                    listening = False
                    Continue_speech = False
                if orders == 'deactivate':  # User told Vale to turn off
                    s2move.put('END')
                    s2main.put('DEACTIVATE')
                    listening = False
                    Continue_speech = False
    print("UI thread ended.")


# main code
if __name__ == '__main__':
    # connect to internet via Nova and initialize GPS
    connect()
    # create data queues for communicating between processes and main
    # this many queues is probably unecessary, but I wanted to be safe *shrug*
    speech_to_move = Queue()
    speech_to_main = Queue()
    move_to_speech = Queue()
    move_to_main = Queue()

    GPIO.setwarnings(False)

    # initial greeting
    begin()

    # Run until told to deactivate
    run = True
    while run == True:

        # request instructions
        say('The Vale autonomous guide is ready to begin guidance.')

        # Receive instructions
        have_job = False
        target_Bldg = None
        while have_job == False: #loop until user has input instructions
            speech = speech2text(r, talk)
            if hey_Vale(speech) == True: #if user says 'Hey vale'
                while target_Bldg == None: #until user inputs correct building name
                    say('Say a building.')
                    speech = speech2text(r, talk)
                    target_Bldg, have_job= check_bldg(speech,have_job,target_Bldg)  #from start line ( have_job)
        print('This is target ', target_Bldg)
        print('This is have job', have_job)
        # Instructions received, create and initialize threads
        ui = Process(target=user_interface, args=(speech_to_main, speech_to_move, move_to_speech))
        # move = Process(target = movement, args= (target_Bldg, move_to_main, move_to_speech, speech_to_move))

        # start threads
        ui.start()

        current = move_class(target_Bldg, move_to_main, move_to_speech, speech_to_move) #initialize movement object
        El_dorado = True  # On the trail we blaze
        while El_dorado == True:
            #Check speech-to-motor queue, see if any orders were received
            orders = current.checkQueue()
            if orders == 'STOP':
                #Vale was told to stop. Wait until told something else.
                print('Motor received stop.')
                current.stop()
                Keep_Waiting = True
                while Keep_Waiting is True:
                    if speech_to_move.empty() is False:  # read from speech queue
                        got = speech_to_move.get() #read speech-to-motor queue
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
            # wait for responses from threads
            got = None
            if speech_to_main.empty() is False:  # read from speech queue
                got = speech_to_main.get()
                if got == 'DEACTIVATE':
                    El_dorado = False
                    run = False
                if got == 'REROUTE':  # user requested to change directions
                    EL_dorado = False
            if move_to_main.empty is False:  # read from move queue
                got = speech_to_main.get()
                if got == 'ARRIVED':
                    # clean up old objects reset while loop and wait for new instructions
                    El_dorado = False
            # if we've exited the while loop that means we're not moving anymore
        current.stop()  # make sure motors have stopped
        current.cleanUp()  # delete created objects, save memory
        print("Motor thread ended.")

        # Gives processes five seconds to close before terminating
        ui.join(5)
        # os.system("sudo hologram network disconnect")