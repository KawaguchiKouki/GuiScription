import tkinter
import subprocess
import json
import os

class TkObject():
    def __init__(self,econf,y,result):
        self.img = tkinter.PhotoImage(file=str(econf["image-dir"])).subsample(4, 4)
        canvas = tkinter.Canvas(width=500, height=500)
        canvas.place(x=0, y=0)
        canvas.create_image(20, 60, image=self.img, anchor=tkinter.NW)
        color=econf["speak"]["color"]
        self.txt = tkinter.Label(StartUp.Get().root,text=result,background=str(color["back"]),foreground=str(color["docs"]))
        self.txt.place(x=int(econf["speak"]["pos_x"]), y=y)

class GuiWindow():
    def __init__(self):
        with open("./Scripts/Gui_Setting.json", "r",encoding="utf-8") as f:
            self.conf = json.load(f)
        pass

    def StartObject(self):
        self.obj=list()
        self.txt = tkinter.Entry(width=int(self.conf["gui-object"]["text001"]["size"]))
        pos = self.conf["gui-object"]["text001"]["pos"]
        self.txt.place(x=int(pos["x"]), y=int(pos["y"]))

    def AppendLine(self,result):
        obj = TkObject(self.conf["eirin"],100,result)
        self.obj.append(obj)

    def CallBack(self,event):
        try:
            txt = str(self.txt.get())
            print(txt)
            result = subprocess.check_output(txt.split(),stderr=subprocess.STDOUT,shell=True)
            self.AppendLine(result)
        except Exception:
            self.AppendLine("Error")
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
