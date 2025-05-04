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
        self.title("Flip and Find")  # Window title
        self.geometry("900x600")     # Window dimensions
        self.configure("#3a3a3a")    # Window background color
        self.custom_font = ("Helvetica, 14, bold")  # Font family
        self.colors = {
            'bg': "#3a3a3a",          # Main background color
            'card_bg': "#0f3469",     # Card background color
            'card_fg': "#e94560",     # Card foregorund color
            'sidebar_bg': "#16213e",  # Sidebar background color
        }


# Launch custom window after the first
flip_window = FlipAndFind(root)


root.mainloop()
