from matplotlib import pyplot as plt
import sys
from PIL import Image
import threading
import numpy as np


current_button=None


play_img = Image.open("/home/pi/MusicMachine/assets/play.png")
pause_img = np.array(Image.open("/home/pi/MusicMachine/assets/pause.jpg"))
exit_img = Image.open("/home/pi/MusicMachine/assets/exit.png")
add_button = np.array(Image.open("/home/pi/MusicMachine/assets/add.jpg"))
blank_img = np.zeros([100,100,3],dtype=np.uint8)
blank_img.fill(255)

shuffle_image = blank_img


KEY = "A"
BPS = 140


class Track():
    def __init__(self,**kwargs): #sets basic values for the track
        global play_img
        global pause_img
        global exit_img
        global tracklist
        global blank_img
        global shuffle_image
        self.play_img = play_img
        self.pause_img = pause_img
        self.exit_img = exit_img
        self.current_img = self.play_img
        self.exitable = True
        if "exitable" in kwargs:
            self.exitable = False
        self.index = str(len(tracklist))
        self.playing = True
        self.instrument_img = blank_img #to be done, potentially
        self.shuffle_img = shuffle_image
    def toggle(self):
        if self.playing:
            self.pause()
        else:
            self.play()
    def play(self):
        self.current_img = self.play_img
        self.playing = True
    def pause(self):
        self.current_img = self.pause_img
        self.playing = False

class AddButton(): #a blank track with no values
    def __init__(self):
        global add_button
        global blank_img
        self.current_img = add_button
        self.exitable=False
        self.index = "0a"
        self.blank_img = blank_img
    def toggle(self):
        tracklist.append(Track())
        #print(tracklist)
        redraw()


def on_press(event):
    sys.stdout.flush()


def on_pick(event):
    line = event.artist
    data = line.get_url()
    if data:
        selected = tracklist[int(data[0])]
        if data[1] == "e":
            plt.clf()
            to_go = tracklist[int(data[0])]
            tracklist.remove(to_go)
            del to_go
            redraw()
        elif data[1] == "m":
            tracklist[int(data[0])].toggle()
            redraw()
        elif data[1] == "k":
            print("key change")
        elif data[1] == "t":
            print("time signature change")
        elif data[1] == "s":
            print("shuffle track values")
        elif data[1] == "i":
            print("instrument selected")
    sys.stdout.flush()

def redraw():
    rows = len(tracklist)
    i=0
    columns = 4
    plt.clf()
    for track in tracklist:
        track.index=str(i)
        fig.add_subplot(rows, columns, columns*i+1)
        plt.imshow(track.current_img, picker = True, url=track.index+"m")
        plt.axis('off')
        if i==0:
            fig.add_subplot(rows, columns, columns*i+2)
            plt.imshow(track.blank_img, picker = True, url=track.index+"k")
            plt.axis('off')
            fig.add_subplot(rows, columns, columns*i+3)
            plt.imshow(track.blank_img, picker = True, url=track.index+"t")
        else:
            fig.add_subplot(rows, columns, columns*i+2)
            plt.imshow(track.shuffle_img, picker = True, url=track.index+"s")
            plt.axis('off')
            fig.add_subplot(rows, columns, columns*i+3)
            plt.imshow(track.instrument_img, picker = True, url=track.index+"i")
        plt.axis('off')
        fig.add_subplot(rows, columns, columns*i+4)
        if track.exitable:
            plt.imshow(track.exit_img, picker=True, url=track.index+"e")
        else:
            plt.imshow(blank_img, picker=True, url=None)
        plt.axis('off')
        i+=1
    plt.draw()
def on_key(event):
    sys.stdout.flush()

        
        
fig = plt.figure(figsize=(14, 10))

kp = fig.canvas.mpl_connect('button_press_event', on_press)
cid = fig.canvas.mpl_connect('pick_event', on_pick)
refresh = fig.canvas.mpl_connect('key_press_event', on_key)

tracklist = [AddButton()]
tracklist.append(Track(exitable=False))
redraw()
plt.show()