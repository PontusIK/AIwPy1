import tkinter as tk
from game import Game
from ui import Ui

def start():
    root = tk.Tk()
    root.title("BlackJack")
    root.geometry("960x720")
    game = Game()
    _ = Ui(root, game)
    root.mainloop()

if __name__ == "__main__":
    start()
