import tkinter as tk
from tkinter import ttk


# Main application window
root = tk.Tk()
root.title("Tkinter in Visual Studio")
ttk.Label(root, text="Hello, Tkinter!").pack()


# Custom window class
class FlipAndFind:
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Flip and Find")
        self.geometry("900x600")
        self.configure("#3a3a3a")


# Launch custom window after the first
flip_window = FlipAndFind(root)


root.mainloop()
