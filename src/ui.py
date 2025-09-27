import tkinter as tk
from game import Game
import card

canvas = None
game = None
images = []
dealerHand = []
playerHand = []

def onHit():
    pass

def onStand():
    pass

def onStart():
    _ = resetCanvas()
    global game
    game = Game()

    for i in range(3):
        deckImage = tk.PhotoImage(file=card.backSidePath())
        deckImage = deckImage.zoom(2)
        images.append(deckImage)
        canvas.create_image((960/2)-(i*3), (720/2)-(i*3), image=deckImage)

    dealCard("player")
    dealCard("player")
    dealCard("dealer")
    dealCard("dealer")

def dealCard(participant):
    cardPath = game.dealCard(participant)
    cardImage = tk.PhotoImage(file=cardPath)
    cardImage = cardImage.zoom(2)
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
    xCoord = 960-10
    yCoord = 0
    offset = 0

    if participant == "player":
        yCoord = 720-10
        offset = -(len(playerHand)-1)*(64*1.5)
    else:
        yCoord = 10
        offset = -(len(dealerHand)-1)*(64*1.5)

    print(offset)
    canvas.coords(imageId, xCoord, yCoord)
    canvas.move(imageId, offset, 0)

def resetCanvas():
    global images
    images = []

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
