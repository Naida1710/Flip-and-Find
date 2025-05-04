import tkinter as tk
import time


class FlipAndFind:
    def __init__(self, master=None):
        self.master = master
        self.master.title("Flip and Find")
        self.master.geometry("900x600")
        self.master.configure(bg="#3a3a3a")

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

        self.current_difficulty = "Easy"
        self.revealed = []
        self.matched_pairs = 0
        self.matched_cards = []
        self.moves = 0
        self.start_time = time.time()
        self.game_solved = False

        # Sidebar setup
        self.sidebar = tk.Frame(self.master, bg="#16213e", height=70)
        self.sidebar.pack(fill="x", side="top")

        # Container for left title and subtitle
        self.left_sidebar = tk.Frame(self.sidebar, bg="#16213e")
        self.left_sidebar.pack(side="left", padx=10, pady=10)

        self.sidebar_label = tk.Label(
            self.left_sidebar,
            text="Flip and Find Game",
            fg="#ffffff",
            bg="#16213e",
            font=("Helvetica", 16, "bold")
        )
        self.sidebar_label.pack(anchor="w")

        self.subtitle_label = tk.Label(
            self.left_sidebar,
            text="TEST YOUR MEMORY",
            fg="#ffffff",
            bg="#16213e",
            font=("Helvetica", 10, "italic")
        )
        self.subtitle_label.pack(anchor="w")

        # Timer on the right
        self.timer_label = tk.Label(
            self.sidebar,
            text="Time: 0s",
            fg="#ffffff",
            bg="#16213e",
            font=("Helvetica", 10)
        )
        self.timer_label.pack(side="right", padx=10, pady=10)

        self.update_timer()

        # Footer with centered buttons
        self.footer = tk.Frame(self.master, bg="#1a1a1a", height=50)
        self.footer.pack(fill="x", side="bottom")

        self.button_frame = tk.Frame(self.footer, bg="#1a1a1a")
        self.button_frame.pack(pady=10)

        self.easy_button = tk.Button(
            self.button_frame,
            text="Easy",
            command=self.set_easy_difficulty
        )
        self.easy_button.pack(side="left", padx=10)

        self.medium_button = tk.Button(
            self.button_frame,
            text="Medium",
            command=self.set_medium_difficulty
        )
        self.medium_button.pack(side="left", padx=10)

        self.hard_button = tk.Button(
            self.button_frame,
            text="Hard",
            command=self.set_hard_difficulty
        )
        self.hard_button.pack(side="left", padx=10)

    def update_timer(self):
        elapsed = int(time.time() - self.start_time)
        self.timer_label.config(text=f"Time: {elapsed}s")
        self.master.after(1000, self.update_timer)

    def set_easy_difficulty(self):
        self.current_difficulty = "Easy"
        print(f"Difficulty set to: {self.current_difficulty}")

    def set_medium_difficulty(self):
        self.current_difficulty = "Medium"
        print(f"Difficulty set to: {self.current_difficulty}")

    def set_hard_difficulty(self):
        self.current_difficulty = "Hard"
        print(f"Difficulty set to: {self.current_difficulty}")


root = tk.Tk()
flip_window = FlipAndFind(master=root)
root.mainloop()
