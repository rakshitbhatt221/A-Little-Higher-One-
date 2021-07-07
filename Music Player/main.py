import os
import threading
import time
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import themed_tk as tk
from mutagen.mp3 import MP3
from pygame import mixer
root = tk.ThemedTk()

root.get_themes()
root.set_theme("radiance")

# Fonts - Arial (corresponds to Helvetica), Courier New (Courier), Comic Sans MS, Fixedsys,
# MS Sans Serif, MS Serif, Symbol, System, Times New Roman (Times), and Verdana
# Styles - normal, bold, roman, italic, underline, and overstrike.

statusbar = ttk.Label(root, text="Welcome to MusicBee", relief=SUNKEN, anchor=W, font='Times 10 italic')
statusbar.pack(side=BOTTOM, fill=X)
menubar = Menu(root)
root.config(menu=menubar)
subMenu = Menu(menubar, tearoff=0)

playlist = []

def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)
    mixer.music.queue(filename_path)

def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1

menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=browse_file)
subMenu.add_command(label="Exit", command=root.destroy)

def about_us():
    tkinter.messagebox.showinfo('MusicBee',"""Simpy Music player Developed by Scrapper221. Feel free to contact me through abc@gmail.com. v(1.0)""")

subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)
mixer.init()  # initializing the mixer
root.title("MusicBee")

#a logo can be added but I have left it :)
#root.iconbitmap(r'images/image_name.ico')

leftframe = Frame(root)
leftframe.pack(side=LEFT, padx=30, pady=30)
playlistbox = Listbox(leftframe)
playlistbox.pack()
addBtn = ttk.Button(leftframe, text="+ Add", command=browse_file)
addBtn.pack(side=LEFT)

def del_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)

delBtn = ttk.Button(leftframe, text="- Del", command=del_song)
delBtn.pack(side=LEFT)

rightframe = Frame(root)
rightframe.pack(pady=30)

topframe = Frame(rightframe)
topframe.pack()

lengthlabel = ttk.Label(topframe, text='Total Length : --:--')
lengthlabel.pack(pady=5)

currenttimelabel = ttk.Label(topframe, text='Current Time : --:--', relief=GROOVE)
currenttimelabel.pack()

def show_details(play_song):
    file_data = os.path.splitext(play_song)
    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "Total Length" + ' - ' + timeformat
    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()

def start_count(t):
    global paused
    
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = "Current Time" + ' - ' + timeformat
            time.sleep(1)
            current_time += 1

def play_music():
    global paused
    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File not found', 'MusicBee could not find the file. Please check again.')

def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"
paused = FALSE

def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused"

def rewind_music():
    play_music()
    statusbar['text'] = "Music Rewinded"

def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)

muted = FALSE

def mute_music():
    global muted
    if muted:  # Unmute the music
        mixer.music.set_volume(0.7)
        volumeBtn.configure(image='')           #need an image here
        scale.set(70)
        muted = FALSE
    else:  # mute the music
        mixer.music.set_volume(0)
        volumeBtn.configure(image='')           #need an image here
        scale.set(0)
        muted = TRUE

middleframe = Frame(rightframe)
middleframe.pack(pady=30, padx=30)

#playPhoto = PhotoImage(file='images/play.png')
playBtn = ttk.Button(middleframe ,    text='Play Button',             command=play_music)       #need an image here
playBtn.grid(row=0, column=0, padx=10)

#stopPhoto = PhotoImage(file='images/stop.png')

stopBtn = ttk.Button(middleframe,     text='Stop Button',             command=stop_music)       #need an image here
stopBtn.grid(row=0, column=1, padx=10)

#pausePhoto = PhotoImage(file='images/pause.png')

pauseBtn = ttk.Button(middleframe,      text='Pause Button',           command=pause_music)      #need an image here
pauseBtn.grid(row=0, column=2, padx=10)

bottomframe = Frame(rightframe)
bottomframe.pack()

#rewindPhoto = PhotoImage(file='images/rewind.png')
rewindBtn = ttk.Button(bottomframe,      text='Rewind Button',          command=rewind_music)      #need an image here
rewindBtn.grid(row=0, column=0)

#mutePhoto = PhotoImage(file='images/mute.png')
#volumePhoto = PhotoImage(file='images/volume.png')

volumeBtn = ttk.Button(bottomframe,    text='volume button',            command=mute_music)        #need an image here
volumeBtn.grid(row=0, column=1)

scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)  # implement the default value of scale when music player starts

mixer.music.set_volume(0.7)

scale.grid(row=0, column=2, pady=15, padx=30)

def on_closing():
    stop_music()
    root.destroy()
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
