import RPi.GPIO as GPIO
import os
import sys
import subprocess
from lcd import *

Play = 20
Prev = 21
Next = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(Play, GPIO.IN)
GPIO.setup(Prev, GPIO.IN)
GPIO.setup(Next, GPIO.IN)

lcd = LcdDisplay()

class MusicPlayer:
    Status = 0
    ChCount = 0
    CurrentChannel = 0
    

    def __init__(self):
        Status = 0
        cmd = subprocess.Popen('mpc playlist', shell = True, stdout = subprocess.PIPE)
        stations = cmd.stdout.readlines()
        self.ChCount = len(stations)
        self.CurrentChannel = 1

    def Play(self):
            cmd = subprocess.check_output('mpc play ' + str(self.CurrentChannel), shell=True, stderr=subprocess.STDOUT,
                                    universal_newlines=True)
            lcd.Display(cmd)

    def Stop(self):
            subprocess.check_output('mpc stop', shell=True, stderr=subprocess.STDOUT,
                                    universal_newlines=True)

    def PlayStop(self):
        if(self.Status == 0):
            self.Play()
            self.Status = 1
        elif(self.Status == 1):
            self.Stop()
            self.Status = 0

    def Forward(self):
        if (self.Status == 1):
            if(self.CurrentChannel<self.ChCount):
                self.CurrentChannel = self.CurrentChannel + 1
            else:
                self.CurrentChannel = 1
        self.Play()

    def Reverse(self):
        if (self.Status == 1):
            if(self.CurrentChannel>1):
                self.CurrentChannel = self.CurrentChannel - 1
            else:
                self.CurrentChannel = self.ChCount
        self.Play()    

    def VolUp(self):
        vol = 0

    def VolDown(self):
        vol = 0
        
    def Display_Channel(self):
        pass

    def Clear_Channel (self):
        pass

    def Display_Playlist(self):
        pass


    def Display_Volume(self):
        return vol


