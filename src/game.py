from deck import Deck
from hand import Hand
from card import Card

class Game:
    def __init__(self):
        self.deck = Deck()
        self.playerHand = Hand()
        self.dealerHand = Hand()

    def dealCard(self):
        return self.deck.draw().path
