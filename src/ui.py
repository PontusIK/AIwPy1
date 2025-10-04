import tkinter as tk
from game import Game
import card

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BlackJack")
        self.geometry("960x780")
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (GameScreen, GameOverScreen, WelcomeScreen):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.showFrame(WelcomeScreen)

    def showFrame(self, screenClass):
        frame = self.frames[screenClass]
        frame.tkraise()

    def newGame(self):
        self.game = Game()
        self.showFrame(GameScreen)

class GameScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.playerTurn = False
        self.photoImages = []
        self.playerHand = []
        self.dealerHand = []
        self.scoreText = tk.StringVar(value="Score: 1000 ")
        self.score = 1000

        self.canvas = tk.Canvas(self, width=960, height=720, bg="darkgreen")
        self.canvas.pack()
        controlsFrame = tk.Frame(self)
        controlsFrame.pack(fill="x")

        tk.Button(
            controlsFrame,
            text="Hit",
            width=10,
            font=("Times", 12, "bold"),
            bd=3,
            command=self.onHit
        ).pack(side="right", pady=10, padx=10)

        tk.Button(
            controlsFrame,
            text="Stand",
            width=10,
            font=("Times", 12, "bold"),
            bd=3,
            command=self.onStand
        ).pack(side="right", pady=10, padx=10)

        tk.Button(
            controlsFrame,
            text="New Game",
            width=10,
            font=("Times", 12, "bold"),
            bd=3,
            command=controller.newGame
        ).pack(side="left", pady=10, padx=10)

        tk.Label(
            controlsFrame,
            textvariable=self.scoreText,
            width=10,
            font=("Times", 12, "bold"),
        ).pack(side="left", pady=10, padx=10)

    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.resetCanvas()
        self.playerTurn = True

        for i in range(3):
            deckImage = tk.PhotoImage(file=card.backSidePath()).zoom(3)
            self.photoImages.append(deckImage)
            self.canvas.create_image((960/2)-(i*6), (720/2)-(i*6), image=deckImage)

        self.dealCard("player")
        self.dealCard("player")
        self.dealCard("dealer")
        self.dealCard("dealer")

    def resetCanvas(self):
        self.photoImages = []
        self.playerHand = []
        self.dealerHand = []

    def onHit(self):
        if self.playerTurn:
            self.dealCard("player")
            if self.controller.game.getScore("player") > 21:
                self.onStand()

    def onStand(self):
        if self.playerTurn:
            self.playerTurn = False

            face = tk.PhotoImage(file=self.controller.game.dealerHand.cards[0].path).zoom(3)
            self.photoImages.append(face)
            self.canvas.itemconfig(self.dealerHand[0], image=face)

            def dealToDealer():
                if self.controller.game.getScore("player") <= 21:
                    if self.controller.game.getScore("dealer") < 17:
                        self.dealCard("dealer")
                        self.after(400, dealToDealer)
            dealToDealer()

            if self.controller.game.getWinner() == "player":
                self.score += 100
            else:
                self.score -= 100

            self.scoreText.set(f"Score: {self.score} ")
            
            if self.score <= 0:
                self.canvas.after(1000, self.controller.showFrame, GameOverScreen)

    def dealCard(self, participant):
        cardPath = self.controller.game.dealCard(participant)
        cardImage = tk.PhotoImage(file=cardPath).zoom(3)
        self.photoImages.append(cardImage)
        imageId = self.canvas.create_image((960/2), (720/2), image=cardImage,
            anchor="se" if participant == "player" else "ne"
        )
        if participant == "player":
            self.playerHand.append(imageId)
        else:
            self.dealerHand.append(imageId)

        self.placeCard(participant, imageId)

    def placeCard(self, participant, imageId):
        xCoord = 960
        yCoord = 0
        offset = 0

        if participant == "player":
            yCoord = 720-10
            offset = -(len(self.playerHand)-1)*(64*2.1)
        else:
            yCoord = 10
            offset = -(len(self.dealerHand)-1)*(64*2.1)

        xCoord += offset
        
        x0, y0 = self.canvas.coords(imageId)
        dx = (xCoord - x0)/10
        dy = (yCoord - y0)/10

        def step(count=0):
            if count < 10:
                self.canvas.move(imageId, dx, dy)
                self.canvas.after(20, step, count + 1)
            else:
                self.canvas.coords(imageId, xCoord, yCoord)

        step()

class GameOverScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        frame = tk.Frame(self, bg="darkgreen")
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.winner = tk.StringVar()
        tk.Label(
            frame,
            textvariable=self.winner,
            font=("Times", 48, "bold"),
            fg="white",
            bg="darkgreen"
        ).pack(pady=(230, 10))

        tk.Button(
            frame,
            text="New Game",
            font=("Times", 18, "bold"),
            bd=3,
            command=lambda: controller.newGame()
        ).pack()

        tk.Button(
            frame,
            text="Quit",
            font=("Times", 18, "bold"),
            bd=3,
            command=controller.destroy
        ).pack(pady=10)

    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.winner.set(f"Winner: {self.controller.game.getWinner()}")

class WelcomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        frame = tk.Frame(self, bg="darkgreen")
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        tk.Label(
            frame,
            text="BlackJack",
            font=("Times", 48, "bold"),
            fg="white",
            bg="darkgreen"
        ).pack(pady=(230, 10))

        tk.Button(
            frame,
            text="Start",
            font=("Times", 18, "bold"),
            bd=3,
            command=lambda: controller.newGame()
        ).pack()

def init():
    ui = Window()
    ui.mainloop()
