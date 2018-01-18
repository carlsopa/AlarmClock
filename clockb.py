import RPi.GPIO as GPIO
from time import *
from datetime import datetime, date, time
from Adafruit_LED_Backpack import SevenSegment
import os
import sys
import subprocess
import paho.mqtt.client as mqtt

Bedroom_Lights = '192.168.1.172'
serverport = 5000
client = mqtt.Client()
Hour = 24
Min = 25
Alarm = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(Hour, GPIO.IN)
GPIO.setup(Min, GPIO.IN)
GPIO.setup(Alarm, GPIO.IN)

face = SevenSegment.SevenSegment()
face.begin()
face.set_brightness(0)
face.set_blink(0x00)

class AlarmClock:
    face.set_colon(True)
    Hour = 0
    Minute = 0
    Alarm = False
    AlarmTime = time(Hour, Minute)
    CurrentHour = 10
    CurrentMinute = 30
    
    def __init__(self):
        client.connect(Bedroom_Lights,1883)
        client.loop_start()
        self.Hour= 12
        self.Minute = 30
        self.Alarm = True
        self.Time = time(self.Hour, self.Minute)
    
    def __init__(self, h, m, a):
        client.connect(Bedroom_Lights,1883)
        client.loop_start()
        self.Hour = h
        self.Minute = m
        self.Alarm = a
        self.Time = time(h, m)

    def HourIncrease(self):
        if (self.Hour > 23):
            self.Hour = 1
        else:
            self.Hour +=1

    def HourDecrease(self):
        self.Hour -=1

    def SetHour(self,x):
        self.Hour = x

    def GetHour(self):
        return self.Hour

    def MinuteIncrease(self):
        if (self.Minute > 60):
            self.Minute = 0
        else:
            self.Minute +=1

    def MinuteDecrease(self):
        self.Minute -=1

    def SetMinute(self,x):
        self.Minute = x

    def GetMinute(self):
         return self.Minute

    def DisplayHour(self, h):
        pos = 0
        if len(str(h)) == 1:
            face.set_digit(0,0)
            face.set_digit(1,str(h))
        else:
            for i, ch in enumerate(str(h)):
                face.set_digit(pos,ch)
                pos += 1
        #face.write_display()

    def DisplayMinute(self, m):
        pos = 2
        if len(str(m)) == 1:
            face.set_digit(2,0)
            face.set_digit(3,str(m))
        else:
            for i, ch in enumerate(str(m)):
                face.set_digit(pos,ch)
                pos += 1
        #face.write_display()

    def SetAlarmTime(self,h,m):
        self.Time = time(h, m)

    def PrintAlarm(self):
        return self.Time

    def SetTime(self):
        Current= datetime.now()
        self.CurrentHour = Current.hour
        self.CurrentMinute = Current.minute
        self.DisplayHour(self.CurrentHour)
        self.DisplayMinute(self.CurrentMinute)
        face.write_display()
        #print(face.readRaw8)

    def PrintTime(self):
        return time(self.CurrentHour, self.CurrentMinute)

    def SetAlarm(self):
        if (self.Alarm == True):
            self.Alarm = False
            print('alarm off')
        else:
            self.Alarm = True
            print('alarm on')

    def GetAlarmStatus(self):
        return self.Alarm

    def AlarmTimerSet(self):
        face.clear()
        face.set_blink(0x04)
        if (GPIO.input(Hour) == False):
            self.HourIncrease()
            self.DisplayHour(self.Hour)
            sleep(0.1)
            print(self.GetHour())
        if (GPIO.input(Min) == False):
            self.MinuteIncrease()
            self.DisplayMinute(self.Minute)
            sleep(0.1)
            print(self.GetMinute())
        if (GPIO.input(Alarm) == False):
            self.SetAlarm()
            print('alarm false')

    def Snooze(self):
        subprocess.check_output('mpc stop', shell=True, stderr=subprocess.STDOUT,
                                universal_newlines=True)
        
        print('PrintTime(): ',self.PrintTime())
        print('Time: ',self.Time)
        print('Old: ',self.PrintAlarm())
        print('hour: ',self.GetHour())
        print('minute: ',self.GetMinute())
        NewMin = self.GetMinute() + 5
        if NewMin>59:
            self.HourIncrease()
            print(NewMin-60)
            NewMin = NewMin-60
        self.SetMinute(NewMin)
        print(NewMin)
        NewHour = self.GetHour()
        #print(NewMin)
        self.SetAlarmTime(NewHour,NewMin)
        print('New: ',self.PrintAlarm())
        #sleep(30)

    def AlarmBoom(self):
        print('help')
        subprocess.check_output('mpc play', shell=True, stderr=subprocess.STDOUT,
                                universal_newlines=True)
        client.publish('bedroom/lights','')

