from matplotlib import pyplot as plt
import sys
from PIL import Image




play_img = Image.open("/home/pi/MusicMachine/assets/play.png")
pause_img =Image.open("/home/pi/MusicMachine/assets/pause.jpg")
exit_img =Image.open("/home/pi/MusicMachine/assets/exit.png")
add_button = Image.open("/home/pi/MusicMachine/assets/add.jpg")
blank_img = Image.open("/home/pi/MusicMachine/assets/blank.png")



class Track():
    def __init__(self,**kwargs):
        global play_img
        global pause_img
        global exit_img
        global tracklist
        self.play_img = play_img
        self.pause_img = pause_img
        self.exit_img = exit_img
        self.current_img = self.play_img
        self.exitable = True
        if "exitable" in kwargs:
            self.exitable = False
        self.index = str(len(tracklist))
    def play():
        self.current_image = self.play_img
    def pause():
        self.current_image = self.pause_img
class AddButton():
    def __init__(self):
        global add_button
        self.current_img = add_button
        self.exitable=False
        self.index = "0"

def get_right_click_path():
    global right_click_path
    global right_click_index
    right_click_path=write_path.replace(".", "-"+str(right_click_index)+".")
    right_click_index += 1
    return right_click_path

def on_press(event):
    print("click "+str(event.button))


def on_pick(event):
    line = event.artist
    data = line.get_url()    
    tracklist.append(Track())
    print(tracklist)
    redraw()

def redraw():
    plt.clf()
    print("redrawing images from tracklist: "+str(tracklist))
    for track in tracklist:
        
        plt.imshow(track.current_img, picker = True, url=track.index+"m")
        plt.axis('off')
        
        if track.exitable:        
            plt.imshow(track.exit_img, picker=True, url=track.index+"e")
        else:
            plt.imshow(blank_img, picker=False)
        plt.axis('off')
    plt.draw()
def on_key(event):
    print('press', event.key)
    sys.stdout.flush()

        
        
fig = plt.figure(figsize=(10, 7))
kp = fig.canvas.mpl_connect('button_press_event', on_press)
cid = fig.canvas.mpl_connect('pick_event', on_pick)

refresh = fig.canvas.mpl_connect('key_press_event', on_key)
tracklist = [AddButton()]
tracklist.append(Track(exitable=False))
redraw()
plt.show()