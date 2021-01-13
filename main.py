import pyautogui as pag
import math
import tkinter as tk
from tkinter import *
import pytesseract as pt
import nltk
import pyttsx3
from bs4 import BeautifulSoup
import requests

def started():
    champstr = champText.get(1.0, tk.END).splitlines()
    global c
    c = []
    for i in champstr:
        if i != "":
            c.append(i)
    window.after(1000, task)

def rewrite(premade):
    champText.delete(1.0, END)
    c = premade.split()
    for i in c:
        champText.insert(END, i+"\n")

def task():
    screenx, screeny = pag.size()
    ss = pag.screenshot(region=(0, screeny / 2, screenx, screeny))
    ss.save(r'ss\shot.png')
    pt.pytesseract.tesseract_cmd = r'tess\tesseract'
    avail = pt.image_to_string(r'ss\shot.png', config='--psm 12')

    for i in c:
        if find(i, avail.split()):
            #playsound('store.wav')
            engine.say(i)
            engine.runAndWait()
    window.after(1000,task)

def find(a, b):
    found = False
    i = 0
    while not found and i <len(b):
        if nltk.edit_distance(a, b[i]) <= math.floor(len(a)/3):
            found = True
        i+=1
    return found

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
window = tk.Tk()
champLabel = tk.Label(text="enter champions/synergies below, separated by line")
champLabel.pack()
champText = tk.Text()
champText.pack()

url = 'https://app.mobalytics.gg/tft/set4/team-comps'
page = requests.get(url).text
soup = BeautifulSoup(page, 'html.parser')
comps=[[]]
i = 0
j = 0
for link in soup.find_all('a'):
    if "/tft/champions/" in (link.get('href')):
        if j != 0 and j<8:
            comps[i].append((link.get('href'))[15:])
            j+=1
        else:
            comps.append([(link.get('href'))[15:]])
            j = 1
            i+=1

comps = comps[1:]
variable = StringVar(window)
variable.set("premade meta comps") # default value
w = OptionMenu(window, variable, " ".join(comps[0]), " ".join(comps[1]), " ".join(comps[2]), " ".join(comps[3]), " ".join(comps[4]), " ".join(comps[5]), " ".join(comps[6]), command = rewrite)
w.pack()
startB = tk.Button(text="click when start", command=started)
endB= tk.Button(text="click to end", command=window.destroy)
startB.pack()
endB.pack()
window.mainloop()
