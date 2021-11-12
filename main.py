from psonic import *
from threading import Thread
from json import load as json_load
from numpy import random
from musthe import *
from musiclib import *
import gpiohelper
from time import sleep




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
    new_track(templates,tracklist,config["CHORD_SEQUENCE_LENGTH"])
    if config["DEBUG"]: print("new track: "+str(tracklist[len(tracklist)-1])+"with bars: "+str(tracklist[len(tracklist)-1].bars))

def magic():
    print("hello world")
if GPIO_MODE:
    #Sets the GPIO pins which relate to the control panel. If you wish to execute this code on
    #A computer without GPIO out, remove this.
    gpiohelper.blue_button.when_pressed = gpiohelper.add_new_track
    gpiohelper.red_button.when_pressed = gpiohelper.delete_most_recent
    gpiohelper.black_button.when_pressed = gpiohelper.shuffle_most_recent
    gpiohelper.brown_button.when_pressed = gpiohelper.magic


chord_sequence=new_chord_sequence(KEY_SIGNATURE,KEY_TONALITY,CHORD_SEQUENCE_LENGTH)

tracklist = []
gpiohelper.tracklist = tracklist
gpiohelper.set_config(config)
gpiohelper.templates = templates

bar = 1
print(chord_sequence)
while True:
    if not GPIO_MODE: get_input()
    for track in tracklist:
        track.tick(bar)
    sleep(bar_length)
    bar +=1
