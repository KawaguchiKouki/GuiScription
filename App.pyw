import tkinter
import subprocess
import json
import os

class TkObject():

    def __init__(self,conf,y,result):
        image = conf["image"]
        img = tkinter.PhotoImage(file=str(image["dir"]))
        self.img = img.subsample(4, 4)
        canvas = StartUp.Get().gui.canvas
        self.pos = {'x':image["pos"]["x"],'y':image["pos"]["y"]}
        self.cimg = canvas.create_image(self.pos['x'], self.pos['y'], image=self.img, anchor=tkinter.NW)
        color=conf["speak"]["color"]
        self.txt = tkinter.Label(StartUp.Get().root,text=result,background=str(color["back"]),foreground=str(color["docs"]),justify=str(conf["speak"]["justify"]))
        self.txt.place(x=int(conf["speak"]["pos_x"]), y=y)

class GuiWindow():
    def __init__(self):
        with open("./Scripts/Gui_Setting.json", "r",encoding="utf-8") as f:
            self.conf = json.load(f)
        self.FrameInit()
        canvas = self.conf["gui-object"]["canvas001"]
        self.canvas = tkinter.Canvas(width=int(StartUp.Get().conf["size"]["x"]), height=int(self.conf["gui-object"]["main"]["pos_y"]),bg=str(self.conf["gui-object"]["canvas001"]["color"]))
        self.canvas.place(x=0, y=0)
        self.canvas["yscrollcommand"]=self.scrollbar.set
        self.size_of = 100

    def FrameInit(self):
        self.frame = []
        conf = StartUp.Get().conf
        main = tkinter.Frame(StartUp.Get().root, width=int(conf["size"]["x"]),height=int(conf["size"]["y"]),bg=str(self.conf["gui-object"]["main"]["color"]))
        main.place(x=0,y=0)
        ufrm = tkinter.Frame(main,width=int(conf["size"]["x"]),height=int(self.conf["gui-object"]["main"]["pos_y"]))
        ufrm.place(x=0,y=0)
        __size = (int(conf["size"]["x"]),int(conf["size"]["y"])-int(self.conf["gui-object"]["main"]["pos_y"]))
        dfrm = tkinter.Frame(main,width=__size[0],height=__size[1],bg=str(self.conf["gui-object"]["sub002"]["color"]))
        dfrm.place(x=0,y=int(self.conf["gui-object"]["main"]["pos_y"]))
        self.scrollbar = tkinter.Scrollbar(ufrm)
        self.scrollbar.pack(side=tkinter.RIGHT, fill="y")
        self.frame.append(main)
        self.frame.append(ufrm)
        self.frame.append(dfrm)

    def StartObject(self):
        self.obj=list()
        self.txt = tkinter.Entry(width=int(self.conf["gui-object"]["text001"]["size"]))
        pos = self.conf["gui-object"]["text001"]["pos"]
        self.txt.place(x=int(pos["x"]), y=int(pos["y"]))

    def EirinAppendLine(self,result):
        obj = TkObject(self.conf["eirin"],self.size_of,result)
        self.obj.append(obj)
        for o in self.obj:
            print(o.img)
            print(o.pos)

    def YourAppendLine(self,cout):
        obj = TkObject(self.conf["you"],self.size_of,cout)
        self.obj.append(obj)

    def CallBack(self,event):
        try:
            txt = str(self.txt.get())
            self.YourAppendLine(txt)
            result = subprocess.check_output(txt.split(),stderr=subprocess.STDOUT,shell=True)
            self.EirinAppendLine(result)
        except Exception as e:
            self.EirinAppendLine(str(e))

class Window():
    def Config(self):
        with open("./Scripts/Setting.json", "r",encoding="utf-8") as f:
            self.conf = json.load(f)

    def Loop(self):
        self.Config()
        self.root = tkinter.Tk()
        self.gui = GuiWindow()
        self.gui.StartObject()
        subprocess.Popen(self.conf["shell"])
        self.root.title(self.conf["title"])
        self.root.geometry(f"{self.conf['size']['x']}x{str(self.conf['size']['y'])}")
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
