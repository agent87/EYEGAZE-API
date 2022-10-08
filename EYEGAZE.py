from multiprocessing import Process
from flask import Flask
import cv2
from gaze_tracking import GazeTracking
import pyautogui
import numpy as np
import time
from tkinter import *
from tkinter import ttk
import random


app = Flask(__name__)

global focus 
focus = {
        'direction':'',
        'lastupdate': 0
        }

def update_focus(direction):
    if focus['direction'] == direction:
        pass
    else:
        focus['direction'] = direction
        focus['lastupdate'] = time.time()


def app_frame():
    root = Tk()  
    root.attributes('-toolwindow', True)
    root.mainloop()


def screen_cam():
    SCREEN_SIZE = tuple(pyautogui.size())
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('recordings/output{}.avi'.format(random.randint(10,1000)), fourcc, 20.0, (SCREEN_SIZE))
    gaze = GazeTracking()
    webcam = cv2.VideoCapture(0)

    while True:
        # Capture the screen
        img = pyautogui.screenshot()
        # Convert the image into numpy array
        img = np.array(img)
        # Convert the color space from BGR to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        _, frame = webcam.read()
        # Finding the width, height and shape of our webcam image
        fr_height, fr_width, _ = frame.shape
        # setting the width and height properties
        img[0:fr_height, 0: fr_width, :] = frame[0:fr_height, 0: fr_width, :]
        #cv2.imshow('frame', img)
        # Write the frame into the file 'output.avi'
        out.write(img)
        # Press 'q' to quit
        ###########END OF RECORDER
        #gaze.refresh(frame)
        cv2.imshow('Frame',frame)


        if gaze.is_blinking():
            update_focus('Blinking')
            print('Blinking')
        elif gaze.is_right():
            update_focus('Right')
            print('Right')
        elif gaze.is_left():
            update_focus('Left')
            print('Left')
        elif gaze.is_center():
            update_focus('Center')
            print('Center')


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        out.release()
        cv2.destroyAllWindows()



@app.route('/status')
def status():
    return True

@app.route('/close')
def close():
    exit()
    return False



if __name__ =='__main__': 
    record_screen = Process(target=screen_cam)
    record_screen.start()
    