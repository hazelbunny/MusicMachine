from gpiozero import Button
import time
from psonic import *
from threading import Thread
from json import load as json_load
from numpy import random
import numpy
from musthe import *
from musiclib import *

#All of these are standard imports apart from musthe (allows musical theory in python),
#psonic (allows playing notes through SonicPi / Supercollider) and gpiozero (allows interfacing
#with the Raspberry Pi's GPIO ports.
#musiclib is written by me, and just contains some less used functions to keep this file

config = get_config()
config["KEY_SIGNATURE"]=Note(config["KEY_SIGNATURE"])
globals().update(config)
#Gets the config file options. The get_config() function is from musiclib.
#They are then added to the global variables so that they are more easily referencable.




with open("templates.json") as file:
    templates = json_load(file)
    file.close()
#Imports instrument-patternn combination data.






if DEBUG: print(templates)

beat_length = 60/140
bar_length = beat_length * TIME_SIGNATURE_TOP
#Calculating how long beats and bars are.


tracklist = []

synthlist = {"melody":[BEEP,PROPHET,PIANO],"chords":[MOD_PULSE],"drums":[PRETTY_BELL]}

class Track:
    def __init__(self):
        self.initialized=False
        global DEBUG
        global templates
        if DEBUG: print("new Track object created")
        self.template=templates[str(random.randint(1,len(templates.keys())))]
        self.synth=random.choice(synthlist[self.template["role"]])
        self.role = self.template["role"]
        #Putting some initialisation in the shuffle() function allows me to let each track keep
        #its template even after being shuffled, eg a piano track won't shuffle into a drum track.
        
        self.shuffle()
    def shuffle(self):
        self.bars=[]
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
        for cur_bar in range(self.template["bars"]):
            self.cur_bar = cur_bar
            self.bars.append(self.new_bar(random.choice(self.template["strum_patterns"])))
        if DEBUG: print(self.bars)
        self.initialized=True
    def new_bar(self, strum_pattern):
        bar=[]
        if DEBUG: print(strum_pattern)
        if self.role == "melody":
            #melody strum patterns of form 0 = 100% rest
            #1 = 100% play, 2=100% tie, 3=50% tie, 50% play, 4=50% rest, 50% tie
            tie = False
            for i in strum_pattern:
                if i == "1":
                    bar.append(self.get_note())
                elif i == "2":
                    pass
                elif i== "3":
                    if pc(50):
                        bar.append(self.get_note())
                    else:
                        bar.append("tie")
                elif i == "4":
                    if pc(50):
                        bar.append("tie")
                    else:
                        bar.append(None)
                else:
                    bar.append(None)
        elif self.role == "chords":
            for i in strum_pattern:
                if i == "1":
                    bar.append(chord_sequence[self.cur_bar])
        elif self.role == "drums":
            for i in strum_pattern:
                if i == "1":
                    bar.append(AMBI_LUNAR_LAND)
        return bar
    def get_note(self):
        if self.role == "melody":
            _note = random.choice(Scale(KEY_SIGNATURE,KEY_TONALITY).notes)
            return Note(str(_note)+str(random.choice(self.template["octaves"]))).number
        else:
            return random.choice(chord_sequence[self.cur_bar%len(chord_sequence)].notes).number
    
    
    
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
            elif type(i) == numpy.int32 or type(i) == list or type(i) == int:
                asdr=self.default_asdr.copy()
                temppos=position
                while temppos < len(bar) and bar[temppos]=="tie":
                    #If the next note is a tie, the current note needs to be lengthened.
                    #It may be more efficient to place ties before the note, however.
                    asdr["release"]+=beat_length/(len(bar)/TIME_SIGNATURE_TOP)
                    temppos+=1
                use_synth(self.synth)
                if type(i) == numpy.int32 or type(i) == int: play(i,**asdr)
                elif type(i) == list:
                    for note in i:
                        play(note,**asdr)
            elif type(i) == samples.Sample:
                sample(i)
            elif i == "chord":
                for note in chord_sequence[bar%len(chord_sequence)]:
                    play(note, **asdr)
                
            time.sleep(sleeptime)
            position +=1
        


def shuffle_most_recent():
    if len(tracklist)>0:
        tracklist[len(tracklist)-1].initialized=False
        tracklist[len(tracklist)-1].shuffle()

def delete_most_recent():
    if len(tracklist)>0:
        delete_thread(tracklist.pop(len(tracklist)-1))

def add_new_track():
    tracklist.append(Track())
    print("new track: "+str(tracklist[len(tracklist)-1])+"with bars: "+str(tracklist[len(tracklist)-1].bars))

def magic():
    print("hello world")

if GPIO_MODE:
    #Sets the GPIO pins which relate to the control panel. If you wish to execute this code on
    #A computer without GPIO out, remove this.
    blue_button = Button("GPIO21")
    black_button = Button("GPIO16")
    red_button = Button("GPIO20")
    brown_button = Button("GPIO26")
    #Sets the GPIO pins which relate to the control panel. If you wish to execute this code on
    #A computer without GPIO out, remove this.
    blue_button.when_pressed = add_new_track
    red_button.when_pressed = delete_most_recent
    black_button.when_pressed = shuffle_most_recent
    brown_button.when_pressed = magic


chord_sequence=[]
chord_sequence.append(make_chord(KEY_SIGNATURE,KEY_TONALITY))

for i in range(1,CHORD_SEQUENCE_LENGTH):
#    if (i==2 and pc(50)) or pc(10):
#        chord_sequence.append(chord_sequence[i-1])
#    else:
    chord_sequence.append(chord_from_key(KEY_SIGNATURE, KEY_TONALITY))


bar = 1
print(chord_sequence)
while True:
    if not GPIO_MODE: get_input()
    for track in tracklist:
        track.tick(bar)
    time.sleep(bar_length)
    bar +=1