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

    def getScore(self, participant):
        hand = self.playerHand if participant == "player" else self.dealerHand
        score1 = score(hand, 1)
        score2 = score(hand, 11)
        if score2 > 21:
            return score1
        else:
            return score2

def score(hand: Hand, aceValue: int):
    score = 0
    for card in hand.cards:
        if card.rank == "A":
            score += aceValue
        elif card.rank == "J" or card.rank == "Q" or card.rank == "K":
            score += 10
        else:
            score += int(card.rank)

    return score
