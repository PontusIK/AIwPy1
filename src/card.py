class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.path = f"../assets/card_{suit}_{rank}.png"
