import json
import os
class Config:
    standartStuff = {
    "pathToSaveFolder": "{}\\temp".format(os.path.expanduser("~")),
    "fullFilePath":"Ещё не существует))",
    "scale":1,
}
    def __init__(self,file):
        self.file = file
        
        self.check()
        
        self.data = self.getData()
    
    def check(self):
        if not os.path.exists(self.file):
            self.toStandart()
    
    def putData(self,data):
        with open(self.file,"w",encoding="utf-8") as f:
            f.write(json.dumps(data,ensure_ascii=False,indent=4))
    def getData(self):
        with open(self.file,"r",encoding="utf-8") as f:
            return json.load(f)
    def toStandart(self):
        self.putData(Config.standartStuff)
        self.data = self.getData()
        if not os.path.exists(self.data["pathToSaveFolder"]):
            os.makedirs(self.data["pathToSaveFolder"])
