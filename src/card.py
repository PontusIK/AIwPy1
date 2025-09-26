import os


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.path = self.setPath()

    def setPath(self):
        baseDir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(baseDir, f"../assets/card_{self.suit}_{self.rank}.png")
