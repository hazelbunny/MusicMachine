from os import path
import json
import random
import musthe

modifiers = {
    'maj':    100,
    'min':    120,
    'aug':    20,
    'dim':    10,
    'dom7':   40,
    'min7':   50,
    'maj7':   40,
    'aug7':   20,
    'dim7':   2,
    'm7dim5': 1,
    'sus2':   10,
    'sus4':   10,
    'open5':  10
    }
modifier_list = []
mod_weights = []
for key in modifiers:
    modifier_list.append(key)
    mod_weights.append(modifiers[key])

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
#Means anything marked @in_thread will run in its own thread, ie multiple threaded functions can
#run at the same time.


@threaded
def delete_thread(to_go):
    time.sleep(bar_length)
    del to_go
#This function just stops Track threads being deleted while they are still playing.

@threaded
def get_input():
    str_in = input().lower()
    if str_in in ["+","add","blue","b","a"]:
        add_new_track()
    elif str_in in ["-","delete","del","red","r"]:
        delete_most_recent()
    elif str_in in ["shuffle","s","black"]:
        shuffle_most_recent()
    elif str_in in ["magic","m","brown"]:
        magic()
        



def chord_from_key(key, tonality):
    modifiers = str()
    if pc(7):
        root = random.choice(musthe.Scale(key,tonality))
        modifier = random.choices(modifier_list,mod_weights,k=1)[0]
        return musthe.Chord(root,modifier)
    else:
        root = random.choice(musthe.Scale(key,tonality))
        return musthe.Chord(root,"maj")


def make_chord(key, tonality):
    chord_name = str()
    chord_name+=str(key)
    if tonality == "major":
        chord_name+="M"
    elif tonality == "minor":
        chord_name+="m"
    return musthe.Chord(chord_name)