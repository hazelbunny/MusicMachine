from psonic import *
from threading import Thread
from json import load as json_load
from numpy import random
from musthe import *
from musiclib import *
from time import sleep
from gpiozero import Button
from DrumTrack import DrumTrack
from ChordsTrack import ChordsTrack
from MelodyClass import MelodyTrack
import time



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


beat_length = 60/140
bar_length = beat_length * TIME_SIGNATURE_TOP
#Calculating how long beats and bars are.
        
blue_button = Button("GPIO21")
black_button = Button("GPIO16")
red_button = Button("GPIO20")
brown_button = Button("GPIO26")

config = {}
def set_config(new_config):
    config.update(new_config)

def shuffle_most_recent():
    if len(tracklist)>0:
        tracklist[len(tracklist)-1].initialized=False
        tracklist[len(tracklist)-1].shuffle()

def delete_most_recent():
    if len(tracklist)>0:
        delete_thread(tracklist.pop(len(tracklist)-1))

def add_new_track():
    drums = False
    chords = False
    for track in tracklist:
        if type(track) == DrumTrack:
            drums = True
        if type(track) == ChordsTrack:
            chords = True
    if drums == False:
        tracklist.append(DrumTrack([templates,globals()]))
    elif chords == False:
        tracklist.append(ChordsTrack([templates,globals()]))
    else:
        tracklist.append(MelodyTrack([templates,globals()]))
    if DEBUG: print("new track: "+str(tracklist[len(tracklist)-1])+"with bars: "+str(tracklist[len(tracklist)-1].bars))

def magic():
    print("hello world")
if GPIO_MODE:
    #Sets the GPIO pins which relate to the control panel. If you wish to execute this code on
    #A computer without GPIO out, remove this.
    blue_button.when_pressed = add_new_track
    red_button.when_pressed = delete_most_recent
    black_button.when_pressed = shuffle_most_recent
    brown_button.when_pressed = magic

       

chord_sequence=new_chord_sequence(KEY_SIGNATURE,KEY_TONALITY,CHORD_SEQUENCE_LENGTH)

tracklist = []

bar = 1
print(chord_sequence)
while True:
    if not GPIO_MODE: get_input()
    for track in tracklist:
        track.tick(bar)
    sleep(bar_length)
    bar +=1
