class Deck:
    def __init__(self) -> None:
        self.cards = []

    def draw(self):
        return self.cards.pop()
