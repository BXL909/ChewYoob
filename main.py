import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd
from pytube import YouTube
from urllib.request import urlopen
import io
import os
from PIL import Image, ImageTk
import datetime

# --- constants --- (UPPER_CASE_NAMES)
# title bar colors
TITLE_FOREGROUND = "orange"
TITLE_BACKGROUND = "#333"
TITLE_BACKGROUND_HOVER = "#333"
BUTTON_FOREGROUND = "orange"
BUTTON_BACKGROUND = TITLE_BACKGROUND
BUTTON_FOREGROUND_HOVER = BUTTON_FOREGROUND
BUTTON_BACKGROUND_HOVER = 'orange'
# window colors
WINDOW_BACKGROUND = "#222"
WINDOW_FOREGROUND = "#bbb"
WIN_BUTTONS_BACKGROUND = "#111"
WIN_BUTTONS_FOREGROUND = "white"

# --- classes --- (CamelCaseNames)
class MyButton(tk.Button):
    def __init__(self, master, text='x', command=None, **kwargs):
        super().__init__(master, bd=0,  padx=5, pady=2, 
                         fg=BUTTON_FOREGROUND, 
                         bg=BUTTON_BACKGROUND,
                         activebackground=BUTTON_BACKGROUND_HOVER,
                         activeforeground=BUTTON_FOREGROUND_HOVER, 
                         highlightthickness=0, 
                         text=text,
                         command=command)
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
    def on_enter(self, event):
        self['bg'] = BUTTON_BACKGROUND_HOVER
    def on_leave(self, event):
        self['bg'] = BUTTON_BACKGROUND

class MyTitleBar(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, relief='flat', bd=1, 
                         bg=TITLE_BACKGROUND,
                         highlightcolor=TITLE_BACKGROUND, 
                         highlightthickness=0)
        self.title_label = tk.Label(self, 
                                    bg=TITLE_BACKGROUND, 
                                    fg=TITLE_FOREGROUND)
        self.set_title("ChewYoob")
        self.close_button = MyButton(self, text='x', command=master.destroy)
        self.other_button = MyButton(self, text='?', command=self.on_other)
        self.pack(expand=True, fill='x')
        self.title_label.pack(side='left')
        self.close_button.pack(side='right')
        self.other_button.pack(side='right')
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.bind("<B1-Motion>", self.on_move)
    def set_title(self, title):
        self.title = title
        self.title_label['text'] = title
    def on_press(self, event):
        self.xwin = event.x
        self.ywin = event.y
        self.set_title("ChewYoob")
        self['bg'] = '#2c2c2c'
        self.title_label['bg'] = TITLE_BACKGROUND_HOVER
    def on_release(self, event):
        self.set_title("ChewYoob")
        self['bg'] = TITLE_BACKGROUND
        self.title_label['bg'] = TITLE_BACKGROUND
    def on_move(self, event):
        x = event.x_root - self.xwin
        y = event.y_root - self.ywin
        self.master.geometry(f'+{x}+{y}')
    def on_other(self):
        pic_url = "https://live.staticflickr.com/65535/52292348079_3a35909082_z.jpg"
        # open the web page picture and read it into a memory stream
        # and convert to an image Tkinter can handle
        my_page = urlopen(pic_url)
        # create an image file object
        my_picture = io.BytesIO(my_page.read())
        # use PIL to open image formats like .jpg  .png  .gif  etc.
        pil_img = Image.open(my_picture)
        pil_img_small = pil_img.resize((138,92))
        # convert to an image Tkinter can use
        global tk_img
        tk_img = ImageTk.PhotoImage(pil_img_small)
        imglabel.configure(image=tk_img)
        imglabel.image=tk_img
        disptitleofvideo.set("")
        dispvideoauthor.set("             ChewYoob v1.0")
        dispvideoduration.set("")
        dispvideopublishdate.set("   https://github.com/BXL909")
        dispvideofilesize.set("")

