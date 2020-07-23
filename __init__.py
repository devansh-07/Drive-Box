import os
import time
import threading
import tkinter.ttk as ttk
from tkinter import *
from tkinter import filedialog
from io import BytesIO
from PIL import ImageTk, Image
from files.scripts.driveapi import DriveAPI
from files.scripts.toolTip import CreateToolTip
from files.scripts.mask import masking
import oauthlib
import requests

global conn, access, darkbg, USER, mainFrame, logoFrame, lbl_logo, wht, sm_font, imgLogo
conn = True
access = True
sm_font = ('Verdana', 9)
darkbg = "#292929"
wht = "#ffffff"
imgLogo = Image.open("files/images/logo.png").resize((80, 70))

def disableAll(f):
    for wd in f.winfo_children():
        try:
            wd.config(state='disabled')
        except:
            pass

def enableAll(f):
    for wd in f.winfo_children():
        try:
            wd.config(state='normal')
        except:
            pass

def insertData():
    global files
    fs = USER.getFileList()
    files.delete(0, END)
    for i, file in enumerate(fs):
        files.insert(i, ' '+file['name'])

def defaultMsg(clr, txt):
    global statusLbl
    statusLbl.config(fg=clr, text=txt)
    statusLbl.after(4000, lambda: statusLbl.config(fg=darkbg))

def chooseFile():
    filename = filedialog.askopenfilename()
    filePath.delete(0, END)
    filePath.insert(0, filename)

def refreshHelper():
    global files, statusLbl, trf
    trf = threading.Thread(target=insertData)
    trf.daemon = True
    trf.start()
    trfw = threading.Thread(target=waitForRfr)
    trfw.daemon = True
    trfw.start()

def waitForRfr():
    global statusLbl, trf
    i = 0
    statusLbl.config(fg="#34A952")
    while trf.is_alive():
        n = i%4
        tng = "Refreshing"+'.'*n
        statusLbl.config(text=tng)
        i += 1
        time.sleep(0.4)
    statusLbl.config(fg=darkbg)

def _signOut():
    soFrm.destroy()
    destroyWidgets(logoFrame)
    destroyWidgets(mainFrame)
    root.geometry("450x220")

    img = ImageTk.PhotoImage(imgLogo)
    lbl_logo = Label(logoFrame, image=img, bg=darkbg)
    lbl_logo.pack(side=LEFT, anchor='nw', pady=(20, 0))

    s = 'Signing out'
    lbl = Label(mainFrame, text=s, fg='#34A952', bg=darkbg, font=('Arial', 14))
    lbl.pack(pady=(40, 0))

    for i in range(7):
        time.sleep(0.3)
        txt = s + '.'*(i%4)
        lbl.config(text=txt.rjust(len(txt)+(i%4), ' '))
    root.quit()

def _showTop(event=None):
    global isTopActive, prf, soFrm, tltp
    tltp.leave()
    if isTopActive == True:
        soFrm.destroy()
        isTopActive = False
    else:
        soFrm = Toplevel()
        soFrm.wm_overrideredirect(True)
        x = prf.winfo_rootx() - 2
        y = prf.winfo_rooty() + prf.winfo_height() + 5
        soFrm.geometry("64x25+"+str(x)+"+"+str(y))
        soFrm.update()
        btnso = Button(soFrm, text="Sign out", fg=wht, bg="#1f1f1f", activebackground="#141414", activeforeground=wht, cursor='hand2', font=sm_font, border=0, command=_removeToken)
        btnso.pack()
        isTopActive = True

def _removeToken():
    os.remove('files/images/token.pickle')
    td = threading.Thread(target=_signOut)
    td.daemon = True
    td.start()

def _downStatus(idxx):
    global dwn, statusLbl, l
    l = ['00.00']
    down = USER.FileDownload(idxx, l)
    if down:
        defaultMsg("#34A952", "File Downloaded.")
    else:
        defaultMsg("#EA4436", "Can't Download this File.")

def waitForDown():
    global tdn, statusLbl, downBtn
    downBtn.config(state='disabled')
    s = 'Downloading'
    i = 0
    while tdn.is_alive():
        n = i%4
        statusLbl.config(fg='#34A952', text=s+('.'*n).ljust(3, ' ')+' - '+(l[0][:5])+'%')
        i += 1
        time.sleep(0.4)
    downBtn.config(state='normal')

