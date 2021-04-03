# to run this code you will need internet connection
# if running for the first time pip install SpeechRecognition
# if running for the first time pip install pyaudio
# make sure the correct microphone is selected run sudo raspi-config, then select advanced, then mic
# the purpose of this code is to go through the valid user inputs for building input
import os
import speech_recognition as sr

# these are needed for speech recognition and microphone input
global r
global talk
r = sr.Recognizer()
talk = sr.Microphone(device_index=None)

# these lists hold valid building destinations for VALE

AC = ['academic building', 'the academic building']

FER = ['fermier', 'premier', 'premiere', 'Vermeer']

TH = ['Thompson', 'Thomson']

ZE = ['Zachary engineering education complex', 'Zachary',
      'Zach', 'Zachary engineering complex']

AD = ['administrative building']

HM=['home', 'Home']

# this is the function that gets speech input
def speech2text(r, talk):
    with talk as source:
        print('say something!…')
        audio = r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        recog = r.recognize_google(audio, language='en-US')
        print(recog)
        return recog
    except sr.UnknownValueError:
        print('Google Speech Recognition could not understand audio')
    except sr.RequestError as e:
        print('Could not request results from Google Speech Recognition service; {0}'.format(e))


# this is where the first input it asked
def begin():
    speech = str(
        'Welcome to VALE the autonomous guidebot of the future!')
    os.system('echo \'' + speech + '\' | festival --tts')

#method to make Vale say something
def say(speech):
    os.system('echo \'' + speech + '\' | festival --tts')

# return building code for the API search
def check_bldg(speech,target_Bldg,have_job):
    if any(sub in speech for sub in AC):
        print('ACAD')
        say('Did you want to go to ' + AC[0])
        check = yes_no()
        if check == True:
            say('Proceeding to ' + AC[0] + ' please follow me.')
            return 'ACAD', True
        else:
            return None, False
    elif any(sub in speech for sub in FER):
        print('FERM')
        say('Did you want to go to ' + FER[0])
        check = yes_no()
        if check == True:
            say('Proceeding to ' + FER[0] + ' please follow me.')
            return 'FERM', True
        else:
            return None, False
    elif any(sub in speech for sub in TH):
        print('THOM')
        say('Did you want to go to ' + TH[0])
        check = yes_no()
        if check == True:
            say('Proceeding to ' + TH[0] + ' please follow me.')
            return 'THOM', True
        else:
            return None, False
    elif any(sub in speech for sub in ZE):
        print('ZEEC')
        say('Did you want to go to ' + ZE[0])
        check = yes_no()
        if check == True:
            say('Proceeding to ' + ZE[0] + ' please follow me.')
            return 'ZEEC', True
        else:
            return None, False
    elif any(sub in speech for sub in AD):
        print('ADMM')
        say('Did you want to go to ' + AD[0])
        check = yes_no()
        if check == True:
            say('Proceeding to ' + AD[0] + ' please follow me.')
            return 'ADMM', True
        else:
            return None, False
    elif any(sub in speech for sub in HM):
        print('HOME')
        say('Did you want to go to ' + HM[0])
        check = yes_no()
        if check == True:
            say('Proceeding to ' + HM[0] + ' please follow me.')
            return 'HME', True
        else:
            return None, False 
    else:
        print('Input not valid.')
        return None, False

# checks if a user has said 'Hey vale'
def hey_Vale(speech):
    hey_checker = ['hey', 'hay', 'hey vale', 'hey veil', 'hey bale', 'hey bail', 'hey Vail', 'hay vale',
                   'hay Vail', 'hay bail', 'hay bale', 'hay Veil', 'haybale']
    print("this is the test: ", speech)
    #Vale_checker = ['veil', 'vale','Vail', 'bail', 'bale']
    if speech in hey_checker: # and any(j in speech for j in Vale_checker):
        say('Hey User')
        return True
    else:
        return False

# checks to make sure the user input is valid
def user_input(speech):
    building_check = {'the academic building', 'academic building', 'Zachary', 'premiere', 'fermier',
             'Fermier', 'Zachary engineering building', 'Thompson', 'Zachary engineering complex', 'Zach', 'Vermeer', 'Home', 'home','mirror'
             }

#checks if the user has inputted a command to Vale
def command_check(speech):
    commands_check = {'stop', 'go', 'resume', 'change', 'reroute','off','deactivate'}
    if speech in commands_check:
        say('Command received.')
        if speech in 'stop':
            # stop motor
            say('Stoppping.')
            return 'stop'

        if speech in 'go' or speech in 'resume':
            # resume travel
            say('Resuming travel.')
            return 'resume'

        if speech in 'change' or speech in 'reroute':
            # change destination
            say('One moment. Cleaning out old navigation data.')
            return 'reroute'

        if speech in 'end' or speech in 'done':
            # user is done with travel
            say('Vale was happy to guide you. Have a pleasant day.')
            return 'end'

        if speech in 'off' or speech in 'deactivate':
            # cancel movement and turn off Vale
            say('Deactivating. Thank you for using Vale!')
            return 'deactivate'

    else:
        say('Invalid input.')

# this is the function for yes or no input
def yes_no():
    yesses = ['yes', 'yeah', 'affirmative', 'correct']
    nos = ['no', 'wrong']
    val = speech2text(r, talk)
    if any(i in val for i in yesses):
        print("User said yes.")
        return True
    elif any(i in val for i in nos):
        print("User said no.")
        return False
    else:
        print("Invalid input.")
        return False

def reroute():  # reroutes gps
    s = str('Rerouting, please wait')
    os.system('echo \'' + s + '\' | festival --tts')

if __name__ == '__main__':
    begin()
    speech = speech2text(r, talk)
    user_input(speech)
    
