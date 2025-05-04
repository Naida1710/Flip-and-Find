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
        self.sidebar = tk.Frame(self.master, bg="#16213e", height=100)
        self.sidebar.pack(fill="x", side="top")

        # Add a label to the sidebar for the game title
        self.sidebar_label = tk.Label(
            self.sidebar,
            text="Flip and Find Game",
            fg="#fff",
            font=("Helvetica", 16, "bold")
        )
        self.sidebar_label.pack(padx=10, pady=5, side="top")

        # Add a subtitle in the sidebar directly under the label
        self.subtitle_label = tk.Label(
            self.sidebar,
            text="TEST YOUR MEMORY",
            fg="#fff",
            font=("Helvetica", 12, "italic")
        )
        self.subtitle_label.pack(padx=10, pady=5, side="top")

        # Add a button for switching difficulty
        self.easy_button = tk.Button(
            self.sidebar,
            text="Easy",
            command=self.set_easy_difficulty
        )
        self.easy_button.pack(side="left", padx=5)

        self.medium_button = tk.Button(
            self.sidebar,
            text="Medium",
            command=self.set_medium_difficulty
        )
        self.medium_button.pack(side="left", padx=5)

        self.hard_button = tk.Button(
            self.sidebar,
            text="Hard",
            command=self.set_hard_difficulty
        )
        self.hard_button.pack(side="left", padx=5)

    def set_easy_difficulty(self):
        self.current_difficulty = "Easy"
        print(f"Difficulty set to: {self.current_difficulty}")

    def set_medium_difficulty(self):
        self.current_difficulty = "Medium"
        print(f"Difficulty set to: {self.current_difficulty}")

    def set_hard_difficulty(self):
        self.current_difficulty = "Hard"
        print(f"Difficulty set to: {self.current_difficulty}")


# Main application window
root = tk.Tk()
flip_window = FlipAndFind(master=root)

root.mainloop()
