
import sys
import stream_engine as se
import threading
import pyautogui
from threading import Lock
import time
import matplotlib.pyplot as plt
import numpy as np
import readchar


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

    def gaze_point(self,x, y, valid, ts):
        #key=readchar.readkey()

        delta_t=ts-self.tstemp
        #if self.iter>=1:
            #tsstr = 'tstemp: ' + str(self.tstemp).rjust(4) + ' ts: ' + str(ts).rjust(4) + ' delta_t: ' + str(delta_t).rjust(4)

         #   delta_x = x - self.xtemp
          #  delta_y = y - self.ytemp

           # x_vel=delta_x/delta_t
            #y_vel=delta_y/delta_t
            #velstr = 'x_vel: ' + str(x_vel).rjust(4) + ' y_vel: ' + str(y_vel).rjust(4)

            #print(tsstr)
            #print(velstr)




        #-------Printa nedan för att se (0,1) koordinat-system.-----
        #positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4) +'Valid: ' + str(valid).rjust(4) + ' ts: ' + str(ts).rjust(4)
        #print(positionStr, end='')
        #print('\b' * len(positionStr), end='', flush=True)
#
        #-------------Se till att punkter ej hamnar utanför då de annars blir fel i transformation,
        #-------------dvs ett tal över ett ger eskalerande värden
        if x>1:
            x=1
        if x<0:
            x=0

        if y>1:
            y=1
        if y<0:
            y=0


        #-------------------------- Transform to pixel values ------------------------
        x_pixel, y_pixel = self.gaze_to_pixel_transform(x, y)

        if abs(x_pixel-self.xtemp)>self.threshold or abs(y_pixel-self.ytemp)>self.threshold:
            #print("x_pixel",x_pixel)
            #print("x_temp", self.xtemp)
            #print(type(self.xtemp))

            #print("y_pixel", y_pixel)
            #print("y_temp", self.ytemp)

            #print("xabs", abs(x_pixel-self.xtemp))
            #print("yabs", abs(y_pixel-self.ytemp))
            #self.iter=0
            self.xmove=x_pixel
            self.ymove=y_pixel
            print("x",self.xmove)
            print("y",self.ymove)
            self.move_mouse(self.xmove, self.ymove)



        #if key=='e':
        #
        #    self.move_mouse(self.xmove, self.ymove)

            #positionStr = 'X: ' + str(x_pixel).rjust(4) + ' Y: ' + str(y_pixel).rjust(4)


        #if key=='e':


            #


        # -------Printa nedan för att se pixel koordinat-system värden.-----
        #positionStr = 'X: ' + str(x_pixel).rjust(4) + ' Y: ' + str(y_pixel).rjust(4)
        #print(positionStr, end='')
        #print('\b' * len(positionStr), end='', flush=True)

        #self.move_mouse(x_pixel,y_pixel)
        #positionStr = 'X: ' + str(x_pixel).rjust(4) + ' Y: ' + str(y_pixel).rjust(4)
        #print(positionStr)
        #if abs(self.xtemp-x_pixel) or abs(self.ytemp-y_pixel) >=50:

        #



        self.tstemp=ts
        self.xtemp=x_pixel
        self.ytemp=y_pixel
        self.xvec.append(x)
        self.yvec.append(y)
        self.xvec_pixel.append(x_pixel)
        self.yvec_pixel.append(y_pixel)
        self.iter+=1
        #print(self.iter)


        #if self.iter==1000:
        #    print("Iteration done!")
#
        #    valueforplot=np.arange(0, self.iter+1, 1).tolist()
#
#
        #    plt.figure(1)
        #    plt.subplot(221)
        #    plt.plot(self.xvec_pixel, self.yvec_pixel, 'rx')
        #    plt.axis([0,self.width_res, 0, self.height_res])
        #    plt.title("Pixelvärden, x_pixel mot y_pixel med resolution på axlarna")
#
        #    plt.subplot(223)
        #    plt.plot(self.xvec_pixel)
        #    #plt.axis([0, self.width_res, 0, len(self.xvec_pixel)])
        #    plt.title("x_pixel")
        #    plt.subplot(224)
        #    plt.plot(self.yvec_pixel,valueforplot)
        #    #plt.axis([0, len(self.yvec_pixel), 0, self.height_res])
        #    plt.title("y_pixel")
        #    plt.show()
        #    quit()







    def gaze_to_pixel_transform(self,x,y):

        x_pixel=int(x*self.width_res)
        y_pixel=int(y*self.height_res)

        return x_pixel, y_pixel


    def move_mouse(self,x_pixel,y_pixel):

        pyautogui.moveTo(x_pixel, y_pixel)


    def start_eyetracker(self):
        api = se.Api()
        device_urls = api.enumerate_local_device_urls()
        if not device_urls:
            print("No eye tracker connected!")
            return
        d = api.device_create(device_urls[0])
        d.gaze_point_subscribe(self.gaze_point)
        d.run()
    ####################################################################

    #------------------------Print mouse position-----------------------
    def mouseposition(self):
        try:
            while True:
                x, y = pyautogui.position()
                positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
                print(positionStr, end='')
                print('\b' * len(positionStr), end='', flush=True)


        except KeyboardInterrupt:
            return
    #####################################################################






if __name__ == '__main__':
    pyautogui.FAILSAFE = False
    et=Eyetracker()
    et.start_eyetracker()



