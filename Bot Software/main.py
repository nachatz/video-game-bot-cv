import cv2 as cv
import numpy as np
import os
import pyautogui
from time import time, sleep
from screencapture import WindowCapture
from computervision import ComputerVision
from hsvfilter import HsvFilter
from threading import Thread
from tkinter import *
import entry
import win32api



#TKINTER ----------------------------------------------------------------------------------
def myClick():
    global inp
    inp = e.get()


def myClick2():
    global SLEEP_TIMER
    SLEEP_TIMER = e.get()


root = Tk()
root.title('Bot by Nikolas Achatz')
e = Entry(root, width= 60)
e.pack()
inp = None
SLEEP_TIMER = 0.2
Button(root, text='Enter client name (Leave empty for desktop view)', command=myClick).pack()
Button(root, text='Sleep Timer for actions', command=myClick2).pack()
Button(root, text="Send", command=root.destroy).pack()
root.mainloop()

#TKINTER END ----------------------------------------------------------------------------------

print("Client Window " + inp)
print("Ticker " + SLEEP_TIMER)

inp = "League of Legends (TM) Client"

#This is the window we want to capture and work with.
wincap = entry.attemptDataSend(inp)


#THIS IS WHAT WE WANT TO FIND in our window
if inp == "Runescape":
    cv_find = ComputerVision('runescapet.JPG')
elif inp == "League":
    cv_find = ComputerVision('minion.JPG')
else:
    cv_find = ComputerVision('runescapet.JPG')

# else:
#     win32api.MessageBox(0, 'You did not attach to a good client, we have nothing to search for.', 'Error')
#     exit(0)




#This is to find our HSV values for new objects.
#cv_find.init_control_gui()


#Determines if we are already doing a task.
is_in_action = False

#This is our preset HSV values for processed searches
if inp == "Runescape":
    hsv_filter = HsvFilter(0, 137, 0, 20, 221, 96, 52, 0, 0, 0)
else:
    hsv_filter = HsvFilter(0,74,33,8,255,255,0,0,0,0)


# Using a different thread we can run the bot actions in parallel
def bot_action(rectangles):
    if len(rectangles) > 0:
        targets = cv_find.get_click_points(rectangles)
        target = wincap.get_screen_position(targets[0])
        pyautogui.moveTo(x=target[0], y=target[1])
        pyautogui.click(button='right')
        sleep(int(SLEEP_TIMER))
        global is_in_action
        is_in_action = False


#Used for FPS monitoring. Not needed
#loop_time = time()

while(True):

    # Continuously grabs the image on the screen using windows OS
    screenshot = wincap.get_screenshot()

    # This is our normal image being modified by the HSV values set above
    processed_img = cv_find.apply_hsv_filter(screenshot, hsv_filter)

    # FINDS INSTANCES OF THE OBJECT WE WANT TO FIND, second value is adjusted to change acceptance
    rectangles = cv_find.find(processed_img, 0.28)

    # Draw the rectangles of positive matches
    output_img = cv_find.draw_rectangles(screenshot, rectangles)


    cv.imshow("Processed", processed_img)
    cv.imshow("Matches", screenshot)

    # Bot action thread, if we aren't in a thread, we can send a new task out.
    if not is_in_action:
        is_in_action = True
        t = Thread(target=bot_action, args=(rectangles,))
        t.start()


    #print('FPS {} '.format(1 /(time() - loop_time)))
    #loop_time = time()


    key = cv.waitKey(1)
    if key == ord('q'):
        cv.destroyAllWindows()
        break



print("done")