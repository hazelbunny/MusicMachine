from pythonosc import osc_message_builder
from pythonosc import udp_client
import time
from fractions import Fraction
from threading import Thread


sender = udp_client.SimpleUDPClient('127.0.0.1', 4559)

BEATS_PER_MINUTE=140
TIME_SIGNATURE=[4,4]


bps = 64*(BEATS_PER_MINUTE/60)/TIME_SIGNATURE[1]

#add instruments to list
loop1={}
for n in range(0,64):
    loop1[n]=[]
loop1[0].append(('/trigger/prophet', [70, 30, 8]))
#loop1[1/2].append(('/trigger/pluck', [80, 1, 8]))
#loop1[0].append(('/trigger/snare', [70, 1, 8]))
#loop1[1/4].append(('/trigger/snare', [70, 1, 8]))
loop1[32].append(('/trigger/snare', []))
loop1[16].append(('/trigger/snare', []))
loop1[18].append(('/trigger/snare', []))
loop1[24].append(('/trigger/snare', []))
loop1[48].append(('/trigger/snare', []))
loop1[0].append(('/trigger/snare', []))
#loop1[3/4].append(('/trigger/snare', [70, 1, 8]))
acceptable_times=[*loop1.keys()]
print(acceptable_times)


beat=0
def play(loop):
    global beat
    for segment in loop[beat%64]: #gets list of instrument commands for time position
        args=[]
        for message in segment: #gets all instruments from list
            args.append(message)
        sender.send_message(*args)
        print(args)

sender.send_message('/trigger/prophet', [70, 1, 8])

@in_thread
def mainloop():
    while True:
        play(loop1)
        global beat
        beat+=1
        time.sleep(1/bps)

mainloop()