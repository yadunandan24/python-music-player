from tkinter import *
from pygame import mixer
from tkinter import messagebox,filedialog
from tkinter import ttk
from ttkthemes import themed_tk as tk
import os
from  mutagen.mp3 import MP3
import threading
import time

root=tk.ThemedTk()
root.get_themes()
root.set_theme("scidpurple")
#initializing mixer module
mixer.init()

#setting up our window
root.title("Music Player")
#root.geometry("500x300")
root.iconbitmap(r'music-player1.ico') #setting our main window icon

root.configure(background='misty rose')

#create status bar
statusbar=ttk.Label(root,text="WELCOME TO PLAYER",relief=RIDGE,anchor=E,font=('Times New Roman', '10', 'normal'),background='red')
statusbar.pack(side=BOTTOM,fill=X)

#creating a left frame
frameleft=Frame(root)
frameleft.pack(side=LEFT,padx=15,pady=25)
frameleft.configure(background='misty rose')
#creating a right frame
frameright=Frame(root)
frameright.pack(padx=20)
frameright.configure(background='misty rose')

statusframe=Frame(root)
statusframe.pack(side=BOTTOM)
#subframe of right frame
frameup=Frame(frameright,background='misty rose')
frameup.pack(pady=10)
#subframe of right frame
framemiddle=Frame(frameright)
framemiddle.pack(pady=10,padx=20)
framemiddle.configure(background='misty rose')
#subframe of right frame
framelower=Frame(frameright)
framelower.pack(pady=10,padx=20)
framelower.configure(background='misty rose')

#creating a label for disp total time
infolabel=ttk.Label(frameup,text='Duration:--:--',font=('arial', '8', 'bold'),relief=GROOVE,background='gray87',foreground='black')
infolabel.pack(pady=10)

#creating a label for remaing time
remaining_time=ttk.Label(frameup,text="Remaining Time:--:--",relief=GROOVE,font=('arial', '8', 'bold'),foreground='black',background='gray87')
remaining_time.pack(pady=10)

#section 1 creating menubar::
#creating a function for message box
def about():
   messagebox.showinfo("MUSIC PLAYER","Created by yadunandan sood-181297\nkartik gupta-181290")  

#creating a function for opening files using file menu->open
def opens():
    global selectfile
    selectfile=filedialog.askopenfilename()
    add_to_playlist(selectfile)#adding to playlist

#creating a function to add items to listbox
#called from inside open()    
def add_to_playlist(file):
    global plist
    file=os.path.basename(selectfile)
    index=0
    playlist.insert(index,file)
    plist.insert(index,selectfile)
    index=index+1
    
#creating a function that quits upon clicking exit
def quits():
   mixer.music.stop()
   root.destroy()

#creating a listbox for playlist
playlist=Listbox(frameleft,highlightcolor='red',relief=GROOVE)
playlist.pack(padx=25)

#a list to add elements to access full filenames and not os filename
plist=[]

#creating menubar
menubar=Menu(root)
root.config(menu=menubar)

#creating submenu1->file
submenu1=Menu(menubar,tearoff=0)
menubar.add_cascade(label="FILE",menu=submenu1)
submenu1.add_command(label='Open',command=opens)
submenu1.add_command(label='Exit',command=quits)

#creating submenu2->exit
submenu1=Menu(menubar,tearoff=0)
menubar.add_cascade(label="HELP",menu=submenu1)
submenu1.add_command(label='ABOUT',command=about)
            
def infor(cur_song):
    #for mp3 files
    name, ext = os.path.splitext(cur_song)
    if(ext=='.mp3'):
        audio = MP3(cur_song)
        length=round(audio.info.length)
    else:# for wav or other files
        z=mixer.Sound(cur_song)
        length=z.get_length()
    
    mins=round(length/60)
    secs=round(length%60)
    timing='{:02d}:{:02d}'.format(mins,secs)
    infolabel.configure(text='Duration:'+' '+timing)
   # global stopped
    #start of threadings
    x=threading.Thread(target=start_timer,args=(length,))
    x.start()
    
def start_timer(l):
    global pause
    global stopped
    length=l
   # w=mixer.music.get_busy()
    #print(w)
    while(length>0 and stopped==1):
        if(pause==1):
            continue
        else:
            mins,secs=divmod(length,60)
            mins=round(mins)
            secs=round(secs)
            timing='{:02d}:{:02d}'.format(mins,secs)
            remaining_time.configure(text='Remining Time:'+' '+timing)
            time.sleep(1)
            length=length-1
    
