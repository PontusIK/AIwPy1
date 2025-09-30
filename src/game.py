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
        possibleScores = self.calculateScores(participant)
        bestScore = possibleScores[0]
        for score in possibleScores:
            if score > bestScore and score <= 21:
                bestScore = score
        return bestScore

    def calculateScores(self, participant):
        hand = self.playerHand if participant == "player" else self.dealerHand

        cardValues = []
        for card in hand.cards:
            if card.rank in ["J", "Q", "K"]:
                cardValues.append([10])
            elif card.rank == "A":
                cardValues.append([1, 11])
            else:
                cardValues.append([int(card.rank)])

        possibleScores = [0]
        for values in cardValues:
            tmpScores = []
            for score in possibleScores:
                for value in values:
                    tmpScores.append(score + value)
            possibleScores = tmpScores

        return possibleScores

    def getWinner(self):
        playerScore = self.getScore("player")
        dealerScore = self.getScore("dealer")
        if playerScore > 21:
            return "dealer"
        if dealerScore > 21:
            return "player"
        return "dealer" if dealerScore >= playerScore else "player"

