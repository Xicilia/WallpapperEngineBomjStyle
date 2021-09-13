from PIL import Image
from PIL import GifImagePlugin
import ctypes
import time
import Config
import os,shutil
import threading

class Desktop:

    def __init__(self):

        self.config = Config.Config("config.json")
    
        self.path = self.config.data["fullFilePath"]
        
        if not os.path.exists(self.path):
            print("file not founded")
            raise FileNotFoundError
            
        self.image = Image.open(self.path)
        self.pathToSave = self.config.data["pathToSaveFolder"]
        self.timeList = []
		
        self.size = self.image.n_frames
		
        self._initialization()

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

    def _initialization(self):
        self._clearBeforeInit()
        for frame in range(0,self.size):
            self.image.seek(frame)
            #print(self.image.info['duration'])
            self.timeList.append(self.image.info['duration'])
            self.image.save("{}\\temp{}.png".format(self.config.data["pathToSaveFolder"],frame))
    
    def idle(self):
        currentIndex = 0
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            ctypes.windll.user32.SystemParametersInfoW(20, 0, "{}\\temp{}.png".format(self.pathToSave,currentIndex) , 0)
            currentIndex += 1
            if currentIndex == self.size:
                currentIndex = 0
            time.sleep(self.timeList[currentIndex]/1000)