from psonic import *
from threading import Thread
set_server_parameter('127.0.0.1',4557,4559)


#tick = Message()

bpm = 140

def in_thread(func):
    def wrapper(*args,**kwargs):
        print(type(kwargs))
        _thread = threading.Thread(target=func,args=args)
        key_args={}
        for key in kwargs:
            key_args[key]=kwargs[key]
        _thread._kwargs=key_args
        _thread.start()

    return wrapper

@in_thread
def psn(pitch, **kwargs): #play a single note
    nkwargs={}
    print(type(kwargs))
    if 'synth' in kwargs.keys():
        use_synth(kwargs['synth'])
    if 'repeat' not in kwargs.keys():
        kwargs['repeat']=1
        kwargs['sleep']=0
    if 'pattern' not in kwargs.keys():
        kwargs['pattern']="////"
    for key in kwargs:
        if key != 'synth' and key != 'sleep' and key != 'repeat' and key != 'pattern':
            nkwargs[key] = kwargs[key]
    for i in range(kwargs['repeat']):
        for determine in kwargs['pattern']:
            if determine == "/":
                play(pitch,**nkwargs)
            sleep(kwargs['sleep']/(len(kwargs['pattern'])/4))

def arpeggiate(notes, pattern, **kwargs):
    note_num = 0
    for determine in pattern:
        if determine == "/":
            note_num+=1
            psn(notes[note_num%len(notes)])

def str_to_array(input_str):
    val = []
    for i in range(len(input_str)):
        print(i)
        val.append(input_str[i])
        
strum = "/ / /   // / // "


#mainloop()
psn(70)
sleep(2)
psn(70,synth=PROPHET)
mychord=chord(E3,MAJOR7)
psn(mychord,synth=PLUCK,repeat=4,sleep=1,pattern=strum)
arpeggiate(mychord, "/ / / / / / / /")
while True:
    pass