#Author: Evan Maraist
#Email: emaraist1357@gmail.com
#TEAM BAST - ESET 420 Capstone

#The purpose of this code is to test some of Keystones features on my own device without
#needing speech to text and etc.

#Changelog for main:
#changed if yes_no(): to use a check statement
#fixed if statements in check_bldg
#changed all say() to print()
#Changed all listens to
#fixed movement thread recursion
#added return statements to check_bldg

#from Hologram.HologramCloud import Hologram
from multiprocessing import Process, Queue
#from VALE_communication import *
import signal
from contextlib import contextmanager
from movement_for_test import movement as test_move

#Connect to internet via Nova hologram
def connect():
    result = False
    while(result == False):
        result = hologram.network.connect()

def check_bldg(speech, goal, mission):
    print(mission)
    AC = ['academic building', 'the academic building']

    FER = ['fermier', 'premier', 'premiere', 'Vermeer']

    TH = ['Thompson']

    ZE = ['Zachary engineering education complex', 'Zachary',
          'Zach', 'Zachary engineering complex']

    AD = ['administrative building']

    if any(sub in speech for sub in AC):
        print('ACAD')
        print('Did you want to go to ' + AC[0])
        check = yes_no()
        if check == True:
            print('Proceeding to ' + AC[0] + ' please follow me.')
            return 'ACAD', True
        else:
            return None, False
    elif any(sub in speech for sub in FER):
        print('FERM')
        print('Did you want to go to ' + FER[0])
        check = yes_no()
        if check == True:
            print('Proceeding to ' + FER[0] + ' please follow me.')
            return 'FERM', True
        else:
            return None, False
    elif any(sub in speech for sub in TH):
        print('THOM')
        print('Did you want to go to ' + TH[0])
        check = yes_no()
        if check == True:
            print('Proceeding to ' + TH[0] + ' please follow me.')
            return 'THOM', True
        else:
            return None, False
    elif any(sub in speech for sub in ZE):
        print('ZEEC')
        print('Did you want to go to ' + ZE[0])
        check = yes_no()
        print(check)
        if check == True:
            print('Proceeding to ' + ZE[0] + ' please follow me.')
            return 'ZEEC', True
        else:
            return None, False
    elif any(sub in speech for sub in AD):
        print('ADMM')
        print('Did you want to go to ' + AD[0])
        check = yes_no()
        if check == True:
            print('Proceeding to ' + AD[0] + ' please follow me.')
            return 'ADMM', True
        else:
            return None, False
    else:
        print('not valid')
        return False, False

def yes_no():
    val = input("Yes or No?")
    if val == 'Yes' or val == "yes":
        print("User said yes.")
        return True
    elif val == 'No' or val == 'no':
        print("User said no")
        return False
    else:
        print("Invalid input.")
        return False

#this process will be responsible for moving Vale to its destination
def movement(dest, m2m, m2s, s2m, main2s):
    print("Movement is running.")
    current = test_move(dest,m2m, m2s,s2m) #initialize movement object
    Keep_Going = True
    while Keep_Going is not False: #run until Vale arrives at target or is told to stop
        # Check speech-to-motor queue, see if any orders were received
        orders = current.checkQueue()
        print("Motors got: ", orders)
        if orders == 'STOP':
            #Vale was told to stop. Wait until told something else.
            print("Motors stopped.")
            Keep_Waiting = True
            while Keep_Waiting is True:
                got = s2m.get() #read speech-to-motor queue
                print("Movement got: ", got)
                if got == 'END':
                    Keep_Waiting = False
                    orders = 'END'
                if got == 'RESUME':
                    print("Movement is resuming.")
                    Keep_Waiting = False
        #Vale was told to reroute or stop running
        if orders == 'END':
            Keep_Going = False
            print("Motor is ending navigation.")
        #print("Update GEO.")
        #print("PID control and movement.")
    # if we've exited the while loop that means we're not moving anymore
    print("Movement looped exited.")
    print("Motors stopped.")
    print("Movement cleanup.")

