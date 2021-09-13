from PIL import Image
from PIL import GifImagePlugin
import ctypes
import time
import json
import os,shutil

class Config:
    standartStuff = {
    "filename":"animeGif228",
    "pathToSaveFolder":"C:\\Users\\student\\Desktop\\zmeya\\temp",
}
    def __init__(self,file):
        self.file = file
        
        self.check()
        
        self.data = self.getData()
    
    def check(self):
        if os.stat(self.file).st_size == 0:
            self.toStandart()
    
    def putData(self,data):
        with open(self.file,"w",encoding="utf-8") as f:
            f.write(json.dumps(data,ensure_ascii=False,indent=4))
    def getData(self):
        with open(self.file,"r",encoding="utf-8") as f:
            return json.load(f)
    def toStandart(self):
        self.putData(Config.standartStuff)

class Desktop:

    def __init__(self,pathToGifImage):

        self.config = Config("config.json")
    
        self.path = pathToGifImage + self.config.data["filename"] + ".gif"
        
        if not os.path.exists(self.path):
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
            self.image.save("temp/temp{}.png".format(frame))
        
    def idle(self):
        currentIndex = 0
        while True:
            ctypes.windll.user32.SystemParametersInfoW(20, 0, "{}\\temp{}.png".format(self.pathToSave,currentIndex) , 0)
            currentIndex += 1
            if currentIndex == self.size:
                currentIndex = 0
            time.sleep(self.timeList[currentIndex]/1000)
			
		
try:
    aa = Desktop("C:\\Users\\student\\Desktop\\")
    aa.idle()
except Exception as e:
    print(e)
    input()
