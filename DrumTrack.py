from numpy import random
import musiclib
import TrackClass
from musthe import *
from psonic import *

class DrumTrack(TrackClass.Track):
    
    
    def __init__(self, templates, num_of_bars):
        self.template = templates["drums"]
        
        
        self.kick_sample = Sample(*musiclib.weighted_choice(self.template["kick_samples"],sample=True))
        self.open_hat_sample = Sample(*musiclib.weighted_choice(self.template["open_hat_samples"],sample=True))
        self.closed_hat_sample = Sample(*musiclib.weighted_choice(self.template["closed_hat_samples"],sample=True))
        self.clap_sample = Sample(*musiclib.weighted_choice(self.template["clap_samples"],sample=True))
        self.snare_sample = Sample(*musiclib.weighted_choice(self.template["snare_samples"],sample=True))
        
        self.num_of_bars = num_of_bars
        
        self.bars = []
        
        self.shuffle()
    def shuffle(self):
        for i in range(0,self.num_of_bars-1):
            bar=[]
            working_bar=musiclib.return_pattern(self.template["patterns"])["pattern"]
            for note in working_bar:
                for key in note:
                    if key == "kick":
                        bar.append({self.kick_sample:note[key]})
                    elif key == "clap":
                        bar.append({self.clap_sample:note[key]})
                    elif key == "snare":
                        bar.append({self.snare_sample:note[key]})
                    elif key == "hat_open":
                        bar.append({self.open_hat_sample:note[key]})
                    elif key == "hat_closed":
                        bar.append({self.closed_hat_sample:note[key]})
                    else:
                        bar.append({Sample(key):note[key]})
            self.bars.append(bar)
    @musiclib.threaded
    def tick(self, global_bar):
        current_bar = (global_bar%self.num_of_bars)-1
        for note in self.bars[current_bar]:
            if musiclib.pc(list(note.values())[0]):
                sample(list(note.keys())[0])
            
        