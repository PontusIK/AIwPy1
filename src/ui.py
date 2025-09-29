import tkinter as tk
from game import Game
import card

canvas = None
game = None
images = []
dealerHand = []
playerHand = []
playerTurn = False

def onHit():
    if playerTurn:
        dealCard("player")

def onStand():
    global playerTurn
    if playerTurn:
        playerTurn = False
        _ = showDealerHiddenCard()
        if game.getScore("player") < 21:
            while game.getScore("dealer") < 17:
                dealCard("dealer")
    print(f"player: {game.getScore("player")}")
    print(f"dealer: {game.getScore("dealer")}")


def showDealerHiddenCard():
    pass

def onStart():
    _ = resetCanvas()
    global game
    game = Game()
    global playerTurn
    playerTurn = True

    for i in range(3):
        deckImage = tk.PhotoImage(file=card.backSidePath())
        deckImage = deckImage.zoom(3)
        images.append(deckImage)
        canvas.create_image((960/2)-(i*6), (720/2)-(i*6), image=deckImage)

    dealCard("player")
    dealCard("player")
    dealCard("dealer")
    dealCard("dealer")

def dealCard(participant):
    cardPath = game.dealCard(participant)
    cardImage = tk.PhotoImage(file=cardPath)
    cardImage = cardImage.zoom(3)
    images.append(cardImage)
    imageId = canvas.create_image(50, 50, image=cardImage,
        anchor="se" if participant == "player" else "ne"
    )
    if participant == "player":
        playerHand.append(imageId)
    else:
        dealerHand.append(imageId)
    _ = placeCard(participant, imageId)

def placeCard(participant, imageId):
    xCoord = 960
    yCoord = 0
    offset = 0

    if participant == "player":
        yCoord = 720-10
        offset = -(len(playerHand)-1)*(64*2.1)
    else:
        yCoord = 10
        offset = -(len(dealerHand)-1)*(64*2.1)

    canvas.coords(imageId, xCoord, yCoord)
    canvas.move(imageId, offset, 0)

def resetCanvas():
    global images
    global dealerHand
    global playerHand
    images = []
    dealerHand = []
    playerHand = []

def init():
    root = tk.Tk()
    root.title("Blackjack")

    global canvas
    canvas = tk.Canvas(root, width=960, height=720, bg="darkgreen")
    canvas.pack()

    controlsFrame = tk.Frame(root)
    controlsFrame.pack(fill="x")

    hitButton = tk.Button(controlsFrame, text="Hit", width=10, command=onHit)
    hitButton.pack(side="right", pady=10, padx=10)
    standButton = tk.Button(controlsFrame, text="Stand", width=10, command=onStand)
    standButton.pack(side="right", pady=10, padx=10)
    startButton = tk.Button(controlsFrame, text="New Game", width=10, command=onStart)
    startButton.pack(side="left", pady=10, padx=10)

    root.mainloop()