def download():
    global files, tdn
    try:
        idx = files.curselection()
        idxx = idx[0]
        tdn = threading.Thread(target=lambda: _downStatus(idxx))
        tdn.daemon = True
        tdn.start()
        tds = threading.Thread(target=waitForDown)
        tds.daemon = True
        tds.start()
    except:
        defaultMsg("#EA4436", "Nothing Selected.")

def waitForUp():
    global tup
    s = 'Uploading'
    disableAll(mainF1)
    i = 0
    while tup.is_alive():
        statusLbl.config(fg='#34A952', text=s+('.'*(i%4)))
        i += 1
        time.sleep(0.4)
    enableAll(mainF1)

def _uploadStatus(fl):
    global dwn, statusLbl
    if fl.strip() != '':
        try:
            USER.FileUpload(fl)
            insertData()
            defaultMsg("#34A952", "File Uploaded.")
        except:
            defaultMsg("#EA4436", "Can't Upload File.")
    else:
        defaultMsg("#EA4436", "Enter valid Path or click Choose File.")

def upload():
    global tup
    tdp = threading.Thread(target=waitForUp)
    tdp.daemon = True
    tdp.start()
    tup = threading.Thread(target=lambda: _uploadStatus(filePath.get()))
    tup.daemon = True
    tup.start()

def _mainPage():
    global filePath, mainF1, files, logoFrame, lbl_logo, prfPic, name, statusLbl, isTopActive, prf, soFrm, downBtn, tltp
    root.geometry("450x470")

    small_logo = ImageTk.PhotoImage(imgLogo.resize((64, 56)))
    lbl_logo.config(image=small_logo)
    lbl_logo.image = small_logo
    lbl_logo.pack(padx=(10, 140), pady=(0, 0))

    dp = ImageTk.PhotoImage(prfPic)
    prf = Label(logoFrame, image=dp, bg=darkbg, cursor='hand2')
    prf.pack(side=RIGHT, padx=(130, 10))
    prf.image = dp

    isTopActive = False
    prf.bind("<ButtonPress>", _showTop)
    tltp = CreateToolTip(prf, name)

    mainF1 = Frame(mainFrame, bg=darkbg)
    mainF1.pack(padx=10, pady=(0, 0))

    mainF2 = Frame(mainFrame, bg=darkbg)
    mainF2.pack(padx=20, pady=(10, 0))

    upLbl = Label(mainF1, text='Upload files: ', bg=darkbg, fg="lightgrey")
    upLbl.pack(side=TOP, padx=(10, 0), pady=(10, 0), anchor='sw')

    filePath = Entry(mainF1, width=25, bg='lightgrey', font=('Verdana', 10))
    filePath.pack(side=LEFT, padx=(10, 10), ipady=1)

    getFileBtn = Button(mainF1, text="Choose File", fg=wht, bg="#1f1f1f", activebackground="#141414", activeforeground=wht, border=0, cursor='hand2', font=sm_font, command=chooseFile)
    getFileBtn.pack(side=LEFT, pady=(10, 10), padx=(0, 0))

    uploadBtn = Button(mainF1, text="Upload", fg=wht, bg="#1f1f1f", activebackground="#141414", activeforeground=wht, border=0, cursor='hand2', font=sm_font, command=upload)
    uploadBtn.pack(side=RIGHT, pady=(10, 10), padx=(10, 10))

    topF = Frame(mainF2, bg=darkbg)
    topF.pack(side=TOP, pady=(0, 0))

    af = Label(topF, text='All files: ', bg=darkbg, fg="lightgrey")
    af.pack(side=LEFT, padx=(0, 150), pady=(10, 10), anchor='sw')

    rfrBtn = Button(topF, fg=wht, bg="#1f1f1f", width=20, height=20, activebackground="#141414", activeforeground=wht, border=0, cursor='hand2', font=sm_font, command=refreshHelper)
    rfrBtn.pack(side=RIGHT, padx=(150, 0), pady=(10, 10))
    rfrImg = PhotoImage(file='files/images/refresh.png')
    rfrBtn.config(image=rfrImg)
    rfrBtn.image = rfrImg
    CreateToolTip(rfrBtn, "Refresh")

    boxF = Frame(mainF2, bg=darkbg)
    boxF.pack(side=TOP, anchor='w')

    scrollbar = ttk.Scrollbar(boxF)
    scrollbar.pack(side=RIGHT, fill=Y)

    files = Listbox(boxF, width=47, height=10, bg='lightgrey', yscrollcommand=scrollbar.set)
    files.pack(side=LEFT, anchor='sw')
    scrollbar.config(command=files.yview)

    statusLbl = Label(mainF2, text='Downloading', bg=darkbg, fg=darkbg, font=('Arial', 11))
    statusLbl.pack(side=LEFT, pady=(15, 8), anchor='sw')

    downBtn = Button(mainF2, text="Download", width=8, fg=wht, bg="#1f1f1f", activebackground="#141414", activeforeground=wht, border=0, cursor='hand2', font=sm_font, command=download)
    downBtn.pack(side=RIGHT, pady=(15, 10), anchor='se')

    tn = threading.Thread(target=insertData)
    tn.daemon = True
    tn.start()

