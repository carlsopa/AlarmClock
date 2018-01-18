import RPi.GPIO as GPIO
import sys
from time import *
import os
from datetime import datetime, date, time
from clockb import *
from playera import *
import paho.mqtt.client as mqtt

Alarm = 18#12
Snooze = 23#16
Min = 24#18
Hour = 25#22
Play = 21#40
Prev = 20#38
Next = 16#36
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
    client.subscribe('bedroom/alarm')

def on_message(client, userdata, msg):
    print('message received')
    print('Topic: '+msg.topic+' Message: '+str(msg.payload))
    if msg.topic == 'bedroom/alarm':
        if b'Alarm' in msg.payload:
            print('turn alarm on/off')
        elif b'Set' in msg.payload:
            print('inside setalarm')
            time = msg.payload
            timer = time.decode()
            timelist = timer.split(',')
            hour = int(timelist[1])
            minute = int(timelist[2])
            print('hour: ',hour)
            print('minute: ',minute)
            Alrm1.SetMinute(minute)
            Alrm1.SetHour(hour)
            Alrm1.SetAlarmTime(hour,minute)
            print('alarm time: ',Alrm1.PrintAlarm())
        elif b'Play' in msg.payload:
            print('turn on/off radio')
            player.PlayStop()
        elif b'Next' in msg.payload:
            print('play next song')
            player.Forward()
        elif b'Prev' in msg.payload:
            print('play previous song')
            player.Reverse()

def SetAlarm():
    print('inside setalarm')
    sleep(5)
    ax = 0
    while(ax == 0):
        Alrm1.AlarmTimerSet()
        sleep(.25)
        if (GPIO.input(Alarm) == False):
            Alrm1.SetAlarmTime(Alrm1.GetHour(),Alrm1.GetMinute())
            face.set_blink(0x00)
            ax = 1
            print('finale alarm time: ',Alrm1.PrintAlarm())
  
Alrm1 = AlarmClock(18,32,True)
#player = MusicPlayer()
Alrm1.PrintAlarm()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect('192.168.1.172',1883,60)
client.loop_start()
print(datetime.now())
while True:
    
    Alrm1.SetTime()
    if (GPIO.input(Alarm) == False):
        print('before sleep pressed')
        sleep(3)
        if (GPIO.input(Alarm) == False):
            SetAlarm()
    if (Alrm1.PrintTime() == Alrm1.Time and xx ==0):
        print('if loop')
        xx=1
        Alrm1.AlarmBoom()
    if (Alrm1.PrintTime() != Alrm1.Time):
        xx=0
    if (GPIO.input(Snooze) == False):
        Alrm1.Snooze()

    if (GPIO.input(Play) == False):
        print('Play/stop')
        player.PlayStop()
    if (GPIO.input(Next) == False):
        print('Next')
        player.Forward()
        print('after next')
    if (GPIO.input(Prev) == False):
        print('prev')
        player.Reverse()
        print('after prev')
    sleep(.1)
