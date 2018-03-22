import RPi.GPIO as GPIO
import sys
from time import *
import os
from datetime import datetime, date, time
from clockb import *
from playera import *
import paho.mqtt.client as mqtt

Alarm = 22
Snooze = 4
Min = 27
Hour = 17
Play = 12
Prev = 20
Next = 16
AlarmSet = False

ax = 0
xx = 0
status = set

GPIO.setmode(GPIO.BCM)
GPIO.setup(Hour, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(Min, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(Snooze, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(Alarm, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(Play, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(Prev, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(Next, GPIO.IN, pull_up_down = GPIO.PUD_UP)


def on_connect(client, userdata, flags, rc):
    print('connected')
    client.subscribe('/Apartment/Bedroom/Alarm')

def on_message(client, userdata, msg):
    print('message received')
    print('Topic: '+msg.topic+' Message: '+str(msg.payload))
    if msg.topic == '/Apartment/Bedroom/Alarm':
        if b'Alarm' in msg.payload:
            print('turn alarm on/off')
        elif b'Set' in msg.payload:
            print('inside setalarm')
            time = msg.payload
            timer = time.decode()
            print(timer)
            timelist = timer.split(',')
            hour = int(timelist[1])
            minute = int(timelist[2])
            print('hour: ',hour)
            print('minute: ',minute)
            Alrm1.SetMinute(minute)
            Alrm1.SetHour(hour)
            Alrm1.SetAlarmTime(hour,minute)
        elif b'Play' in msg.payload:
            player.PlayStop()
        elif b'Next' in msg.payload:
            player.Forward()
        elif b'Prev' in msg.payload:
            player.Reverse()

        
Alrm1 = AlarmClock(10,24,True)
player = MusicPlayer()
Alrm1.PrintAlarm()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect('192.168.1.172',1883,0)
client.loop_start()
print(datetime.now())
while True:
    Alrm1.SetTime()
    if (GPIO.input(Alarm) == False):
        print('alarm set button')
        Alrm1.EnterAlarmSet()

    if (Alrm1.PrintTime() == Alrm1.Time):
#        xx=1
        Alrm1.AlarmBoom()
#    if (Alrm1.PrintTime() != Alrm1.Time):
#        xx=0
    if (GPIO.input(Snooze) == False):
        Alrm1.Snooze()
    if (GPIO.input(Play) == False):
        player.PlayStop()
    if (GPIO.input(Next) == False):
        player.Forward()
    if (GPIO.input(Prev) == False):
        player.Reverse()
    sleep(.1)
