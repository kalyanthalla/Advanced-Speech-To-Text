import time
import os
from tkinter import *
import threading
import pyttsx3
import random
import speech_recognition as sr

r = sr.Recognizer()
list_of_punctuations = {'comma': ',', 'fullstop': '.', 'full stop': '.',
                        'new line': '\n', 'newline': '\n', 'colon': ':',
                        "exclamation mark": '!', "semicolon": ';',
                        'question mark': '?', 'hyphen': '-', 'underscore': '_', 'hash': '#'}

fnt1 = ('Trebuchet MS', 12, 'bold')
fnt2 = ('Century Gothic', 20, 'bold')

# Global Variables
btnAnim = 0
rec = 0
L2 = None  # Define L2 globally to avoid reference issues

def speakText(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 120)
        engine.setProperty('volume', 0.9)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print("Error in TTS:", e)

def stt():
    global btnAnim, rec, L2
    if rec == 1:
        L2.delete(0.0, END)
        L2.insert(0.0, " " * 18 + "Please Stay silent for a few Seconds")
        print('Calibrating Microphone')
        time.sleep(1)

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=4)
            L2.delete(0.0, END)
            L2.insert(0.0, " " * 18 + "Speak Now")
            time.sleep(1)

        with sr.Microphone() as source:
            print("Say something!")
            try:
                audio = r.listen(source, timeout=10)
            except Exception as e:
                print("MIC ERROR:", e)
                return

    try:
        b = r.recognize_google(audio)
        print('\n\n\n' + b)
        
        for x in list_of_punctuations.keys():
            if x in b:
                b = b.replace(x, list_of_punctuations[x])
        
        print('\n\n\n' + b)
        L2.delete(0.0, END)
        L2.insert(0.0, b)
        speakText(b)
        
        temp = str(random.randint(100, 1000))
        with open(f"storedText{temp}.txt", 'w') as f:
            f.write(b)
        print(f"Output Saved in storedText{temp}.txt")
        
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        L2.delete(0.0, END)
        L2.insert(0.0, "Speech Recognition could not understand audio.\nPlease Speak Clearly..!")
    except sr.RequestError as e:
        print(f"Could not request from Google Speech Recognition service; {e}")
        L2.delete(0.0, END)
        L2.insert(0.0, "Could not request from Google Speech Recognition service.\nPlease check your Internet Connection..!")

def update(ind):
    global btnAnim
    if btnAnim == 1:
        ind = ind % N
        frame = frames[ind]
        B1.config(image=frame)
        ind += 1
    root.after(100, update, ind)

def multiThreading():
    while True:
        stt()

def start1():
    global btnAnim, rec
    btnAnim = 1
    rec = 1
    threading.Thread(target=stt, daemon=True).start()  # Start stt() in a separate thread

# Initialize GUI
root = Tk()
root.title("Advanced Speech to Text")
root.geometry("500x500+400+10")

N = 3  # Change N to the actual number of frames your gif contains
frames = [PhotoImage(file='micrec.gif', format=f'gif -index {i}') for i in range(N)]

win = Frame(root, bg='powderblue')
L1 = Label(win, text="ADVANCED SPEECH TO TEXT", font=fnt2, bg='powderblue')
L1.place(x=25, y=10, height=30, width=450)

L2 = Text(win, font=fnt1)
L2.place(x=25, y=50, height=200, width=450)

B1 = Button(win, command=start1)
photo = PhotoImage(file="micrec.gif")
B1.config(image=photo, relief=RAISED, bg='red')
B1.place(x=150, y=280, height=200, width=200)

win.place(x=0, y=0, height=500, width=500)
root.after(0, update, 0)
root.mainloop()