# --- main ---
root = tk.Tk()
root.overrideredirect(True) # turns off title bar, geometry
usermessage = StringVar()   # used to hold error messages and notifications
# window dimensions
w = 400
h = 240
# determine screen size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
# centre our window in the screen
xpoint = (screen_width/2) - (w/2)
ypoint = (screen_height/2) - (h/2)
root.geometry("%dx%d+%d+%d" % (w,h,xpoint,ypoint))  # set new geometry

# --- functions ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def validatelink():   
    inputstring = str(link.get())
    linklastchecked = str(link.get())
    #handle exceptions or download
    #no link provided
    if len(inputstring) == 0:
        usermessage.set("No URL provided!")     
        downloadButton.configure(state=DISABLED)
        return FALSE
    #check its not a url to somewhere else
    stringstocheck = ['youtube', 'youtu.be']
    res = [ele for ele in stringstocheck if (ele in inputstring)]
    if bool(res) == FALSE:        
        usermessage.set("YouTube links only!")
        downloadButton.configure(state=DISABLED)
        return FALSE
    return TRUE

def callback(link):
    content = link.get()
    if str(urlvalidcheckmark.get()) == "✓":
        if content == str(linklastchecked.get()):
            return
        else:
            usermessage.set("URL changed. Re-verify.")     
            urlvalidcheckmark.set("✗")
            downloadButton.configure(state=DISABLED)
            chooseDirButton.configure(state=DISABLED)
            dispvideofilesize.set("")
            disptitleofvideo.set("")
            dispvideoauthor.set("")
            dispvideoduration.set("")
            dispvideopublishdate.set("")
            mp3check.configure(state=DISABLED)
            imglabel.configure(image=tk_img_logo)
            imglabel.image=tk_img_logo

def choosefolder():
    foldername = fd.askdirectory()
    # foldername length will remain at zero if user cancels or escapes from askdirectory window
    if len(foldername) > 0:
        global folderloc 
        folderloc = foldername
        if len(foldername) > 28:
            dispfoldernamefordisplay.set(foldername[:28]+'...')
        else:
            dispfoldernamefordisplay.set(foldername)
        foldervalidcheckmark.set("✓")
        if urlvalidcheckmark.get() == "✓":
            downloadButton.configure(state=NORMAL)
        else:
            downloadButton.configure(state=DISABLED)

def downloader():
    #disable everything during download  
    usermessage.set("Downloading...")
    checkURLButton.configure(state=DISABLED)
    chooseDirButton.configure(state=DISABLED)
    downloadButton.configure(state=DISABLED)
    mp3check.configure(state=DISABLED)
    #refresh window
    root.update()
    #root.update_idletasks()
    inputstring = str(link.get())
    # link appears valid but video has a length of < 1 second
    url =YouTube(inputstring)
    if url.length < 1:
        usermessage.set("Video not found!")
        return
    if mp3only.get() == 1:
        video = url.streams.filter(only_audio=True).first()
        outfile = video.download(output_path=folderloc)
        # save the file
        base, ext = os.path.splitext(outfile)
        new_file = base + '.mp3'
        os.rename(outfile, new_file)
        usermessage.set("FILE DOWNLOADED")  
    else:
        video = url.streams.get_highest_resolution()
        video.download(output_path=folderloc)
        usermessage.set("FILE DOWNLOADED")  
    #enable everything again now that the file has either downloaded or failed
    checkURLButton.configure(state=NORMAL)
    chooseDirButton.configure(state=NORMAL)
    downloadButton.configure(state=NORMAL)
    mp3check.configure(state=NORMAL)

