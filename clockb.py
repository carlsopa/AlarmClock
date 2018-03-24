import RPi.GPIO as GPIO
from time import *
from datetime import datetime, date, time
import SevenSegment
import lcd as LCD
import os, sys, subprocess, paho.mqtt.client as mqtt


Bedroom_Lights = '192.168.1.172'
serverport = 5000
client = mqtt.Client()
Hour = 17
Min = 27
Alarm = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(Hour, GPIO.IN)
GPIO.setup(Min, GPIO.IN)
GPIO.setup(Alarm, GPIO.IN)
lcd = LCD.LcdDisplay()
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
    SetStatus = 'Inactive'
    
    def __init__(self):
        client.connect(Bedroom_Lights,1883)
        client.loop_start()
        self.Hour= 12
        self.Minute = 30
        self.Alarm = True
        self.Time = time(self.Hour, self.Minute)
        self.SetStatus = 'Inactive'
    
    def __init__(self, h, m, a):
        
        client.loop_start()
        self.Hour = h
        self.Minute = m
        self.Alarm = a
        self.Time = time(h, m)
        self.SetStatus = 'Inactive'

    def HourIncrease(self):
        if (self.Hour > 23):
            self.Hour = 0
        else:
            self.Hour +=1

    def HourDecrease(self):
        self.Hour -=1

    def SetHour(self,x):
        self.Hour = x

    def GetHour(self):
        return self.Hour

    def MinuteIncrease(self):
        if (self.Minute > 59):
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
        face.write_display()

    def DisplayMinute(self, m):
        pos = 2
        if len(str(m)) == 1:
            face.set_digit(2,0)
            face.set_digit(3,str(m))
        else:
            for i, ch in enumerate(str(m)):
                face.set_digit(pos,ch)
                pos += 1
        face.write_display()

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

    def PrintTime(self):
        return time(self.CurrentHour, self.CurrentMinute)

    def AlarmOnOff(self):
        #print('AlarmOnOff')
        #print(self.Alarm)
        if (self.Alarm == True):
            self.Alarm = False
            lcd.Print('Alarm Off')
            print('Alarm Off')
        else:
            self.Alarm = True
            lcd.Print('Alarm On')
            print('Alarm on')
            
    def SetAlarm(self):
        sleep(2)
        while(self.SetStatus == 'Active'):
            self.AlarmTimerSet()
            sleep(.25)

    def GetAlarmStatus(self):
        return self.Alarm

    def AlarmTimerSet(self):
        face.set_blink(0x04)
        self.DisplayHour(self.Hour)
        self.DisplayMinute(self.Minute)
        if (GPIO.input(Hour) == False):
            self.HourIncrease()
            self.DisplayHour(self.Hour)
            sleep(0.1)
        if (GPIO.input(Min) == False):
            self.MinuteIncrease()
            self.DisplayMinute(self.Minute)
            sleep(0.1)
        if (GPIO.input(Alarm) == False):
            #self.SetAlarm()
            self.SetAlarmTime(self.GetHour(),self.GetMinute())
            face.set_blink(0x00)
            self.SetStatus = 'Inactive'
            print('alarm false')

    def EnterAlarmSet(self):
        sleep(3)
        if (GPIO.input(Alarm) == False):
            self.SetStatus = 'Active'
            while(self.SetStatus == 'Active'):
                self.SetAlarm()
        else:
            #print('AlarmSet else')
            self.AlarmOnOff()

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
            NewMin = NewMin-60
        self.SetMinute(NewMin)
        NewHour = self.GetHour()
        self.SetAlarmTime(NewHour,NewMin)
        print('New: ',self.PrintAlarm())

    def AlarmBoom(self):
        #print('help')
        client = mqtt.Client()
        client.connect(Bedroom_Lights,1883)
        client.loop_start()
        client.publish('/Apartment/Bedroom/Lights','Left')
        client.publish('/Apartment/Bedroom/Lights','Right')
        subprocess.check_output('mpc play', shell=True, stderr=subprocess.STDOUT,
                                universal_newlines=True)
        #client.publish('/Apartment/Bedroom/Lights','Left')
        #client.publish('/Apartment/Bedroom/Lights'.'Right')
