import tkinter as tk


class FlipAndFind:
    def __init__(self, master=None):
        self.master = master
        self.master.title("Flip and Find")  # Window title
        self.master.geometry("900x600")     # Window dimensions
        self.master.configure(bg="#3a3a3a")  # Window background color

        # Define difficulty levels with symbols
        self.difficulty_levels = {
            "Easy": {
                "grid": (4, 4),
                "symbols": ["⭐", "❤️", "🔺", "🔺", "🔺", "🔺", "🔺", "🔺"]
            },
            "Medium": {
                "grid": (6, 6),
                "symbols": ["⭐", "❤️", "🔺", "🔺", "🔺", "🔺", "🔺", "🔺"]
            },
            "Hard": {
                "grid": (8, 8),
                "symbols": ["⭐", "❤️", "🔺", "🔺", "🔺", "🔺", "🔺", "🔺"]
            }
        }


# Main application window
root = tk.Tk()
flip_window = FlipAndFind(master=root)

root.mainloop()
