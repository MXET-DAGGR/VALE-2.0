import os
import speech_recognition as sr

# these are needed for speech recognition and microphone input
global r
global talk
r = sr.Recognizer()
talk = sr.Microphone(device_index=None)

# these dictonaries hold valid building destinations for VALE

AC = {'academic building', 'the academic building'}

FER = {'fermier', 'premier', 'premiere', 'Vermeer'}

TH = {'Thompson'}

ZE = {'Zachary engineering education complex', 'Zachary',
      'Zach', 'Zachary engineering complex'}

AD = {'administrative building'}

TS = {'test', 'link', 'cat', 'igloo'}

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
def check_bldg(speech,target_Bldg,have_job): #removed goal and mission for testing
    if speech in AC:
        ACAD = str('ACAD')
        say('Did you want to go to the acadmeic building')
        if yes_no():
            say('Proceeding to the academic building please follow me.')
            goal = 'ACAD'
            mission = True
            return goal, mission
    if speech in TS:
        TST = str('TST')
        say('Did you want to go to the test spot')
        if yes_no():
            say('Proceeding to the test spot please follow me.')
            goal = 'ACAD'
            mission = True
            return goal, mission
    if speech in FER:
        FERM = str('FERM')
        say('Did you want to go to fermier')
        if yes_no():
            say('Proceeding to fermier please follow me.')
            goal = 'FERM'
            mission = True
            return goal, mission
    if speech in TH:
        THOM = str('THOM')
        say('Did you want to go to Thompson')
        if yes_no():
            say('Proceeding to Thompson please follow me.')
            goal = 'THOM'
            mission = True
            return goal, mission
    if speech in ZE:
        ZEEC = str('ZEEC')
        say('Did you want to go to Zachary')
        if yes_no():
            say('Proceeding to Zachary please follow me.')
            goal = 'ZEEC'
            mission = True
            return goal, mission
    if speech in AD:
        ADMM = str('ADMM')
        say('Did you want to go to administrative building')
        if yes_no():
            say('Proceeding to administrative building please follow me.')
            goal = 'ADMM'
            mission = True
            return goal, mission
    else:
        print('Invalid input, please try again')
        return None, False

# checks if a user has said 'Hey vale'
def hey_Vale(speech):
    hey_checker = {'hey', 'hay'}
    #Vale_checker = {'veil', 'vale', 'Vail', 'bail', 'bale'}
    if speech in hey_checker:# or speech in Vale_checker:
        return True
    else:
        return False

# checks to make sure the user input is valid
def user_input(speech):
    building_check = {'the academic building', 'academic building', 'Zachary', 'premiere', 'fermier',
             'Fermier', 'Zachary engineering building', 'Thompson', 'Zachary engineering complex', 'Zach', 'Vermeer', 'mirror', 'test'
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
   # speech = speech2text(r, talk)
    speech = str(input('Type Bitch: '))
    if speech == 'yes' or speech == 'yeah':
        return True
    else:
        return False

def reroute():  # reroutes gps
    s = str('Rerouting, please wait')
    os.system('echo \'' + s + '\' | festival --tts')

if __name__ == '__main__':
    begin()
    #speech = speech2text(r, talk)
    speech = str(input('Listen here: '))
    user_input(speech)
    

