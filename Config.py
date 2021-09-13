import json
import os
class Config:
    standartStuff = {
    "filename":"animeGif228",
    "pathToSaveFolder":"C:\\Users\\Алая Дьяволица\\Desktop\\temp",
    "pathToFile":"C:\\Users\\Алая Дьяволица\\Desktop\\",
    "FullFilePath":"TEST",
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
