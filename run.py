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

        # Initial game state variables
        self.current_difficulty = "Easy"
        self.revealed = []
        self.matched_pairs = 0
        self.matched_cards = []
        self.moves = 0
        self.start_time = None
        self.game_solved = False

        # Create a top sidebar frame
        self.sidebar = tk.Frame(self.master, bg="#16213e", height=150)
        self.sidebar.pack(fill="x", side="top")

        # Add a label to the sidebar
        self.sidebar_label = tk.Label(
            self.sidebar,
            text="Flip and Find Game",
            fg="#fff",
            font=("Helvetica", 16, "bold")
        )
        self.sidebar_label.pack(padx=10, pady=10, side="left")


# Main application window
root = tk.Tk()
flip_window = FlipAndFind(master=root)

root.mainloop()