def confirmurl():
    if validatelink() == TRUE:
        usermessage.set("No video found!")
        global url
        confirmvideofound.set("N")
        url =YouTube(str(link.get()))
        # if video wasn't found, we'd have quit this function at this point so we can assume it was found if we're still here
        confirmvideofound.set("Y")
        if confirmvideofound.get()=="Y":
            usermessage.set("")
            urlvalidcheckmark.set("✓")
            chooseDirButton.configure(state=NORMAL)
            mp3check.configure(state=NORMAL)
        else:
            usermessage.set("No video found!")
            return
        global titleofvideo
        if len(url.title) > 34:
            titleofvideo = (url.title[:34]+'...')
        else:
            titleofvideo = url.title
        # use .title() to avoid UPPER, lower or mIxEd cases
        disptitleofvideo.set ("Title: " + titleofvideo.title())
        
        global videoauthor
        if len(url.author) > 34:
            videoauthor = (url.author[:34]+'...')
        else:
            videoauthor=url.author
        dispvideoauthor.set("Publisher: " + str(videoauthor))

        global videopublishdate
        videopublishdate = str(url.publish_date)[:10]
        dispvideopublishdate.set("Publish date: " + str(videopublishdate))

        global videoduration
        videoduration = url.length
        dispvideoduration.set("Duration: " + str(datetime.timedelta(seconds=videoduration)))

        global videofilesize
        video = url.streams.get_highest_resolution()
        videofilesize = round(video.filesize / 1048576,2) 
        dispvideofilesize.set("File size: " + str(videofilesize)+" Mb")

        global pic_url
        pic_url = url.thumbnail_url
        # open the web page picture and read it into a memory stream
        # and convert to an image Tkinter can handle
        my_page = urlopen(pic_url)
        # create an image file object
        my_picture = io.BytesIO(my_page.read())
        # use PIL to open image formats like .jpg  .png  .gif  etc.
        pil_img = Image.open(my_picture)
        pil_img_small = pil_img.resize((138,92))
        # convert to an image Tkinter can use
        global tk_img
        tk_img = ImageTk.PhotoImage(pil_img_small)
        imglabel.configure(image=tk_img)
        imglabel.image=tk_img
        if foldervalidcheckmark.get()=="✓":
            downloadButton.configure(state=NORMAL)
        else:
            downloadButton.configure(state=DISABLED)
    else:
        urlvalidcheckmark.set("✗")
        chooseDirButton.configure(state=DISABLED)
        dispvideofilesize.set("")
        disptitleofvideo.set("")
        dispvideoauthor.set("")
        dispvideoduration.set("")
        dispvideopublishdate.set("")
        inputstring = str(link.get())
        downloadButton.configure(state=DISABLED)
        mp3check.configure(state=DISABLED)
        imglabel.configure(image=tk_img_logo)
        imglabel.image=tk_img_logo
        # handle exceptions or download
        # no link provided
        if len(inputstring) == 0:
            usermessage.set("No URL provided!")     
            return FALSE
        # check its not a url to somewhere else
        stringstocheck = ['youtube', 'youtu.be']
        res = [ele for ele in stringstocheck if (ele in inputstring)]
        if bool(res) == FALSE:        
            usermessage.set("YouTube links only!")
            return FALSE        
        usermessage.set("No video found. Check URL.")

title_bar = MyTitleBar(root) 
#title_bar.pack()  # it is inside `TitleBar.__init__()`
# a canvas for the main area of the window
window = tk.Canvas(root, bg=WINDOW_BACKGROUND, highlightthickness=0)
# pack the widgets
window.pack(expand=True, fill='both')

link = StringVar()                  # user input
urlvalidcheckmark = StringVar()     # governs whether the tick displays after url checked
foldervalidcheckmark = StringVar()  # governs whether the tick displays after dir selected
disptitleofvideo = StringVar()      # video title after possible truncation
dispvideoauthor = StringVar()       # video auther after possible truncation
dispvideopublishdate = StringVar()  # video publish date
dispvideoduration = StringVar()     # calculated from total seconds
dispvideofilesize = StringVar()     # calculated from bytes
confirmvideofound = StringVar()     # flag to confirm we found a video
linklastchecked = StringVar()       # linklastchecked is used by a callback to compare any alterations to the input field to the last input that was checked on each keypress
link.trace("w", lambda name, index,mode, var=link: callback(var))   # attach callback to link field to check for changes

dispfoldernamefordisplay = StringVar()  # chosen folder name, potentially truncated
dispfoldernamefordisplay.set("No folder selected")

