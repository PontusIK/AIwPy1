from deck import Deck
from hand import Hand
import card

class Game:
    def __init__(self):
        self.deck = Deck()
        self.playerHand = Hand()
        self.dealerHand = Hand()

    def dealCard(self, participant):
        dealtCard = self.deck.draw()

        if participant == "player":
            self.playerHand.addCard(dealtCard)
        else:
            self.dealerHand.addCard(dealtCard)

        if self.dealerHand.count() == 1:
            return card.backSidePath()
        else:
            return dealtCard.path
