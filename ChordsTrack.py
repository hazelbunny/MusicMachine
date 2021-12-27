from numpy import random
import musiclib
import TrackClass
from musthe import *
from psonic import *
from time import sleep

#test

class ChordsTrack(TrackClass.Track):
    
    
    def __init__(self,details):
        self.template = details[0]["chords"]
        self.config = details[1]
        
        self.chord_sequence =  self.config["chord_sequence"]
        self.bar_length = self.config["bar_length"]
        self.synth = Synth(musiclib.weighted_choice(self.template["synths"]))
        #print(self.synth.name)
        self.num_of_bars = self.config["CHORD_SEQUENCE_LENGTH"]
        
        self.bars = []
        
        self.shuffle()
    def shuffle(self):
        for i in range(0,self.num_of_bars-1):
            bar=[]
            working_bar=musiclib.return_pattern(self.template["patterns"])["pattern"]
            for chord in working_bar:
                if "type" in chord:
                    if chord["type"] == "chord":
                        asdr,modifiers,chance={},{},100
                        if "asdr" in chord:
                            asdr = chord["asdr"]
                            if "amp" in asdr:
                                asdr["amp"]*=0.7
                            else:
                                asdr["amp"]=0.5
                        if "modifiers" in chord:
                            modifiers = chord["modifiers"]
                        if "chance" in chord:
                            chance = chord["chance"]
                        bar.append({"asdr":asdr,"modifiers":modifiers,"chance":chance})
                    else:
                        bar.append(None)
                else:
                    bar.append(None)
            self.bars.append(bar)
    
    
    @musiclib.threaded
    def tick(self, global_bar):
        current_bar = (global_bar%self.num_of_bars)-1
        bar_notes = self.chord_sequence[(global_bar%len(self.chord_sequence))-1].notes
        sleeptime = self.bar_length/len(self.bars[current_bar])
        chord_list = self.bars[current_bar]
        for chord in chord_list:
            if chord !=None:
                if musiclib.pc(chord["chance"]):
                    #print(str(self.chord_sequence[(global_bar%len(self.chord_sequence))-1]))
                    for note in bar_notes:
                        synth(self.synth,note.number,**chord["asdr"])
                    for modifier in chord["modifiers"]:
                        if musiclib.pc(chord["modifiers"][modifier]):
                            synth(self.synth,note=(bar_notes[0]+Interval(modifier)).number, **chord["asdr"])
                            break
            sleep(sleeptime)
            
        
