import random
import tkinter as tk
from game import Game
import card

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.score = 1000
        self.playerBank = []

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

    def restart(self):
        self.score = 1000
        self.chips = []
        self.frames[GameScreen].populatePlayerBank()
        self.newGame()

class GameScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.playerTurn = False
        self.photoImages = []
        self.playerHand = []
        self.dealerHand = []
        self.bettedChips = []
        self.scoreText = tk.StringVar(value="Score: 1000 ")

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

        self.populatePlayerBank()

    def populatePlayerBank(self):
        xCoord = 960*0.1
        yCoord = 720*0.9
        for _ in range(10):
            xCoord += random.randint(-20, 20)
            yCoord += random.randint(-20, 20)
            chipImage = tk.PhotoImage(file=card.getChip("red")).zoom(3)
            imageId = self.canvas.create_image(xCoord, yCoord, image=chipImage)
            self.controller.playerBank.append((chipImage, imageId))

    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.resetCanvas()
        self.playerTurn = True

        self.betChip("player")
        self.betChip("dealer")

        for i in range(3):
            deckImage = tk.PhotoImage(file=card.backSidePath()).zoom(3)
            self.photoImages.append(deckImage)
            self.canvas.create_image((960/2)-(i*6), (720/2)-(i*6), image=deckImage)

        self.dealCard("player")
        self.dealCard("player")
        self.dealCard("dealer")
        self.dealCard("dealer")

    def resetCanvas(self):
        self.scoreText.set(f"Score: {self.controller.score} ")
        self.photoImages = []
        self.playerHand = []
        self.dealerHand = []

    def betChip(self, participant):
        if participant == "dealer":
            startX = 960*0.25
            startY = 720*0.05

            chipImage = tk.PhotoImage(file=card.getChip("red")).zoom(3)
            imageId = self.canvas.create_image(startX, startY, image=chipImage)
            self.bettedChips.append((chipImage, imageId))
        else:
            chipImage, imageId = self.controller.playerBank.pop()
            self.bettedChips.append((chipImage, imageId))
            startX, startY = self.canvas.coords(imageId)

        finalX = int(960*0.15)+random.randint(-10, 10)
        finalY = int(720*0.5)+random.randint(-10, 10)
        dx = (finalX-startX)/10
        dy = (finalY-startY)/10

        def step(count=0):
            if count < 10:
                self.canvas.move(imageId, dx, dy)
                self.canvas.after(20, step, count+1)
            else:
                self.canvas.coords(imageId, finalX, finalY)

        step()

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
                playerScore = self.controller.game.getScore("player")
                dealerScore = self.controller.game.getScore("dealer")

                if playerScore > 21:
                    self.after(400, self.decideWinner)
                    return

                if dealerScore < 17:
                    self.dealCard("dealer")
                    self.after(400, dealToDealer)
                else:
                    self.after(400, self.decideWinner)

            dealToDealer()

    def decideWinner(self):
        winner = self.controller.game.getWinner()
        finalX = int(960*0.1)+random.randint(-20, 20)
        yOffset = 0.1 if winner == "dealer" else 0.9
        finalY = int(720*yOffset)+random.randint(-20, 20)

        def moveChip(imageId, dx, dy, count=0):
            if count < 10:
                self.canvas.move(imageId, dx, dy)
                self.after(20, lambda: moveChip(imageId, dx, dy, count+1))
            else:
                self.canvas.coords(imageId, finalX, finalY)

        for image, id in self.bettedChips:
            x0, y0 = self.canvas.coords(id)
            dx = (finalX - x0)/10
            dy = (finalY - y0)/10
            moveChip(id, dx, dy)
            if winner == "player":
                self.controller.playerBank.append((image, id))
        
        self.after(200, self.bettedChips.clear)

        if winner == "player":
            self.controller.score += 100
        else:
            self.controller.score -= 100

        self.scoreText.set(f"Score: {self.controller.score} ")

        if self.controller.score <= 0:
            self.after(1000, self.controller.showFrame, GameOverScreen)

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
                self.canvas.after(20, step, count+1)
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
            text="You Lose",
            font=("Times", 48, "bold"),
            fg="white",
            bg="darkgreen"
        ).pack(pady=(230, 10))

        tk.Button(
            frame,
            text="Restart",
            font=("Times", 18, "bold"),
            bd=3,
            command=controller.restart
        ).pack()

        tk.Button(
            frame,
            text="Quit",
            font=("Times", 18, "bold"),
            bd=3,
            command=controller.destroy
        ).pack(pady=10)

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
