from tkinter import *
from screencapture import WindowCapture

def attemptDataSend(inp):
    try:
        value = WindowCapture(inp)
    except:
        value = WindowCapture()

    return value

def myClick(e):
    global inp
    inp = e.get()
    return inp
