import tkinter as tk
from game import Game

class Ui:
    def __init__(self, root):
        self.root = root
        self.game = Game()
        self.canvas = tk.Canvas(root, width=950, height=710, bg="darkgreen")
        self.canvas.pack()
