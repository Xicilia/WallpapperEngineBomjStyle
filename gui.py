import tkinter
import Config
import threading
import Desktop
import sys
from tkinter.filedialog import askopenfilename,askdirectory
import re

isThreadStopped = False

class GUI:
    
    def __init__(self,width,height,name):
        self.root = tkinter.Tk()
        self.root.geometry("{}x{}".format(width,height))
        self.root.title(name)
        #self.root.configure(bg = "#b16eff")
        
        self.config = Config.Config("config.json")
        
        self.frames = None
        self.isStarted = False
        self.thread = None
        
        self.desktop = Desktop.Desktop()
        self.wasInited = False
        self.scale = tkinter.BooleanVar()
        self.scale.set(self.config.data["scale"])
        
        self.rootLabels = {}
        
        self.initButtons()
        self.checkFile()
    
    def checkFile(self):
        if not re.match(r".+\.gif$", self.config.data["fullFilePath"]):
            self.rootLabels["warningFileLabel"].place(x = 20,y = 100)
            self.rootLabels["startButton"]["state"] = tkinter.DISABLED
            
        else:
            self.rootLabels["warningFileLabel"].place_forget()
            self.rootLabels["startButton"]["state"] = tkinter.NORMAL 
    
    def changeScale(self):
        self.config.data["scale"] = self.scale.get()
        self.config.putData(self.config.data)
    
    def chooseDirectory(self):
        
        directory = askdirectory()
        
        if directory:
            self.config.data["pathToSaveFolder"] = directory
            self.config.putData(self.config.data)
            self.rootLabels["currentDirectoryLabel"]["text"] = "Временная папка:{}".format(self.config.data["pathToSaveFolder"])
    
    def chooseFile(self):
        filename = askopenfilename()
        
        if filename:
            self.config.data["fullFilePath"] = filename
            self.config.putData((self.config.data))
            self.checkFile()
            self.rootLabels["currentFileLabel"]["text"] = self.config.data["fullFilePath"]
            self.wasInited = False
    
    def initButtons(self):
        fileLabel = tkinter.Label(self.root,text = "Текущий файл:")
        fileLabel.place(x=20,y=50)
        self.rootLabels["currentFileLabel"] = tkinter.Label(self.root,text = self.config.data["fullFilePath"])
        self.rootLabels["currentFileLabel"].place(x=120,y = 50)
        self.rootLabels["currentDirectoryLabel"] = tkinter.Label(self.root,text = "Папка с фреймами:{}".format(self.config.data["pathToSaveFolder"]))
        self.rootLabels["currentDirectoryLabel"].place(x=20,y = 200)
        self.rootLabels["currentDirectoryChange"] = tkinter.Button(self.root,text="Изменить",command=self.chooseDirectory)
        self.rootLabels["currentDirectoryChange"].place(x=20,y=220)
        self.rootLabels["warningFileLabel"] = tkinter.Label(self.root,text = "Файл не существует/не является файлом формата .gif")
        self.rootLabels["currentFileButton"] = tkinter.Button(self.root,text="Изменить",command = self.chooseFile)
        self.rootLabels["currentFileButton"].place(x=20,y = 70)
        self.rootLabels["startButton"] = tkinter.Button(self.root,text="Старт",command = self.startDesktop)
        self.rootLabels["startButton"].place(x=20,y=300)
        self.rootLabels["processingLabel"] = tkinter.Label(self.root,text="в процессе создания.........")
        self.rootLabels["processingInfoLabel"] = tkinter.Label(self.root,text="")
        self.rootLabels["scaleCheck"] = tkinter.Checkbutton(self.root,text = "Подстраивать изображения под экран",variable = self.scale,
                                                            onvalue = 1,offvalue = 0,command=self.changeScale)
        self.rootLabels["scaleCheck"].place(x=550,y = 20)
    def setupFramesAndStart(self):
        self.frames = Desktop.FrameList(self.scale.get(),self.rootLabels["processingInfoLabel"])
        self.desktop.setList(self.frames)
        self.rootLabels['processingLabel'].place_forget()
        self.rootLabels['processingInfoLabel'].place_forget()
        self.desktop.idle()
    def startDesktop(self):
        if self.wasInited and not self.isStarted:
            print("init again")
            self.thread = threading.Thread(target=self.desktop.idle)
            self.thread.start()
            self.rootLabels["currentFileButton"]["state"] = tkinter.DISABLED
            self.rootLabels["currentDirectoryChange"]["state"] = tkinter.DISABLED
            self.rootLabels["startButton"]["text"] = "Cтоп"
            self.isStarted = True
            return
        if not self.isStarted:
            self.rootLabels["startButton"]["text"] = "Cтоп"
            print("started getting frames")
            self.rootLabels['processingLabel'].place(x=100,y = 200)
            self.rootLabels["processingInfoLabel"].place(x = 100,y = 250)
            self.thread = threading.Thread(target=self.setupFramesAndStart)
            self.thread.start()
            #self.rootLabels['processingLabel'].place_forget()
            self.isStarted = True
            self.wasInited = True
            self.rootLabels["currentFileButton"]["state"] = tkinter.DISABLED
            self.rootLabels["currentDirectoryChange"]["state"] = tkinter.DISABLED
        else:
            self.rootLabels["startButton"]["text"] = "Cтарт"
            self.thread.do_run = False
            self.isStarted = False
            self.rootLabels["currentFileButton"]["state"] = tkinter.NORMAL
            self.rootLabels["currentDirectoryChange"]["state"] = tkinter.NORMAL
    
    def setupFile(self):
        pass
    
    def idle(self):
        self.root.mainloop()