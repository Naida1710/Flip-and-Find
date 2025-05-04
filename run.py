import tkinter as tk
import time


class FlipAndFind:
    def __init__(self, master=None):
        self.master = master
        self.master.title("Flip and Find")
        self.master.geometry("900x600")
        self.master.configure(bg="#3a3a3a")

        # Difficulty levels
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

        # Initial game state
        self.current_difficulty = "Easy"
        self.revealed = []
        self.matched_pairs = 0
        self.matched_cards = []
        self.moves = 0
        self.start_time = time.time()
        self.game_solved = False

        # Top bar
        self.sidebar = tk.Frame(self.master, bg="#16213e", height=70)
        self.sidebar.pack(fill="x", side="top")

        self.title_subtitle_frame = tk.Frame(self.sidebar, bg="#16213e")
        self.title_subtitle_frame.pack(side="left", padx=10)

        self.sidebar_label = tk.Label(
            self.title_subtitle_frame,
            text="Flip and Find Game",
            fg="#fff",
            bg="#16213e",
            font=("Helvetica", 16, "bold")
        )
        self.sidebar_label.pack(anchor="w")

        self.subtitle = tk.Label(
            self.title_subtitle_frame,
            text="TEST YOUR MEMORY",
            fg="#aaa",
            bg="#16213e",
            font=("Helvetica", 12)
        )
        self.subtitle.pack(anchor="w")

        # Timer on the right
        self.timer_label = tk.Label(
            self.sidebar,
            text="Time: 00:00",
            fg="#00ff00",
            bg="#16213e",
            font=("Helvetica", 16, "bold")
        )
        self.timer_label.pack(side="right", padx=20)

        # Footer for difficulty buttons
        self.footer = tk.Frame(self.master, bg="#16213e", height=60)
        self.footer.pack(fill="x", side="bottom")

        self.button_frame = tk.Frame(self.footer, bg="#16213e")
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

        self.update_timer()

    def update_timer(self):
        if self.start_time:
            elapsed = int(time.time() - self.start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
            formatted_time = f"{minutes:02}:{seconds:02}"
            self.timer_label.config(text=f"Time: {formatted_time}")
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


# Launch the app
root = tk.Tk()
flip_window = FlipAndFind(master=root)
root.mainloop()