def destroyWidgets(f):
    for wd in f.winfo_children():
        wd.destroy()

def getAuth_API():
    global access
    try:
        USER._getAuth()
        _connToAPI()
    except oauthlib.oauth2.rfc6749.errors.AccessDeniedError:
        access = False

def _connToAPI():
    global conn, name, prfPic
    k = USER._callAPI()
    if k == False:
        conn = False
    else:
        name, url = USER._getProfile()
        img_data = requests.get(url).content
        prfPic = masking(Image.open(BytesIO(img_data)).resize((56, 56)))

def thrAuth():
    t1 = threading.Thread(target=getAuth_API)
    t1.daemon = True
    t1.start()
    t2 = threading.Thread(target=lambda: waitForAuth(t1))
    t2.daemon = True
    t2.start()

def colorLabel(s, vl, thread):
    colors = ["#4285F5", "#EA4436", "#FBBD06", "#34A952"]
    i = 0
    while thread.is_alive():
        n = i%4
        tng = s+'.'*n
        vl.config(fg=colors[n], text=tng.rjust(len(tng)+n, ' '))
        i += 1
        time.sleep(0.4)
        if not conn or not access:
            break

def waitForAuth(thr):
    destroyWidgets(mainFrame)
    s = 'Authenticating'
    lbl = Label(mainFrame, text=s, bg=darkbg, font=('Arial', 12))
    lbl.pack(pady=(40, 0), side=LEFT, anchor='sw')
    colorLabel(s, lbl, thr)
    if conn and access:
        destroyWidgets(mainFrame)
        _mainPage()
    else:
        if not conn:
            lbl.config(fg='#EA4436', text="No Internet Connection.")
        elif not access:
            lbl.config(fg='#EA4436', text="Access Denied.")

def waitForConn(thr):
    s = 'Connecting to Drive'
    lbl1 = Label(mainFrame, text=s, bg=darkbg, font=('Arial', 12))
    lbl1.pack(pady=(30, 0))
    colorLabel(s, lbl1, thr)

    if conn == True:
        destroyWidgets(mainFrame)
        _mainPage()
    else:
        lbl1.config(fg='#EA4436', text="Can't connect to Drive\nNo Internet", font=('Arial', 13))

root = Tk()
root.resizable(width=False, height=False)
root.title("DrivePlay")
root.configure(bg=darkbg)
root.geometry("450x220+400+400")
try:
    p = ImageTk.PhotoImage(file='files/images/icon.png')
    root.iconphoto(False, p)
except:
    pass

logoFrame = Frame(root, bg=darkbg)
logoFrame.pack(side=TOP, padx=(10, 10), pady=(20, 0))

mainFrame = Frame(root, bg=darkbg)
mainFrame.pack(padx=10, pady=(10, 0))

logo = ImageTk.PhotoImage(imgLogo)
lbl_logo = Label(logoFrame, image=logo, bg=darkbg)
lbl_logo.pack(side=LEFT, anchor='nw', pady=(20, 0))

USER = DriveAPI()
if USER.auth == 0:
    lbl_logo.pack(pady=(10, 0))

    button = Button(mainFrame, text="Start", fg=wht, bg="#1f1f1f", activebackground="#141414", activeforeground=wht, border=0, cursor='hand2', width=7, command=thrAuth)
    button.pack(side=TOP, pady=(30, 10))
else:
    th1 = threading.Thread(target=_connToAPI)
    th1.daemon = True
    th1.start()
    th12 = threading.Thread(target=lambda: waitForConn(th1))
    th12.daemon = True
    th12.start()

root.mainloop()
