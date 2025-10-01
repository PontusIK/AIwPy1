import tkinter as tk
from game import Game
import card

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

        self.canvas = tk.Canvas(self, width=960, height=720, bg="darkgreen")
        self.canvas.pack()
        controlsFrame = tk.Frame(self)
        controlsFrame.pack(fill="x")

        tk.Button(controlsFrame, text="Hit", width=10, command=self.onHit).pack(side="right", pady=10, padx=10)
        tk.Button(controlsFrame, text="Stand", width=10, command=self.onStand).pack(side="right", pady=10, padx=10)

        self.game = None
        self.playerTurn = False
        self.photoImages = []
        self.playerHand = []
        self.dealerHand = []

    def start(self):
        self.resetCanvas()
        self.game = Game()
        self.playerTurn = True

        for i in range(3):
            deckImage = tk.PhotoImage(file=card.backSidePath())
            deckImage = deckImage.zoom(3)
            self.photoImages.append(deckImage)
            self.canvas.create_image((960/2)-(i*6), (720/2)-(i*6), image=deckImage)

        self.dealCard("player")
        self.dealCard("player")
        self.dealCard("dealer")
        self.dealCard("dealer")

    def resetCanvas(self):
        self.photoImages = []
        self.playerTurn = []
        self.dealerHand = []

    def onHit(self):
        if self.playerTurn:
            self.dealCard("player")

    def onStand(self):
        if self.playerTurn:
            self.playerTurn = False
            if self.game.getScore("player") <= 21:
                while self.game.getScore("dealer") < 17:
                    self.dealCard("dealer")

            face = tk.PhotoImage(file=self.game.dealerHand.cards[0].path).zoom(3)
            self.photoImages.append(face)
            self.canvas.itemconfig(self.dealerHand[0], image=face)

    def dealCard(self, participant):
        pass

class GameOverScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

def init():
    ui = Window()
    ui.mainloop()
