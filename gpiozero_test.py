from gpiozero import Button
import time
from psonic import *
from threading import Thread
from json import load as json_load
from numpy import random

set_server_parameter('127.0.0.1',4557,4559)

BEATS_PER_MINUTE=140
KEY_SIGNATURE="C"
TIME_SIGNATURE_TOP=4
TIME_SIGNATURE_TOP=4

DEBUG = False

with open("templates.json") as file:
    templates = json_load(file)
    file.close()
    
#with open("instruments.json") as file:
#    templates = json_load(file)
#    file.close()

print(templates)

beat_length = 60/140
bar_length = beat_length * TIME_SIGNATURE_TOP

tracklist = []

def threaded(fn):
    def wrapper(*args, **kwargs):
        Thread(target=fn, args=args, kwargs=kwargs).start()
    return wrapper

def new_bar(role, strum_pattern):
    bar=[]
    print(strum_pattern)
    role = "melody"
    if role == "melody":
        tie = False
        for i in strum_pattern:
            if random.randint(0,6) == 0: tie = True
            if tie:
                bar.append("tie")
            elif i == "1":
                bar.append(random.choice(chord(C4,MAJOR7)))
            else:
                bar.append(None)
    return bar
            
                

class Track:
    def __init__(self):
        global DEBUG
        global templates
        if DEBUG: print("new Track object created")
        self.end=False
        self.instrument=""
        self.template=templates[str(random.randint(1,len(templates.keys())))]
        
        
        self.shuffle()
    def end_tasks(self):
        self.end=True
    def shuffle(self):
        self.bars=[]
        self.default_asdr={
            "attack":0.5,
            "attack_level":1,
            "decay":1,
            "sustain_level":1,
            "sustain":0,
            "release":0.5
            }
        if DEBUG: print(str(self)+" is being shuffled")
        print(self.template)
        for bar in range(int(self.template["bars"])):
            keys=[]
            for key in self.template["strum_patterns"].keys():
                keys.append(key)
            self.bars.append(new_bar(self.template["role"],self.template["strum_patterns"][random.choice(keys)]))
        self.instrument=""
        print(self.bars)
    @threaded
    def tick(self, global_bar):
        if DEBUG: print("music sync from "+str(self))
        bar = self.bars[global_bar%len(self.bars)]
        position = 1
        for i in bar:
            if type(i) == int:
                asdr=self.default_asdr
                temppos=position+1
                while bar[temppos]=="tie":
                    self.default_asdr["sustain"]+=1
                    temppos+=1
                play(i,**asdr)
            elif type(i) == samples.Sample:
                sample(i)
            time.sleep(bar_length/len(bar))
            position +=1
        



blue_button = Button("GPIO21")
black_button = Button("GPIO16")
red_button = Button("GPIO20")

def shuffle_most_recent():
    if len(tracklist)>0:
        tracklist[len(tracklist)-1].shuffle()

def delete_most_recent():
    if len(tracklist)>0:
        to_go=tracklist.pop(len(tracklist)-1)
        if DEBUG: print("deleting "+str(to_go))
        del to_go

def add_new_track():
    tracklist.append(Track())

blue_button.when_pressed = add_new_track
red_button.when_pressed = delete_most_recent
black_button.when_pressed = shuffle_most_recent


bar = 1
while True:
    for track in tracklist:
        track.tick(bar)
    time.sleep(bar_length)
    bar +=1