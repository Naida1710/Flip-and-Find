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
                "symbols": ["⭐", "❤️", "🔺", "🔵", "🐱", "🍀", "🎵", "🌙", "🌈", "⚽"],
            },
            "Hard": {
                "grid": (6, 5),
                "symbols": [
                    "⭐", "❤️", "🔺", "🔵", "🐱", "🍀", "🎵", "🌙",
                    "🌈", "⚽", "🍕", "🐶", "📚", "☀️", "🎮"
                ],
            },
        }

        self.current_difficulty = "Easy"
        self.revealed = []
        self.matched_pairs = 0
        self.matched_cards = []
        self.moves = 0
        self.start_time = None
        self.game_solved = False

        # Start Game screen (initial screen)
        self.start_screen = tk.Frame(self.master, bg="#3a3a3a", height=600)
        self.start_screen.pack(fill="both", expand=True)

        self.start_title = tk.Label(
            self.start_screen,
            text="Welcome to Flip and Find!",
            fg="#fff",
            bg="#3a3a3a",
            font=("Helvetica", 20, "bold"),
        )
        self.start_title.pack(pady=20)

        self.start_subtitle = tk.Label(
            self.start_screen,
            text="Test your memory and have fun!",
            fg="#aaa",
            bg="#3a3a3a",
            font=("Helvetica", 14),
        )
        self.start_subtitle.pack(pady=10)

        self.start_button = tk.Button(
            self.start_screen,
            text="Start Game",
            font=("Helvetica", 16, "bold"),
            bg="#00adb5",
            fg="white",
            command=self.start_game,
        )
        self.start_button.pack(pady=30)

        # Game screen: initially hidden
        self.game_area = tk.Frame(self.master, bg="#3a3a3a")
        self.sidebar = tk.Frame(self.game_area, bg="#16213e", height=70)
        self.sidebar.pack(fill="x", side="top")

        self.sidebar_left = tk.Frame(self.sidebar, bg="#16213e")
        self.sidebar_left.pack(side="left", padx=10)

        self.sidebar_label = tk.Label(
            self.sidebar_left,
            text="Flip and Find Game",
            fg="#fff",
            bg="#16213e",
            font=("Helvetica", 16, "bold"),
        )
        self.sidebar_label.pack(anchor="w")

        self.subtitle = tk.Label(
            self.sidebar_left,
            text="TEST YOUR MEMORY",
            fg="#aaa",
            bg="#16213e",
            font=("Helvetica", 12),
        )
        self.subtitle.pack(anchor="w")

        self.new_game_btn = tk.Button(
            self.sidebar,
            text="New Game",
            font=("Helvetica", 12, "bold"),
            bg="#00adb5",
            fg="white",
            command=self.reset_game,
        )
        self.new_game_btn.pack(side="top", pady=10)

        self.stats_frame = tk.Frame(self.sidebar, bg="#16213e")
        self.stats_frame.pack(side="right", padx=20)

        self.timer_label = tk.Label(
            self.stats_frame,
            text="Time: 00:00",
            fg="#00ff00",
            bg="#16213e",
            font=("Helvetica", 16, "bold"),
        )
        self.timer_label.pack(anchor="e")

        self.moves_label = tk.Label(
            self.stats_frame,
            text="Moves: 0",
            fg="#00ffff",
            bg="#16213e",
            font=("Helvetica", 16, "bold"),
        )
        self.moves_label.pack(anchor="e")

        # Game area: grid left, right panel
        self.game_area_content = tk.Frame(self.game_area, bg="#3a3a3a")
        self.game_area_content.pack(fill="both", expand=True, pady=10, padx=20)

        # Game grid aligned left
        self.grid_frame = tk.Frame(self.game_area_content, bg="#3a3a3a")
        self.grid_frame.pack(side="left", padx=20, pady=20)

        # Right panel for difficulty and congratulations
        self.right_panel = tk.Frame(self.game_area_content, bg="#222831")
        self.right_panel.pack(side="right", fill="y", padx=20)

        # Difficulty buttons moved to right panel
        self.diff_label = tk.Label(
            self.right_panel,
            text="Select Difficulty",
            font=("Helvetica", 12, "bold"),
            bg="#222831",
            fg="white",
        )
        self.diff_label.pack(pady=(20, 5))

        self.difficulty_buttons = tk.Frame(self.right_panel, bg="#222831")
        self.difficulty_buttons.pack(pady=(0, 20))

        self.easy_button = tk.Button(
            self.difficulty_buttons,
            text="Easy",
            command=self.set_easy_difficulty,
            width=10
        )
        self.easy_button.pack(pady=5)

        self.medium_button = tk.Button(
            self.difficulty_buttons,
            text="Medium",
            command=self.set_medium_difficulty,
            width=10
        )
        self.medium_button.pack(pady=5)

        self.hard_button = tk.Button(
            self.difficulty_buttons,
            text="Hard",
            command=self.set_hard_difficulty,
            width=10
        )
        self.hard_button.pack(pady=5)

        # Congratulations frame under difficulty
        self.congrats_frame = tk.Frame(
            self.right_panel,
            bg="#393e46",
            bd=4,
            relief="ridge",
            width=250,
            height=200,
        )
        self.congrats_frame.pack(pady=20, fill="x")
        self.congrats_frame.pack_forget()

        self.create_grid()
        self.update_timer()

    def start_game(self):
        self.start_screen.pack_forget()  # Hide the start screen
        self.game_area.pack(fill="both", expand=True)  # Show the game screen

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
                    command=lambda r=row, c=col: self.reveal_card(r, c),
                )
                btn.grid(row=row, column=col, padx=5, pady=5)
                self.buttons[(row, col)] = {
                    "button": btn,
                    "symbol": symbol_pool.pop(),
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
        first_card, second_card = self.revealed
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
        if not (
            first_card in self.matched_cards or
            second_card in self.matched_cards
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
        formatted_time = f"{elapsed // 60:02}:{elapsed % 60:02}"

        for widget in self.congrats_frame.winfo_children():
            widget.destroy()

        title = tk.Label(
            self.congrats_frame,
            text="🎉 Congratulations! 🎉",
            bg="#393e46",
            fg="#00ffcc",
            font=("Helvetica", 14, "bold"),
        )
        title.pack(pady=(15, 5))

        info = (
            f"Difficulty: {self.current_difficulty}\n"
            f"Moves: {self.moves}\n"
            f"Time: {formatted_time}"
        )
        stats = tk.Label(
            self.congrats_frame,
            text=info,
            bg="#393e46",
            fg="white",
            font=("Helvetica", 11),
        )
        stats.pack(pady=5)

        again = tk.Button(
            self.congrats_frame,
            text="Play Again",
            font=("Helvetica", 12, "bold"),
            bg="#00adb5",
            fg="white",
            command=self.reset_game,
        )
        again.pack(pady=(10, 15))

        self.congrats_frame.pack(pady=20, fill="x")


# Run the app
root = tk.Tk()
app = FlipAndFind(master=root)
root.mainloop()