Label(root, text = 'YouTube URL:', bg=WINDOW_BACKGROUND, fg=WINDOW_FOREGROUND).place(x= 10 , y = 40)
Label(root, text = 'save to:', bg=WINDOW_BACKGROUND, fg=WINDOW_FOREGROUND).place(x= 10 , y = 180)
link_enter = Entry(root, textvariable=link, relief=FLAT, insertbackground="white",bg="#444", fg="#eee",width = 30)
link_enter.place(x = 94, y = 40)
usermessagelabel=Label(root, bg=WINDOW_BACKGROUND, fg=BUTTON_FOREGROUND, textvariable = usermessage)
usermessagelabel.place(x= 10 , y = 210) 
Label(root, bg=WINDOW_BACKGROUND, fg='orange', textvariable = urlvalidcheckmark).place(x= 282 , y = 38)  
Label(root, bg=WINDOW_BACKGROUND, fg='orange', textvariable = foldervalidcheckmark).place(x= 282 , y = 180)  

#youtube data fields
Label(root, bg=WINDOW_BACKGROUND, fg=WINDOW_FOREGROUND,textvariable=disptitleofvideo).place(x= 150 , y = 70)
Label(root, bg=WINDOW_BACKGROUND, fg=WINDOW_FOREGROUND,textvariable=dispvideoauthor).place(x= 150 , y = 90)
Label(root, bg=WINDOW_BACKGROUND, fg=WINDOW_FOREGROUND,textvariable=dispvideopublishdate).place(x= 150 , y = 110)
Label(root, bg=WINDOW_BACKGROUND, fg=WINDOW_FOREGROUND,textvariable=dispvideoduration).place(x= 150 , y = 130)
Label(root, bg=WINDOW_BACKGROUND, fg=WINDOW_FOREGROUND,textvariable=dispvideofilesize).place(x= 150 , y = 150)

#directory field
Label(root, bg=WINDOW_BACKGROUND, fg=WINDOW_FOREGROUND,textvariable=dispfoldernamefordisplay).place(x= 94 , y = 181)    

pic_url = "https://live.staticflickr.com/65535/52292348079_3a35909082_z.jpg"
# open the web page picture and read it into a memory stream
# and convert to an image Tkinter can handle
my_page = urlopen(pic_url)
# create an image file object
my_picture = io.BytesIO(my_page.read())
# use PIL to open image formats like .jpg  .png  .gif  etc.
pil_img = Image.open(my_picture)
pil_img_small = pil_img.resize((138,92))
# convert to an image Tkinter can use
global tk_img
tk_img = ImageTk.PhotoImage(pil_img_small)
tk_img_logo = ImageTk.PhotoImage(pil_img_small)
imglabel = Label(image=tk_img, border=0)
imglabel.place(x=10,y=74)

#MP3 checkbox
mp3only = IntVar()
mp3check = Checkbutton(root, state=DISABLED, bg=WINDOW_BACKGROUND, activebackground=WINDOW_BACKGROUND,fg=WINDOW_FOREGROUND, activeforeground=WINDOW_FOREGROUND, selectcolor=BUTTON_BACKGROUND,text="Audio only?", variable=mp3only, onvalue=1, offvalue=0)
mp3check.place (x=205, y=207)

#Buttons
checkURLButton = Button(root,text = 'VERIFY', relief=FLAT, borderwidth=0, pady=0, padx = 2, bg = WIN_BUTTONS_BACKGROUND, fg = WIN_BUTTONS_FOREGROUND, command = confirmurl)
checkURLButton.place(x=300 ,y = 40)
chooseDirButton = tk.Button(root, state=DISABLED, text = 'SAVE TO', relief=FLAT, borderwidth=0, pady=0, bg = WIN_BUTTONS_BACKGROUND, fg = WIN_BUTTONS_FOREGROUND, padx = 2, command = choosefolder)
chooseDirButton.place(x=300 ,y = 181)
downloadButton = tk.Button(root, state=DISABLED, text = 'DOWNLOAD', relief=FLAT, borderwidth=0, pady=0,  bg = WIN_BUTTONS_BACKGROUND, fg = WIN_BUTTONS_FOREGROUND, padx = 2, command = downloader)
downloadButton.place(x=300 ,y = 210)

#set initial focus on entry field
link_enter.focus_set()

root.mainloop()