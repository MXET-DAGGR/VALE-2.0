#to run this code you will need internet connection
#if running for the first time pip install SpeechRecognition
#if running for the first time pip install pyaudio
#make sure the correct microphone is selected run sudo raspi-config, then select advanced, then mic
#the purpose of this code is to go through the valid user inputs for building input
import os
import speech_recognition as sr

#these are needed for speech recognition and microphone input
#r = sr.Recognizer()
talk = sr.Microphone(device_index=None)
r = sr.Recognizer()
#these dictonaries hold valid building destinations for VALE

AC = {'academic building', 'the academic building'}

FER = {'fermier', 'premier', 'premiere', 'Vermeer'}

TH = {'Thompson'}

ZE = {'Zachary engineering education complex', 'Zachary',
        'Zach', 'Zachary engineering complex'}

AD = {'administrative building'}

#this is the function that gets speech input
def speech_talk(r, talk):
    with talk as source:
        print("say something!…")
        audio = r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        recog = r.recognize_google(audio, language = 'en-US')
        print(recog)
        return recog
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
#this is where the first input it asked
def speech_rec(r, talk):
    speech = str('Welcome to VALE the autonomous guidebot of the future! Please input the entirety of the building name you would like to go to.'
                   'If you need to stop at any point please say stop and say go when vale can resume. Where would you like to go?')
    os.system("echo \"" + speech + "\" | festival --tts")
    return

#return building code for the API search
def check_word(speech):
    if speech in AC:
        ACAD = str('ACAD')
        print(ACAD)
        return ACAD

    if speech in FER:
        FERM = str('FERM')
        print(FERM)
        return FERM

    if speech in TH:
        THOM = str('THOM')
        print(THOM)
        return THOM

    if speech in ZE:
        ZEEC = str('ZEEC')
        print(ZEEC)
        return ZEEC

    if speech in AD:
        ADMM = str('ADMM')
        print(ADMM)
        return ADMM

    else:
        print('not valid')
   
#checks to make sure the user input is valid
def user_input(speech):
    check = {"the academic building", "academic building", "Zachary", "premiere", "fermier",
             "Fermier", "Zachary engineering building", "Thompson", "Zachary engineering complex", "Zach", "Vermeer"
             }
    why = speech
    if speech in check:
            question = str('Did you want to go to the')
          
            q =str('Say yes or no.')
            os.system("echo \"" + question + why + q + "\" | festival --tts")
            yes_no()
    else:
            speech = str('Input something else')
            os.system("echo \"" + speech + "\" | festival --tts")
            return
#this is the function for yes or no input        
def yes_no():   
    speech = speech_talk(r, talk)
    if speech == 'yes':
            s = str('ok follow me')
            os.system("echo \"" + s + "\" | festival --tts")
            check_word(speech)
            #put in driving here
            
    else:
            s = str('Input something else')
            os.system("echo \"" + s + "\" | festival --tts")
            return

def reroute():  #reroutes gps
    s = str('Rerouting, please wait')
    os.system("echo \"" + s + "\" | festival --tts")
            

speech = speech_rec(r, talk)
#uncomment this loop for continous running
while(1):
    speech = speech_talk(r, talk)
    #speech is the user input
    user_input(speech)

        
   