#this process will be responsible for listening to a user's input
def user_interface(s2main,s2move,move2s,main2s ): # listen for user input and react
    print("UI is running.")
    Keep_Going = True
    while Keep_Going == True:
        status = None
        if move2s.empty() is False:
            status = move2s.get()
        print("UI Received: ", status)
        if status == 'ARRIVED': #Vale has arrived at destination
            print('We have arrived. Thank you for using Vale.')
            break
        #listen for 'Hey Vale'
        print("Would you like to input a command?")
        s2main.put('CHECK')
        #wait for return
        received = False
        while received == False:
            if main2s.empty() is False:
                check = main2s.get()
                received = True
        if check is True: #user wants to input an order
            print('Hey User')
            s2move.put('STOP')
            listening = True
            while listening is True: # listen for orders
                #receive orders from user
                s2main.put('ORDERS')
                received2 = False
                while received2 == False:
                    if main2s.empty() is False:
                        orders = main2s.get()
                        received2 = True
                if orders == 'stop': # user said stop, wait for user to print resume
                    listening = False
                if orders == 'resume': # user wants to resume along path
                    s2move.put('RESUME')
                    print("UI Put: RESUME")
                    listening = False
                if orders == 'reroute' or orders == 'end': # user wants to input a new destination or is done
                    s2move.put('REROUTE')
                    s2main.put('REROUTE')
                    print("UI Put: REROUTE")
                    listening = False
                    Keep_Going = False
                if orders == 'deactivate': #User told Vale to turn off
                    s2move.put('END')
                    s2main.put('DEACTIVATE')
                    print("UI Put: END and DEACTIVATE")
                    listening = False
                    Keep_Going = False



#main code
if __name__ == '__main__':
    #connect to internet via Nova
    print("Connect to internet.")

    #create data queues for communicating between processes and main
    #this many queues is probably unecessary, but I wanted to be safe *shrug*
    speech_to_move = Queue()
    speech_to_main = Queue()
    move_to_speech = Queue()
    move_to_main = Queue()
    main_to_speech = Queue()


    #initial greeting
    print("Commencing trial.")

    #Run until told to deactivate
    run = True
    while run == True:

        #request instructions
        print('The Vale autonomous guide is ready to begin guidance.')

        #Receive instructions
        have_job = False
        target_Bldg = 0
        while have_job == False: #loop until user has input instructions
            orders = input("Which building would you like to navigate to?")
            temp = []
            target_Bldg,have_job = check_bldg(orders,target_Bldg,have_job)

            print(target_Bldg)
            print(have_job)

        #Instructions received, create and initialize threads
        ui = Process(target= user_interface, args=(speech_to_main, speech_to_move, move_to_speech, main_to_speech))
        move = Process(target = movement, args= (target_Bldg, move_to_main, move_to_speech, speech_to_move))
        print("Threads initialized.")

        #start threads
        ui.start()
        move.start()
        print("Threads started.")

        El_dorado = True #On the trail we blaze
        while El_dorado == True:
            # wait for responses from threads
            got = None
            if speech_to_main.empty() is False: #read from speech queue
                got = speech_to_main.get()
                print("Main got: ", got)
                if got == 'DEACTIVATE':
                    El_dorado = False
                    run = False
                if got == 'REROUTE': # user requested to change directions
                    EL_dorado = False
                if got == 'CHECK':
                    check = yes_no()
                    main_to_speech.put(check)
                if got == 'ORDERS':
                    val = input("Do you wish to stop, resume, reroute, or deactivate?")
                    main_to_speech.put(val)
            if move_to_main.empty is False: # read from move queue
                got = speech_to_main.get()
                if got == 'ARRIVED':
                    # clean up old objects reset while loop and wait for new instructions
                    El_dorado = False
        print("El_dorado exited.")
        #Gives processes five seconds to close before terminating
        ui.join(5)
        move.join(5)
        print("Threads closed.")