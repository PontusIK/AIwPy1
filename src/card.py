import os


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.path = os.path.join(self.getAssetDir(), f"card_{self.suit}_{self.rank}.png")

    def getAssetDir(self):
        baseDir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(baseDir, "..", "assets")
        
    def backSidePath(self):
        return os.path.join(self.getAssetDir(), "card_back.png")
