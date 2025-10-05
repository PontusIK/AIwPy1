import os
import sys

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.path = getResourcePath(f"card_{self.suit}_{self.rank}.png")

def getResourcePath(relativePath):
    if hasattr(sys, "_MEIPASS"):
        basePath = sys._MEIPASS
    else:
        basePath = os.path.dirname(os.path.abspath(__file__))
        basePath = os.path.join(basePath, "..")
    return os.path.join(basePath, "assets", relativePath)

def backSidePath():
    return getResourcePath("card_back.png")

def getChip(color):
    return getResourcePath(f"chip_{color}.png")
