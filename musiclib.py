from os import path
import json
import random
import musthe
from time import sleep

major_modifiers = {
    'maj':    120,
    'aug':    20,
    'dom7':   40,
    'maj7':   40,
    'aug7':   20
    }
minor_modifiers = {
    'min':    70,
    'min7':   50,
    }
modifiers = {
    'dim':    10,
    'dim7':   2,
    'm7dim5': 1,
    'open5':  10
    }

modifiers.update(major_modifiers)
modifiers.update(minor_modifiers)
modifier_list = []
mod_weights = []
for key in modifiers:
    modifier_list.append(key)
    mod_weights.append(modifiers[key])

minor_modifiers_list = []
minor_modifiers_weights = []
for key in minor_modifiers:
    minor_modifiers_list.append(key)
    minor_modifiers_weights.append(minor_modifiers[key])

major_modifiers_list = []
major_modifiers_weights = []
for key in major_modifiers:
    major_modifiers_list.append(key)
    major_modifiers_weights.append(major_modifiers[key])

default_config = {
    "BEATS_PER_MINUTE":140,
    "KEY_SIGNATURE":"C",
    "KEY_TONALITY":'major',
    "TIME_SIGNATURE_TOP":4,
    "TIME_SIGNATURE_TOP":4,
    "DEBUG":False,
    "CHORD_SEQUENCE_LENGTH":8,
    "GPIO_MODE":False
    }

def write_config(file):
    global default_config
    json.dump(default_config, file)
    return default_config

def get_config():
    global default_config
    try:
        with open("config.json") as file:
            config = json.load(file)
        file.close()
    except FileNotFoundError:
        with open("config.json","x") as file:
            config = write_config(file)
        file.close()
    except json.decoder.JSONDecodeError:
        with open("config.json","w") as file:
            config = write_config(file)
        file.close()
    for key in default_config.keys():
        if not key in config.keys():
            with open("config.json","w") as file:
                config = write_config(file)
            file.close()
            break
    return config

def pc(num):
    return random.choices([True,False],weights=(num,100-num),k=1)[0]


from threading import Thread

def threaded(fn):
    def wrapper(*args, **kwargs):
        Thread(target=fn, args=args, kwargs=kwargs).start()
    return wrapper
#Means anything marked @threaded will run in its own thread, ie multiple threaded functions can
#run at the same time.


@threaded
def delete_thread(to_go):
    sleep(8)
    del to_go
#This function just stops Track threads being deleted while they are still playing.

@threaded
def get_input():
    str_in = input().lower()
    if str_in in ["+","add","blue","b","a","plus","p"]:
        add_new_track()
    elif str_in in ["-","delete","del","red","r"]:
        delete_most_recent()
    elif str_in in ["shuffle","s","black"]:
        shuffle_most_recent()
    elif str_in in ["magic","m","brown"]:
        magic()

def new_chord_sequence(KEY_SIGNATURE,KEY_TONALITY,CHORD_SEQUENCE_LENGTH):
    chord_sequence = []
    chord_sequence.append(make_chord(KEY_SIGNATURE,KEY_TONALITY))
    for i in range(1,CHORD_SEQUENCE_LENGTH):
        if (i==2 and pc(50)):
            chord_sequence.append(chord_sequence[i-1])
        else:
            chord_sequence.append(chord_from_key(KEY_SIGNATURE, KEY_TONALITY))
    return chord_sequence


def chord_from_key(key, tonality):
    modifiers = str()
    scale = musthe.Scale(key,tonality)
    if pc(24):
        root = random.choice(scale)
        modifier = random.choices(modifier_list,mod_weights,k=1)[0]
        return musthe.Chord(root,modifier)
    else:
        root = random.choice(scale)
        degree = scale.notes.index(musthe.Note(str(root)+"0"))
        if tonality == "major":
            modifier = ['maj','min','min','maj','maj','min','dim'][degree]
        elif tonality == "minor":
            modifier = ['min','dim','maj','min','min','maj','maj'][degree]
        if modifier == 'major':
            modifier = random.choices(major_modifiers_list,major_modifiers_weights,k=1)[0]
        elif modifier == "minor":
            modifier = random.choices(minor_modifiers_list,minor_modifiers_weights,k=1)[0]
        return musthe.Chord(root,modifier)


def make_chord(key, tonality):
    chord_name = str()
    chord_name+=str(key)
    if tonality == "major":
        chord_name+="M"
    elif tonality == "minor":
        chord_name+="m"
    return musthe.Chord(chord_name)

def weighted_choice(dictionary,**kwargs):
    key_list = []
    weights = []
    for key in dictionary:
        key_list.append(key)
        weights.append(dictionary[key]["weight"])
    r =  random.choices(key_list,weights,k=1)[0]
    if "sample" in kwargs and kwargs["sample"] == True:
        if "duration" in dictionary[r]:
            return r, dictionary[r]["duration"]
        else:
            return r, 1
    else:
        return r
def return_pattern(pattern_dict):
    pattern_list = []
    weights = []
    for pattern in pattern_dict:
        pattern_list.append(pattern)
        weights.append(pattern["weight"])
    r =  random.choices(pattern_list,weights,k=1)[0]
    return r
