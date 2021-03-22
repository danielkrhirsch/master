
import sys
import stream_engine as se
import threading
import pyautogui
from threading import Lock
import time
import matplotlib.pyplot as plt
import numpy as np
import time
import readchar
import subprocess
import os
import keyboard
#-----------------Useful copy&paste code-----------------------
# positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4) +'Valid: ' + str(valid).rjust(4) + ' ts: ' + str(ts).rjust(4)
# print(positionStr, end='')
# print('\b' * len(positionStr), end='', flush=True)


#-------------------------- EYE TRACKER-----------------------------
class Eyetracker():

    def __init__(self):
        self.tstemp=0
        self.xtemp=0
        self.ytemp=0
        self.iter=0
        self.xvec_pixel=[]
        self.yvec_pixel=[]
        self.xvec = []
        self.yvec = []
        self.width_res = pyautogui.size()[0] - 1
        self.height_res = pyautogui.size()[1] - 1  # minus en för pyautogui mouseover börjar på 0
        self.threshold=15#Threshold for readings
        self.xmove=None
        self.ymove=None
        self.ctime=time.time()
        self.freq=70
        self.timedelta=3
        self.api = se.Api()
        self.device_urls = self.api.enumerate_local_device_urls()
        self.d=self.api.device_create(self.device_urls[0])
        #self.key=keyboard.add_hotkey("ctrl",lambda: pyautogui.click())
        pyautogui.FAILSAFE = False




    def gaze_point(self,x, y, valid, ts):


        if x>1:
            x=1
        if x<0:
            x=0

        if y>1:
            y=1
        if y<0:
            y=0


        #-------------------------- Transform to pixel values ------------------------
        if time.time()-self.ctime>=((1/self.freq)*self.timedelta):
            x_pixel, y_pixel = self.gaze_to_pixel_transform(x, y)
            self.move_mouse(x_pixel,y_pixel)




            self.ctime=time.time()

        # -------------------------- Send to move mouse ------------------------


        #if abs(self.starttime-time.time())>=1:
        #    frequency=self.iter
        #    print("Frequency", frequency)
        #    quit()

    def gaze_to_pixel_transform(self,x,y):

        x_pixel=int(x*self.width_res)
        y_pixel=int(y*self.height_res)

        return x_pixel, y_pixel

    def click(self):
        pyautogui.click()

    def move_mouse(self,x_pixel,y_pixel):

        pyautogui.moveTo(x_pixel, y_pixel)


    def start_eyetracker(self):

        if not self.device_urls:
            print("No eye tracker connected!")
            return

        self.d.gaze_point_subscribe(self.gaze_point)
        tread=threading.Thread(self.d.run())
        tread.start()
    ####################################################################

    def stop_eyetracker(self):
        self.d.stop()








if __name__ == '__main__':

    et = Eyetracker()
    et.start_eyetracker()


    #et.stop_eyetracker()
#    try:
        #subprocess.Popen(["dconf", "write", "/org/gnome/desktop/interface/cursor-size", '48'])
        #subprocess.Popen(["dconf", "write", "/org/gnome/desktop/interface/cursor-theme", "'redglass'"])
#        et.start_eyetracker()
#    except KeyboardInterrupt:

#        et.stop_eyetracker()
        #subprocess.Popen(["dconf", "write", "/org/gnome/desktop/interface/cursor-size", '16'])
        #subprocess.Popen(["dconf", "write", "/org/gnome/desktop/interface/cursor-theme", "'yaru'"])





