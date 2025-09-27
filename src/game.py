from deck import Deck
from hand import Hand

class Game:
    def __init__(self):
        self.deck = Deck()
        self.playerHand = Hand()
        self.dealerHand = Hand()

    def dealCard(self, participant):
        card = self.deck.draw()

        if participant == "player":
            self.playerHand.addCard(card)
        else:
            self.dealerHand.addCard(card)

        if self.dealerHand.count() == 1:
            return card.backSidePath()
        else:
            return card.path
