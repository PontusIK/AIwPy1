import os


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.path = os.path.join(getAssetDir(), f"card_{self.suit}_{self.rank}.png")

def getAssetDir():
    baseDir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(baseDir, "..", "assets")
        
def backSidePath():
    return os.path.join(getAssetDir(), "card_back.png")

def getChip(color):
    return os.path.join(getAssetDir(), f"chip_{color}.png")
