from PIL import Image
from PIL import GifImagePlugin
import ctypes
import time
import Config
import os,shutil
import threading

class FrameList:
    
    def __init__(self,scale,label = None):
        self.config = Config.Config("config.json")
        
        self.path = self.config.data["fullFilePath"]
        self.label = label
        self.scale = scale
        if not os.path.exists(self.path):
            print("file not founded")
        
        self.image = Image.open(self.path)
        self.duration = self.image.info['duration']
        self.pathToSave = self.config.data["pathToSaveFolder"]
        self.size = self.image.n_frames
        self.cachedFile = None
        
        self._initFrames()
    def _clearBeforeInit(self):
        folder = self.pathToSave
        
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except:
                pass
    def _initFrames(self):
        self._clearBeforeInit()
        
        self.pathToCached = os.path.expanduser("~") + "\\AppData\\Roaming\\Microsoft\\Windows\\Themes\\CachedFiles"
        self.cachedFiles = [f for f in os.listdir(self.pathToCached) if os.path.isfile(os.path.join(self.pathToCached, f))]
        shutil.copy(os.path.join(self.pathToCached, self.cachedFiles[0]),self.config.data["pathToSaveFolder"])
        
        self.cachedFile = os.path.join(self.config.data["pathToSaveFolder"],self.cachedFiles[0])
        for frame in range(0,self.size):
            self.image.seek(frame)
            if self.scale:
                scaledImage = self.image.resize((1920,1080),Image.ANTIALIAS)
            else:
                scaledImage = self.image
            scaledImage.save("{}\\temp{}.png".format(self.config.data["pathToSaveFolder"],frame),quality=90)
            if self.label: self.label['text'] = '{} кадр из {} были идентефицированы'.format(frame,self.size)
     

class Desktop:

    def __init__(self,frameList = None):
        
        if not frameList:
            self.frameList = None
        else:
            self.frameList = frameList
        
        self.config = Config.Config("config.json")
        self.pathToSave = self.config.data["pathToSaveFolder"]

    def setList(self,frame_list):
        self.frameList = frame_list
    def idle(self):
        currentIndex = 0
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            ctypes.windll.user32.SystemParametersInfoW(20, 0, "{}\\temp{}.png".format(self.pathToSave,currentIndex) , 0)
            currentIndex += 1
            if currentIndex == self.frameList.size:
                currentIndex = 0
            time.sleep(self.frameList.duration/1000)
        else:
            ctypes.windll.user32.SystemParametersInfoW(20, 0, self.frameList.cachedFile , 0)