import tkinter
import Config
import threading
import multiprocessing
import Desktop
import sys
from tkinter.filedialog import askopenfilename

isThreadStopped = False

class GUI:
    
    def __init__(self,width,height,name):
        self.root = tkinter.Tk()
        self.root.geometry("{}x{}".format(width,height))
        self.root.title(name)
        
        self.config = Config.Config("config.json")
        
        self.isStarted = False
        self.thread = None
        
        self.rootLabels = {
            "currentFileLabel":"Nothing",
            "currentFileButton":"Nothing",
            "startButton":"Nothing",
        }
        
        self.initButtons()
    
    def chooseFile(self):
        filename = askopenfilename()
        
        if filename:
            self.config.data["fullFilePath"] = filename
            self.config.putData((self.config.data))
            self.rootLabels["currentFileLabel"]["text"] = self.config.data["fullFilePath"]
    
    def initButtons(self):
        fileLabel = tkinter.Label(self.root,text = "Текущий файл:")
        fileLabel.place(x=20,y=50)
        self.rootLabels["currentFileLabel"] = tkinter.Label(self.root,text = self.config.data["fullFilePath"])
        self.rootLabels["currentFileLabel"].place(x=fileLabel.winfo_width()+120,y = 50)
        self.rootLabels["currentFileButton"] = tkinter.Button(self.root,text="изменить",command = self.chooseFile)
        self.rootLabels["currentFileButton"].place(x=20,y = 150)
        self.rootLabels["startButton"] = tkinter.Button(self.root,text="старт",command = self.startDesktop)
        self.rootLabels["startButton"].place(x=20,y=200)
    
    def setupDesktop(self):
        desktop.idle()
    
    def startDesktop(self):
        if not self.isStarted:
            self.rootLabels["startButton"]["text"] = "стоп"
            desktop = Desktop.Desktop()
            self.thread = threading.Thread(target=desktop.idle)
            self.thread.start()
            self.isStarted = True
            self.rootLabels["currentFileButton"]["state"] = tkinter.DISABLED
        else:
            self.rootLabels["startButton"]["text"] = "старт"
            self.thread.do_run = False
            self.isStarted = False
            self.rootLabels["currentFileButton"]["state"] = tkinter.NORMAL
    
    def setupFile(self):
        pass
    
    def idle(self):
        self.root.mainloop()