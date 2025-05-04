import tkinter as tk
import time
import random


class FlipAndFind:
    def __init__(self, master=None):
        self.master = master
        self.master.title("Flip and Find")
        self.master.geometry("900x600")
        self.master.configure(bg="#3a3a3a")

        self.difficulty_levels = {
            "Easy": {
                "grid": (4, 3),
                "symbols": ["⭐", "❤️", "🔺", "🔵", "🐱", "🍀"]
            },
            "Medium": {
                "grid": (5, 4),
                "symbols": [
                    "⭐", "❤️", "🔺", "🔵", "🐱", "🍀", "🎵", "🌙",
                    "🌈", "⚽"
                ]
            },
            "Hard": {
                "grid": (6, 5),
                "symbols": [
                    "⭐", "❤️", "🔺", "🔵", "🐱", "🍀", "🎵", "🌙",
                    "🌈", "⚽", "🍕", "🐶", "📚", "☀️", "🎮"
                ]
            }
        }

        self.current_difficulty = "Easy"
        self.revealed = []
        self.matched_pairs = 0
        self.matched_cards = []
        self.moves = 0
        self.start_time = time.time()
        self.game_solved = False

        # Sidebar at the top
        self.sidebar = tk.Frame(self.master, bg="#16213e", height=70)
        self.sidebar.pack(fill="x", side="top")

        # Title and subtitle
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

        # Stats frame (timer and moves)
        self.stats_frame = tk.Frame(self.sidebar, bg="#16213e")
        self.stats_frame.pack(side="right", padx=20)

        self.timer_label = tk.Label(
            self.stats_frame,
            text="Time: 00:00",
            fg="#00ff00",
            bg="#16213e",
            font=("Helvetica", 16, "bold")
        )
        self.timer_label.pack(anchor="e")

        self.moves_label = tk.Label(
            self.stats_frame,
            text="Moves: 0",
            fg="#00ffff",
            bg="#16213e",
            font=("Helvetica", 16, "bold")
        )
        self.moves_label.pack(anchor="e")

        # Footer frame (difficulty buttons)
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

        # Main content frame (grid and congratulations side by side)
        self.content_frame = tk.Frame(self.master, bg="#3a3a3a")
        self.content_frame.pack(expand=True, fill="both", pady=20)

        # Game grid frame centered
        self.grid_frame = tk.Frame(self.content_frame, bg="#3a3a3a")
        self.grid_frame.pack(side="left", expand=True)

        # Congratulations frame
        self.congrats_frame = tk.Frame(
            self.content_frame,
            bg="#222831",
            bd=4,
            relief="ridge",
            width=300,
            height=250
        )
        self.congrats_frame.pack(
            side="right",
            padx=20,
            pady=20,
            fill="both",
            expand=False
        )
        self.congrats_frame.pack_forget()  # Hide until game is solved

        # Create the grid and timer
        self.create_grid()
        self.update_timer()

    def create_grid(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        grid_size = self.difficulty_levels[self.current_difficulty]["grid"]
        symbols = self.difficulty_levels[self.current_difficulty]["symbols"]

        row_count, col_count = grid_size
        total_pairs = (row_count * col_count) // 2

        symbol_pool = symbols[:total_pairs] * 2
        random.shuffle(symbol_pool)

        self.buttons = {}
        for row in range(row_count):
            for col in range(col_count):
                btn = tk.Button(
                    self.grid_frame,
                    text="?",
                    font=("Helvetica", 28),
                    width=4,
                    height=2,
                    command=lambda r=row, c=col: self.reveal_card(r, c)
                )
                btn.grid(row=row, column=col, padx=5, pady=5)
                self.buttons[(row, col)] = {
                    "button": btn,
                    "symbol": symbol_pool.pop()
                }

    def reveal_card(self, row, col):
        button = self.buttons[(row, col)]["button"]
        symbol = self.buttons[(row, col)]["symbol"]

        if (row, col) in self.revealed or (row, col) in self.matched_cards:
            return

        button.config(text=symbol)
        self.revealed.append((row, col))

        if len(self.revealed) == 2:
            self.master.after(500, self.check_match)

    def check_match(self):
        first_card = self.revealed[0]
        second_card = self.revealed[1]

        first_symbol = self.buttons[first_card]["symbol"]
        second_symbol = self.buttons[second_card]["symbol"]

        self.moves += 1
        self.moves_label.config(text=f"Moves: {self.moves}")

        if first_symbol == second_symbol:
            self.matched_pairs += 1
            self.matched_cards.extend([first_card, second_card])
            if self.matched_pairs == len(self.buttons) // 2:
                self.show_congratulations()

        self.master.after(500, self.hide_cards, first_card, second_card)
        self.revealed = []

    def hide_cards(self, first_card, second_card):
        if (
            first_card not in self.matched_cards
            and second_card not in self.matched_cards
        ):
            self.buttons[first_card]["button"].config(text="?")
            self.buttons[second_card]["button"].config(text="?")

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
        self.reset_game()

    def set_medium_difficulty(self):
        self.current_difficulty = "Medium"
        self.reset_game()

    def set_hard_difficulty(self):
        self.current_difficulty = "Hard"
        self.reset_game()

    def reset_game(self):
        self.revealed = []
        self.matched_pairs = 0
        self.matched_cards = []
        self.moves = 0
        self.start_time = time.time()
        self.moves_label.config(text="Moves: 0")
        self.create_grid()
        self.congrats_frame.pack_forget()

    def show_congratulations(self):
        elapsed = int(time.time() - self.start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60
        formatted_time = f"{minutes:02}:{seconds:02}"

        for widget in self.congrats_frame.winfo_children():
            widget.destroy()

        title = tk.Label(
            self.congrats_frame,
            text="🎉 Congratulations! 🎉",
            bg="#222831",
            fg="#00ffcc",
            font=("Helvetica", 16, "bold")
        )
        title.pack(pady=(20, 10))

        info = (
            f"Difficulty: {self.current_difficulty}\n"
            f"Moves: {self.moves}\n"
            f"Time: {formatted_time}"
        )
        stats_label = tk.Label(
            self.congrats_frame,
            text=info,
            bg="#222831",
            fg="#eeeeee",
            font=("Helvetica", 12)
        )
        stats_label.pack(pady=10)

        play_again_btn = tk.Button(
            self.congrats_frame,
            text="Play Again",
            font=("Helvetica", 12, "bold"),
            bg="#00adb5",
            fg="white",
            command=self.reset_game
        )
        play_again_btn.pack(pady=(10, 20))

        self.congrats_frame.pack(side="right", padx=20, pady=20, fill="both")


# Run the application
root = tk.Tk()
flip_window = FlipAndFind(master=root)
root.mainloop()
