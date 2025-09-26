import tkinter as tk
from game import Game

def onHit():
    pass

def onStand():
    pass

def onStart():
    pass

def init():
    root = tk.Tk()
    root.title("Blackjack")

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
