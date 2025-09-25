import tkinter as tk
from ui import Ui

def start():
    root = tk.Tk()
    root.title("BlackJack")
    root.geometry("960x720")
    _ = Ui(root)
    root.mainloop()

if __name__ == "__main__":
    start()
