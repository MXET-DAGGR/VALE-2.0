# to run this code you will need internet connection
# if running for the first time pip install SpeechRecognition
# if running for the first time pip install pyaudio
# make sure the correct microphone is selected run sudo raspi-config, then select advanced, then mic
# the purpose of this code is to go through the valid user inputs for building input
import os
import time
import speech_recognition as sr

# these are needed for speech recognition and microphone input
global r
global talk
global recog
r = sr.Recognizer()
talk = sr.Microphone(device_index=1) #make sure to check what index is the external microphone
recog = ' ' #This variable is to get the text that the user says

# these dictonaries hold valid building destinations for VALE2.0
AC = ['academic building', 'the academic building', 'academic', 'Academic Building', 
    'The Academic Building', 'Academic', 'stomach building', 'akademiks', 'epidemic']

FER = ['fermier', 'premier', 'premiere', 'vermeer', 'ferm', 'fermier hall', 
        'premier hall', 'vermeer hall', 'premiere hall', 'Fermier', 'Premier', 'Premiere', 
        'Vermeer', 'Ferm', 'Fermier Hall', 'Premier Hall', 'Vermeer Hall', 'Premiere Hall', 'bummer']

TH = ['Thompson', 'Thom', 'Thumb', 'Tumson', 'Tom', 'Thompson Hall', 'Thumbson Hall', 
        'Tomson hall', 'Tumson hall']

BL = ['Blocker', 'bloc', 'block', 'blocker building', 'bloc building', 'block building']

# this is the function that gets speech input and converts it to text
def speech2text(recog):
    with talk as source:
        r.adjust_for_ambient_noise(source)
        print('say something…')
        audio = r.listen(source, phrase_time_limit=10)
        try:
            recog = r.recognize_google(audio, language='en-US')
            print(recog)
            return recog
        except Exception as e:
            print("Error: " + str(e))

# checks if a user has said 'Hey VALE' before being in route
def Begin_VALE():
    checker = ['hey veil', 'hey vale', 'hey Vail', 'hey bail', 'hey bale', 'hey Val', 'hey bal',
                'hay veil', 'hay vale', 'hay Vail', 'hay bail', 'hay bale', 'hay Val', 'hay bal', 
                'kval', 'Hapeville', 'hey bill', 'hay bill', 'hey april', 'hey', 'hay', 'Yo', 'Vale', 
                'veil', 'vale','Vail', 'bail', 'bale', 'bill', 'bell']
    i = 0
    speech = speech2text(recog)
    while i == 0:
        if any(i in speech for i in checker):
            begin()
            i +=1
        else:
            speech = speech2text(recog)

# this is where the first input it asked
def begin():
    os.system("afplay " + "VALE_Intro.mp3")


# return building code for the API search
def check_bldg(speech):
    i = 0
    while i == 0:
        if any(sub in speech for sub in AC):
            print('ACAD')
            os.system("afplay " + "ASK_ACAD.mp3")
            check = yes_no()
            if check == True:
                os.system("afplay " + "Follow_ACAD.mp3")
                i +=1
                return 'ACAD', True
            else:
                os.system("afplay " + "Other.mp3")
                speech = speech2text(recog)
        elif any(sub in speech for sub in FER):
            print('FERM')
            os.system("afplay " + "Ask_FERM.mp3")
            check = yes_no()
            if check == True:
                os.system("afplay " + "Follow_FERM.mp3")
                i +=1
                return 'FERM', True
            else:
                os.system("afplay " + "Other.mp3")
                speech = speech2text(recog)
        elif any(sub in speech for sub in TH):
            print('THOM')
            os.system("afplay " + "ASK_THOM.mp3")
            check = yes_no()
            if check == True:
                os.system("afplay " + "Follow_THOM.mp3")
                i +=1
                return 'THOM', True
            else:
                os.system("afplay " + "Other.mp3")
                speech = speech2text(recog)
        elif any(sub in speech for sub in BL):
            print('BLOC')
            os.system("afplay " + "Ask_Bloc.mp3")
            check = yes_no()
            if check == True:
                os.system("afplay " + "Follow_Bloc.mp3")
                i +=1
                return 'BLOC', True
            else:
                os.system("afplay " + "Other.mp3")
                speech = speech2text(recog)
                
        else:
            os.system("afplay " + "Repeat2.mp3")
            speech = speech2text(recog)
            #return None, False

# checks to make sure the user input is valid
def user_input(speech):
    building_check = {'academic building', 'the academic building', 'academic', 'Academic Building', 
    'The Academic Building', 'Academic', 'akademiks', 'stomach building', 'fermier', 'premier', 'premiere', 'vermeer', 'ferm', 
    'fermier hall', 'premier hall', 'vermeer hall', 'premiere hall', 'Fermier', 'Premier', 'Premiere', 
    'Vermeer', 'Ferm', 'Fermier Hall', 'Premier Hall', 'Vermeer Hall', 'Premiere Hall', 'Thompson', 
    'Thom', 'Thumb', 'Tumson', 'Tom', 'Thompson Hall', 'Thumbson Hall', 'Tomson hall', 'Tumson hall',
    'Blocker', 'bloc', 'block', 'blocker building', 'bloc building', 'block building'
             }

# this is the function for yes or no input
def yes_no():
    yesses = ['yes', 'Yes', 'Jes', 'jes', 'jess', 'Yess', 'yess', 'yeah', 'affirmative', 'correct']
    nos = ['no', 'wrong', 'No', 'Nah', 'Na']
    val = speech2text(recog)
    i = 0
    while i == 0:
        if any(i in val for i in yesses):
            print("User said yes.")
            i+=1
            return True
        elif any(i in val for i in nos):
            print("User said no.")
            i+=1
            return False
        else:
            print("Invalid input.")
            os.system("afplay " + "Invalid.mp3")
            val = speech2text(recog)

if __name__ == '__main__':
    Begin_VALE()    
    speech = speech2text(recog)
    user_input(speech)
    check_bldg(speech)
