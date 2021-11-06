from gpiozero import Button
import time
from psonic import *
from threading import Thread
from json import load as json_load
from numpy import random
import numpy
from musthe import *

#All of these are standard imports apart from musthe (allows musical theory in python),
#psonic (allows playing notes through SonicPi / Supercollider) and gpiozero (allows interfacing
#with the Raspberry Pi's GPIO ports.



globvars = {
    #ALLCAPS entries below can be edited to change the feel of the track.
    #These should potentially be moved into a config file.
    "BEATS_PER_MINUTE":140,
    "KEY_SIGNATURE":Note('C'),
    "KEY_TONALITY":MAJOR
    "TIME_SIGNATURE_TOP":4,
    "TIME_SIGNATURE_TOP":4,
    "DEBUG":False #Change to True to enable command line output.
    "CHORD_SEQUENCE_LENGTH":8 #Defines how many chords are in the basic chord sequence.
    "coin":[True,False]
    }

globals().update(globvars)


#These are the global variables that I want referencable at all times.




with open("templates.json") as file:
    templates = json_load(file)
    file.close()

#Imports instrument-patternn combination data.


#with open("instruments.json") as file:
#    instruments = json_load(file)
#    file.close()



if DEBUG: print(templates)

beat_length = 60/140
bar_length = beat_length * TIME_SIGNATURE_TOP
#Calculating how long beats and bars are.


tracklist = []


def threaded(fn):
    def wrapper(*args, **kwargs):
        Thread(target=fn, args=args, kwargs=kwargs).start()
    return wrapper
#Means anything marked @in_thread will run in its own thread, ie multiple threaded functions can
#run at the same time.


@in_thread
def delete_thread(to_go):
    if DEBUG: print("deleting "+str(to_go))
    time.sleep(bar_length)
    del to_go
#This function just stops Track threads being deleted while they are still playing.


class Track:
    def __init__(self):
        global DEBUG
        global templates
        if DEBUG: print("new Track object created")
        self.instrument=""
        self.template=templates[str(random.randint(1,len(templates.keys())))]
        #Putting some initialisation in the shuffle() function allows me to let each track keep
        #its template even after being shuffled, eg a piano track won't shuffle into a drum track.
        
        self.shuffle()
    def shuffle(self):
        self.bars=[]
        self.role = template["role"]
        #Each track has a role, which defines how some data should be interpreted.
        self.default_asdr={
            "attack":0.1,
            "decay":0,
            "sustain_level":1,
            "sustain":0.5,
            "release":0.4
            }
        #This default ASDR envelope should be stored in the JSON file.
        #ASDR stands for "attack", "decay", "sustain", "release" and defines how long each
        #note should be played for, and how.
        if DEBUG: print(str(self)+" is being shuffled")
        if DEBUG: print(self.template)
        for bar in range(int(self.template["bars"])):
            self.bars.append(self.new_bar(random.choice(self.template["strum_patterns"])))
        self.instrument=""
        "Remember to implement instrument, or merge it into role."
        #Each track's instrument is like a role, but more specific, and defines which synths
        #can be used.
        if DEBUG: print(self.bars)
    def new_bar(self, strum_pattern):
        bar=[]
        if DEBUG: print(strum_pattern)
        if self.role == "melody":
            tie = False
            for i in strum_pattern:
                if i == "1":
                    bar.append(self.get_note())
                elif i == "2":
                    pass
                elif i== "3":
                    if random.choice(coin):
                        bar.append(self.get_note())
                    else:
                        bar.append("tie")
                elif i == "4":
                    if random.choice(coin):
                        bar.append("tie")
                    else:
                        bar.append(None)
                else:
                    bar.append(None)
        return bar
    def get_note(self):
        note = int()
            
        
        return note
    
    
    
    @threaded
    def tick(self, global_bar):
        #This function makes a track play its current bar.
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
                    #If the next note is a tie, the current note needs to be lengthened.
                    #It may be more efficient to place ties before the note, however.
                    asdr["release"]+=beat_length/(len(bar)/TIME_SIGNATURE_TOP)
                    temppos+=1
                play(i,**asdr)
            elif type(i) == samples.Sample:
                sample(i)
            time.sleep(sleeptime)
            position +=1
        


#Sets the GPIO pins which relate to the control panel. If you wish to execute this code on
#A computer without GPIO out, remove this.
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

#Sets the GPIO pins which relate to the control panel. If you wish to execute this code on
#A computer without GPIO out, remove this.
blue_button.when_pressed = add_new_track
red_button.when_pressed = delete_most_recent
black_button.when_pressed = shuffle_most_recent
brown_button.when_pressed = hello_world


chord_sequence=[]
chord_sequence.append(KEY_SIGNATURE(weighted_tonality()))

for i in range(2,CHORD_SEQUENCE_LENGTH):
    if (i==2 and random.choice(coin,weights=(1,2))) or (random.choice(coin,weights=(1,4))):
        chord_sequence.append(chord_sequence[i-1])
    else:
        chord_sequence.append(
bar = 1
while True:
    for track in tracklist:
        track.tick(bar)
    time.sleep(bar_length)
    bar +=1