import tkinter
import subprocess
import json
import os

class TkObject():

    def __init__(self,conf,y,result):
        image = conf["image"]
        self.img = tkinter.PhotoImage(file=str(image["dir"])).subsample(4, 4)
        canvas = StartUp.Get().gui.canvas
        canvas.create_image(image["pos"]["x"], image["pos"]["y"], image=self.img, anchor=tkinter.NW)
        color=conf["speak"]["color"]
        self.txt = tkinter.Label(StartUp.Get().root,text=result,background=str(color["back"]),foreground=str(color["docs"]),justify=conf["speak"]["justify"])
        self.txt.place(x=int(conf["speak"]["pos_x"]), y=y)

class GuiWindow():
    def __init__(self):
        with open("./Scripts/Gui_Setting.json", "r",encoding="utf-8") as f:
            self.conf = json.load(f)
        canvas = self.conf["gui-object"]["canvas001"]
        self.canvas = tkinter.Canvas(width=int(canvas["size"]["x"]), height=int(canvas["size"]["y"]))
        self.canvas.place(x=0, y=0)
        pass

    def StartObject(self):
        self.obj=list()
        self.txt = tkinter.Entry(width=int(self.conf["gui-object"]["text001"]["size"]))
        pos = self.conf["gui-object"]["text001"]["pos"]
        self.txt.place(x=int(pos["x"]), y=int(pos["y"]))

    def EirinAppendLine(self,result):
        obj = TkObject(self.conf["eirin"],150,result)
        self.obj.append(obj)

    def YourAppendLine(self,cout):
        obj = TkObject(self.conf["you"],100,cout)
        self.obj.append(obj)

    def CallBack(self,event):
        try:
            txt = str(self.txt.get())
            self.YourAppendLine(txt)
            result = subprocess.check_output(txt.split(),stderr=subprocess.STDOUT,shell=True)
            self.EirinAppendLine(result)
        except Exception as e:
            self.EirinAppendLine(str(e))
            return

class Window():
    def Config(self):
        with open("./Scripts/Setting.json", "r",encoding="utf-8") as f:
            self.conf = json.load(f)

    def Loop(self):
        self.root = tkinter.Tk()
        self.gui = GuiWindow()
        self.gui.StartObject()
        self.Config()
        subprocess.Popen(self.conf["shell"])
        self.root.title(self.conf["title"])
        self.root.geometry(str(self.conf["size"]["x"])+"x"+str(self.conf["size"]["y"]))
        self.root.bind('<Return>', self.gui.CallBack)
        self.root.mainloop()

class StartUp():
    __this = None
    def __init__(__self):
        pass

    @classmethod
    def Get(cls):
        if cls.__this is not None:
            return cls.__this
        cls.__this = Window()
        return cls.__this

    @classmethod
    def DestroyAllWindows(cls):
        cls.__this = None

    @classmethod
    def main(cls):
        cls.Get().Loop()

if __name__ == "__main__":
    StartUp.main()
