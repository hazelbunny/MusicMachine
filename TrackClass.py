import time
from psonic import *
from threading import Thread
from json import load as json_load
from numpy import random
import numpy
from musthe import *
from musiclib import threaded
from musiclib import *

class Track:
    def __init__(self,template,**kwargs):
        if "DEBUG" in kwargs:
            self.debug=kwargs["DEBUG"]
        else:
            self.debug = False
        self.initialized=False
        self.template = template
        self.synth=random.choice(synthlist[self.template["role"]])
        self.role = self.template["role"]
        #Putting some initialisation in the shuffle() function allows me to let each track keep
        #its template even after being shuffled, eg a piano track won't shuffle into a drum track.
        
        self.shuffle()
    def shuffle(self):
        return
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
        if self.debug: print(str(self)+" is being shuffled")
        if self.debug: print(self.template)
        for cur_bar in range(self.template["bars"]):
            self.cur_bar = cur_bar
            self.bars.append(self.new_bar(random.choice(self.template["strum_patterns"])))
        if DEBUG: print(self.bars)
        self.initialized=True
    def get_note(self):
        if self.role == "melody":
            _note = random.choice(Scale(KEY_SIGNATURE,KEY_TONALITY).notes)
            return Note(str(_note)+str(random.choice(self.template["octaves"]))).number
        else:
            return random.choice(chord_sequence[self.cur_bar%len(chord_sequence)].notes).number
    
    def update_config(glob_vars):
        self.config = glob_vars
    
    @threaded
    def tick(self, global_bar):
        #This function makes a track play its current bar.
        raise Exception("This thread has no assigned tick behaviour.")
        if self.debug: print("music sync from "+str(self))
        bar = self.bars[global_bar%len(self.bars)]
        position = 1
        sleeptime=bar_length/len(bar)
        
        
        
        
        
        
        """
        for i in bar:
            if str(i) == "tie":
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
            elif str(i) == "chord":
                asdr = self.default_asdr
                asdr["release"]=2
                for note in chord_sequence[global_bar%len(chord_sequence)].notes:
                    play(note.number, **asdr)
                
            time.sleep(sleeptime)
            position +=1
            
            """
    def set_values(self,**kwargs):
        if "synth" in kwargs:
            self.synth=kwargs["synth"]
        if "role" in kwargs:
            self.role=kwargs["role"]