#section 2 creating music::
def play_song():
    '''a function for playing music'''
    global pause
    global stopped
    
    stopped=1
    if(pause==1):
        mixer.music.unpause()
        statusbar.configure(text="MUSIC UNPAUSED")
        pause=2
    
    else:
        try:    
            
            time.sleep(1)
            cur_song_index=playlist.curselection()
            cur_song_index=int(cur_song_index[0])
            cur_song=plist[cur_song_index]
            mixer.music.load(cur_song)
            mixer.music.play()
            statusbar.configure(text="MUSIC PLAYING:"+os.path.basename(cur_song))
            infor(cur_song)#for displaying length
        except:
            messagebox.showwarning("Warning","First select a file")
 
global stopped
stopped=1           
def stop_song():
    '''a function to stop music'''
    mixer.music.stop()
    statusbar.configure(text="MUSIC STOPPED!")
    global stopped
    stopped=2

def pause_song():
   ''' a function to pause music'''
   global pause
   pause=1
   mixer.music.pause()
   statusbar.configure(text="MUSIC PAUSED")
   
x=IntVar() #creating a vriable to store current value of scale

def volume(x):
    ''' a function to set volume'''
    val=((float(x))/100) #as set_value only takes value between 0 and 1
    mixer.music.set_volume(val)
    global v
    v=val

def rewind():
    play_song()
    statusbar.configure(text="MUSIC REWINDED")
   
def mute_song():
    '''a function to mute and unmute'''
    global mute
    if(mute==1):
        #mixer.music.set_volume(0)
        volume_control.set(0)
        mute=2
        mutebtn.configure(image=unmutepic)
    elif(mute==2):
        #mixer.music.set_volume(.3)
        volume_control.set(30)
        mutebtn.configure(image=mutepic)
        mute=1
                
#a function for deleting from playlist 
#last element has to be deleted first
def del_song():
     cur_song_index=playlist.curselection()
     cur_song_index=int(cur_song_index[0])
     playlist.delete(cur_song_index)
     plist.pop()
         
pausepic=PhotoImage(file='pause2.png') #import image of pause button
#create pause button
global pause
pause=2
pausebtn=ttk.Button(framemiddle,command=pause_song,image=pausepic)
pausebtn.grid(row=0,column=0,padx=10)

playpic=PhotoImage(file='play2.png') #import image of play button
#create play button
playbtn=ttk.Button(framemiddle,image=playpic,command=play_song)
playbtn.grid(row=0,column=1,padx=10)

stoppic=PhotoImage(file='stop2.png') #import image of stop button
#create stop button
stopbtn=ttk.Button(framemiddle,image=stoppic,command=stop_song)
stopbtn.grid(row=0,column=2,padx=10)

#create rewind
rewindpic=PhotoImage(file='rewind.png')
rewindbtn=ttk.Button(framelower,command=rewind,image=rewindpic)
rewindbtn.grid(row=0,column=1)

#creating a add button for playlist
addpic=PhotoImage(file='add.png')
addbtn=ttk.Button(frameleft,text="ADD",image=addpic,command=opens)
addbtn.pack(side=LEFT,padx=29)

#creating a delete button for playlist
delpic=PhotoImage(file='delete.png')
delbtn=ttk.Button(frameleft,text="DELETE",image=delpic,command=del_song)
delbtn.pack(side=LEFT)

#create mute button
global mute
mute=1
#importing images for mute and unmute
mutepic=PhotoImage(file='mute.png')
unmutepic=PhotoImage(file='unmute.png')
#creating mute button
mutebtn=ttk.Button(framelower,image=mutepic,command=mute_song)
mutebtn.grid(row=0,column=2,padx=10)
#create volume scale
volume_control=ttk.Scale(framelower,from_=0,to=100,orient=HORIZONTAL,variable=x,command=volume)
volume_control.set(30)#setting default value for scale
mixer.music.set_volume(0.3)#setting default value for volume
volume_control.grid(row=0,column=3,padx=15)


def close():
    stop_song()
    root.destroy()

root.protocol('WM_DELETE_WINDOW', close)

root.resizable(0,0)
root.mainloop()
