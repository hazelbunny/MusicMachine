from numpy import random
import musiclib
import TrackClass
from musthe import *
from psonic import *
from time import sleep

class DrumTrack(TrackClass.Track):
    
    
    def __init__(self,details):
        self.template = details[0]["drums"]
        self.config = details[1]
        
        self.bar_length = self.config["bar_length"]
        self.kick_sample = Sample(*musiclib.weighted_choice(self.template["kick_samples"],sample=True))
        self.open_hat_sample = Sample(*musiclib.weighted_choice(self.template["open_hat_samples"],sample=True))
        self.closed_hat_sample = Sample(*musiclib.weighted_choice(self.template["closed_hat_samples"],sample=True))
        self.clap_sample = Sample(*musiclib.weighted_choice(self.template["clap_samples"],sample=True))
        self.snare_sample = Sample(*musiclib.weighted_choice(self.template["snare_samples"],sample=True))
        
        self.num_of_bars = self.config["CHORD_SEQUENCE_LENGTH"]
        
        self.bars = []
        
        self.shuffle()
    def shuffle(self):
        for i in range(0,self.num_of_bars-1):
            bar=[]
            working_bar=musiclib.return_pattern(self.template["patterns"])["pattern"]
            for beat in working_bar:
                beat_array = []
                for key in beat:
                    if key == "kick":
                        beat_array.append({self.kick_sample:beat[key]})
                    elif key == "clap":
                        beat_array.append({self.clap_sample:beat[key]})
                    elif key == "snare":
                        beat_array.append({self.snare_sample:beat[key]})
                    elif key == "hat_open":
                        beat_array.append({self.open_hat_sample:beat[key]})
                    elif key == "hat_closed":
                        beat_array.append({self.closed_hat_sample:beat[key]})
                bar.append(beat_array)
            self.bars.append(bar)
    
    
    @musiclib.threaded
    def tick(self, global_bar):
        current_bar = (global_bar%self.num_of_bars)-1
        sleeptime = self.bar_length/len(self.bars[current_bar])
        for beat in self.bars[current_bar]:
            for note in beat:
                if musiclib.pc(list(note.values())[0]):
                    print(list(note.keys())[0].name+" playing for "+str(sleeptime))
                    sample(list(note.keys())[0])
            sleep(sleeptime)
            
        