from deck import Deck
from hand import Hand

class Game:
    def __init__(self):
        self.deck = Deck()
        self.playerHand = Hand()
        self.dealerHand = Hand()
        self.playerHand.addCard(self.deck.draw())
        self.playerHand.addCard(self.deck.draw())
