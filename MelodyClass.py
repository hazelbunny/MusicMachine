from numpy import random
import musiclib
import TrackClass
from musthe import *
from psonic import *
from time import sleep

class MelodyTrack(TrackClass.Track):
    def __init__(self,details):
        self.template = details[0]["melody"]
        self.config = details[1]
        
        self.bar_length = self.config["bar_length"]
        self.synth = Synth(musiclib.weighted_choice(self.template["synths"]))
        #print(self.synth.name)
        self.num_of_bars = self.config["CHORD_SEQUENCE_LENGTH"]
        
        self.bars = []
        
        
        self.root = self.config["KEY_SIGNATURE"]
        self.tonality = self.config["KEY_TONALITY"]
        #Putting some initialisation in the shuffle() function allows me to let each track keep
        #its template even after being shuffled, eg a piano track won't shuffle into a drum track.
        
        self.shuffle()
    def shuffle(self):
        for i in range(0,self.num_of_bars-1):
            bar=[]
            working_bar=musiclib.return_pattern(self.template["patterns"])["pattern"]
            for note_template in working_bar:
                if "note" in note_template:
                    if note_template["note"] == "root":
                        cur_note = self.root
                    elif note_template["note"] == "random":
                        cur_note = self.get_note()
                    else:
                        cur_note = self.get_note()
                    asdr,modifiers,chance={},{},100
                    if "asdr" in note_template:
                        asdr = note_template["asdr"]
                    if "modifiers" in note_template:
                        modifiers = note_template["modifiers"]
                    if "chance" in note_template:
                        chance = note_template["chance"]
                    bar.append({"note":cur_note.number,"asdr":asdr,"modifiers":modifiers,"chance":chance})
            self.bars.append(bar)
    def get_note(self):
        _note = random.choice(Scale(self.root,self.tonality).notes)
        return Note(str(_note)+str(random.choice(self.template["octaves"])))
    
    def update_config(glob_vars):
        self.config = glob_vars
    
    @musiclib.threaded
    def tick(self, global_bar):
        #This function makes a track play its current bar.
        current_bar = (global_bar%self.num_of_bars)-1
        sleeptime = self.bar_length/len(self.bars[current_bar])
        bar = self.bars[current_bar]
        for beat in bar:
            if beat !=None:
                if musiclib.pc(beat["chance"]):
                    synth(self.synth,beat["note"],**beat["asdr"])
                    print(beat["note"])
            sleep(sleeptime)
            
            
    def set_values(self,**kwargs):
        if "synth" in kwargs:
            self.synth=kwargs["synth"]
        if "role" in kwargs:
            self.role=kwargs["role"]
