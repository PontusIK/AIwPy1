import tkinter as tk

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BlackJack")
        self.geometry("960x800")
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (GameScreen, GameOverScreen):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.showFrame(GameScreen)

    def showFrame(self, screenClass):
        frame = self.frames[screenClass]
        frame.tkraise()

class GameScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        tk.Canvas(self, width=960, height=720, bg="darkgreen").pack()
        controlsFrame = tk.Frame(self)
        controlsFrame.pack(fill="x")

        tk.Button(controlsFrame, text="Hit", width=10, command=self.onHit).pack(side="right", pady=10, padx=10)
        tk.Button(controlsFrame, text="Stand", width=10, command=self.onStand).pack(side="right", pady=10, padx=10)

    def onHit(self):
        pass

    def onStand(self):
        pass

class GameOverScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

def init():
    ui = Window()
    ui.mainloop()
