import time
import os
from tkinter import *
import threading
import pyttsx3
import random

import speech_recognition as sr
r = sr.Recognizer()

list_of_punctuations = {'comma':',', 'fullstop':'.','full stop':'.',
                        'new line':'\n','newline': '\n','colon':':',
                        "exclamation mark":'!',"semicolon":';',
                        'question mark':'?', 'hyphen':'-','underscore':'_','hash':'#'}

fnt1 = ('Trebuchet MS',12,'bold')
fnt2 = ('Century Gothic',20,'bold')

#Global Variables
btnAnim = 0 
rec = 0

def speakText(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty('voice',
        'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
        engine.setProperty('rate',120) # Speed percent (can go over 100)
        engine.setProperty('volume',0.9) # Volume 0-1
        engine.say(text)
        engine.runAndWait()
    except:
        pass

def stt():
    global btnAnim, rec, L2

    if(rec ==1):
        L2.delete(0.0,END)
        L2.insert(0.0," "*18+"Please Stay silent for few Seconds")
        print('Calibrating Microphone')
        print('Please be silent for few seconds.')
        time.sleep(1)
        
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source,duration=4)
            L2.delete(0.0,END)
            L2.insert(0.0," "*18+"          Speak Now")
            time.sleep(1)
           
        with sr.Microphone() as source:
            print("Say something!")
            try:
                audio = r.listen(source,timeout = 10)
            except Exception as e:
                print("MIC ERROR : ",e)

    # recognise speech using Google Speech Recognition
    try:
        b = r.recognize_google(audio)
        print('\n\n\n'+ b)
        
        for x in list_of_punctuations.keys():
            if x in b:
                b = b.replace(x, list_of_punctuations[x])
        
        print('\n\n\n'+ b)
        L2.delete(0.0,END)
        L2.insert(0.0,b)
        speakText(b)
        
        temp = str(random.randint(100,1000))
        f = open("storedText"+temp+".txt",'w')
        f.write(b)
        f.close()
        print("Output Saved in storedText"+temp+".txt")
            
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        L2.delete(0.0,END)
        L2.insert(0.0,"Speech Recognition could not understand audio.\nPlease Speak Clearly..!")
    except sr.RequestError as e:
        print("Could not request from Google Speech Recognition service;\n{0}".format(e))
        L2.delete(0.0,END)
        L2.insert(0.0,"Could not request from Google Speech Recognition service.\nPlease check for Internet Connection..!")

root = Tk()
root.title("Advance Speech to Text")
root.geometry("500x500+400+10")

N = 3 #change N value to exact number of frames your gif contains for full play 
frames = [PhotoImage(file='micrec.gif',format = 'gif -index %i' %(i)) for i in range(N)]

def update(ind):
    global btnAnim
    if(btnAnim==1):
        ind = ind%N
        frame = frames[ind]
        ind += 1
        B1.config(image=frame)
    root.after(100, update, ind)

def multiThreading():
    while True:
        stt()

t1 = threading.Thread(target = multiThreading)
t1.start()

def start1():
    global btnAnim, rec
    btnAnim = 1
    rec = 1

win = Frame(root, bg = 'powderblue')

L1 = Label(win, text="ADVANCE SPEECH TO TEXT")
L1.config(font = fnt2,bg = 'powderblue')
L1.place(x=25,y=10,height = 30,width = 450)

L2 = Text(win)
L2.config(font = fnt1)
L2.place(x=25,y=50,height = 200,width = 450)

B1 = Button(win)
photo = PhotoImage(file = "micrec.gif")
B1.config(image=photo,relief = RAISED, command = start1)
B1.config(bg='red')
B1.place(x = 150, y = 280, height = 200, width = 200)

win.place(x=0,y=0,height = 500,width = 500)
root.after(0, update, 0)
mainloop()



