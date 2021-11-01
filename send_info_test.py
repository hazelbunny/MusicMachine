from pythonosc import osc_message_builder
from pythonosc import udp_client
import time
from fractions import Fraction

sender = udp_client.SimpleUDPClient('127.0.0.1', 4559)

BEATS_PER_MINUTE=120



bps = BEATS_PER_MINUTE/60

#add instruments to list
loop1={}
for n in range(0,32):
    for d in range(6):
        if 2**d>n:
            loop1[n/2**d]=[]
loop1[0].append(('/trigger/prophet', [70, 2, 8]))
#loop1[1/2].append(('/trigger/pluck', [80, 1, 8]))
#loop1[0].append(('/trigger/snare', [70, 1, 8]))
#loop1[1/4].append(('/trigger/snare', [70, 1, 8]))
#loop1[1/2].append(('/trigger/snare', [70, 1, 8]))
#loop1[3/4].append(('/trigger/snare', [70, 1, 8]))
acceptable_times=[*loop1.keys()]
print(acceptable_times)



def play(loop):
    go_ahead,position=get_time()
    if go_ahead:
        print("vetted: "+str(position))
        for segment in loop1[position]: #gets list of instrument commands for time position
            args=[]
            for message in segment: #gets all instruments from list
                args.append(message)
            sender.send_message(*args)
    time.sleep(0.000005)

def get_time():
    datetime = time.time()
    dts=str(datetime)
    decimal_place=dts.index(".")
    seconds = float(dts[len(dts)-10:len(dts)-8])
    decimals = float("0."+dts[decimal_place+1:len(dts)])
    if decimals in acceptable_times:
        nowbeat = decimals/bps
        position=round(nowbeat,5)
        print(position)
        return position in acceptable_times,position
    else:
        return False,0
     
    
    
while True:
    play(loop1)