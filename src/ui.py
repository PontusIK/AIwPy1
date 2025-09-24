import tkinter as tk

class Ui:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.canvas = tk.Canvas(root, width=950, height=710, bg="darkgreen")
        self.canvas.pack()
