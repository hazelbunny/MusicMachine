from gpiozero import Button
import time
from psonic import *
from threading import Thread
from json import load as json_load
from numpy import random
import numpy
from musthe import *



BEATS_PER_MINUTE=140
KEY_SIGNATURE=Note('C')
TIME_SIGNATURE_TOP=4
TIME_SIGNATURE_TOP=4

globals().update({"DEBUG":False})



with open("templates.json") as file:
    templates = json_load(file)
    file.close()
    
#with open("instruments.json") as file:
#    instruments = json_load(file)
#    file.close()



if DEBUG: print(templates)

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

@in_thread
def delete_thread(to_go):
    if DEBUG: print("deleting "+str(to_go))
    time.sleep(bar_length)
    del to_go

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
            "attack":0.1,
            "decay":0,
            "sustain_level":1,
            "sustain":0.5,
            "release":0.4
            }
        if DEBUG: print(str(self)+" is being shuffled")
        print(self.template)
        for bar in range(int(self.template["bars"])):
            self.bars.append(new_bar(self.template["role"],random.choice(self.template["strum_patterns"])))
        self.instrument=""
        print(self.bars)
    @threaded
    def tick(self, global_bar):
        if DEBUG: print("music sync from "+str(self))
        bar = self.bars[global_bar%len(self.bars)]
        position = 1
        sleeptime=bar_length/len(bar)
        for i in bar:
            if i == "tie":
                pass
            elif type(i) == numpy.int32:
                asdr=self.default_asdr.copy()
                temppos=position
                while temppos < len(bar) and bar[temppos]=="tie":
                    asdr["release"]+=beat_length/(len(bar)/TIME_SIGNATURE_TOP)
                    temppos+=1
                play(i,**asdr)
                print("note: "+str(i)+" with sustain: "+str(asdr["sustain"]))
            elif type(i) == samples.Sample:
                sample(i)
            time.sleep(sleeptime)
            position +=1
        



blue_button = Button("GPIO21")
black_button = Button("GPIO16")
red_button = Button("GPIO20")
brown_button = Button("GPIO26")

def shuffle_most_recent():
    if len(tracklist)>0:
        tracklist[len(tracklist)-1].shuffle()

def delete_most_recent():
    if len(tracklist)>0:
        delete_thread(tracklist.pop(len(tracklist)-1))

def add_new_track():
    tracklist.append(Track())

def hello_world():
    print("hello world")

blue_button.when_pressed = add_new_track
red_button.when_pressed = delete_most_recent
black_button.when_pressed = shuffle_most_recent
brown_button.when_pressed = hello_world


bar = 1
while True:
    for track in tracklist:
        track.tick(bar)
    time.sleep(bar_length)
    bar +=1