import tkinter as tk
import time
import random


class FlipAndFind:
    def __init__(self, master=None):
        self.master = master
        self.master.title("Flip and Find")
        self.master.geometry("1000x600")
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
        self.start_time = None
        self.timer_running = False

        self.sidebar = tk.Frame(self.master, bg="#16213e", height=70)
        self.sidebar.pack(fill="x", side="top")

        self.sidebar_label = tk.Label(
            self.sidebar,
            text="Flip and Find Game",
            fg="#fff",
            bg="#16213e",
            font=("Helvetica", 16, "bold")
        )
        self.sidebar_label.pack(side="left", padx=10)

        self.new_game_btn = tk.Button(
            self.sidebar,
            text="NEW GAME",
            command=self.reset_game,
            bg="#00adb5",
            fg="white",
            font=("Helvetica", 12, "bold"),
            padx=20,
            pady=5
        )
        self.new_game_btn.pack(side="top", pady=10)

        # --- Moved timer and moves labels to sidebar ---
        self.moves_label = tk.Label(
            self.sidebar,
            text="Moves: 0",
            fg="#00ffff",
            bg="#16213e",
            font=("Helvetica", 12, "bold")
        )
        self.moves_label.pack(side="right", padx=10)

        self.timer_label = tk.Label(
            self.sidebar,
            text="Time: 00:00",
            fg="#00ff00",
            bg="#16213e",
            font=("Helvetica", 12, "bold")
        )
        self.timer_label.pack(side="right", padx=10)

        self.body = tk.Frame(self.master, bg="#3a3a3a")
        self.body.pack(fill="both", expand=True, pady=10, padx=10)

        self.grid_frame = tk.Frame(self.body, bg="#3a3a3a")
        self.grid_frame.pack(side="left", padx=20)

        self.right_panel = tk.Frame(self.body, bg="#3a3a3a")
        self.right_panel.pack(side="right", padx=20, fill="y")

        self.difficulty_label = tk.Label(
            self.right_panel,
            text=f"Current Level: {self.current_difficulty}",
            bg="#3a3a3a",
            fg="white",
            font=("Helvetica", 14, "bold")
        )
        self.difficulty_label.pack(pady=(10, 5))

        self.difficulty_var = tk.StringVar(value=self.current_difficulty)
        self.difficulty_menu = tk.OptionMenu(
            self.right_panel,
            self.difficulty_var,
            *self.difficulty_levels.keys(),
            command=self.set_difficulty_from_dropdown
        )
        self.difficulty_menu.config(
            bg="#00adb5",
            fg="white",
            font=("Helvetica", 14, "bold"),
            width=12,
            highlightthickness=0
        )
        self.difficulty_menu.pack(pady=(0, 15))

        self.start_game_btn = tk.Button(
            self.right_panel,
            text="Start Game",
            command=self.start_game,
            bg="#4CAF50",
            fg="white",
            font=("Helvetica", 14, "bold"),
            padx=10,
            pady=5
        )
        self.start_game_btn.pack(pady=(30, 10))

        self.congrats_frame = tk.Frame(
            self.master,
            bg="#222831",
            bd=4,
            relief="ridge",
            width=300,
            height=250
        )
        self.congrats_frame.pack(side="bottom", pady=20)
        self.congrats_frame.pack_forget()

        self.create_grid()

    def set_difficulty_from_dropdown(self, value):
        self.current_difficulty = value
        self.difficulty_label.config(text=f"Current Level: {value}")
        self.reset_game()

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
        if not self.timer_running:
            return

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

        if not (
            first_card in self.matched_cards or
            second_card in self.matched_cards
        ):
            self.master.after(500, self.hide_cards, first_card, second_card)

        self.revealed = []

    def hide_cards(self, first_card, second_card):
        self.buttons[first_card]["button"].config(text="?")
        self.buttons[second_card]["button"].config(text="?")

    def update_timer(self):
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
            formatted_time = f"{minutes:02}:{seconds:02}"
            self.timer_label.config(text=f"Time: {formatted_time}")
            self.master.after(1000, self.update_timer)

    def start_game(self):
        self.reset_game()
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()

    def reset_game(self):
        self.revealed = []
        self.matched_pairs = 0
        self.matched_cards = []
        self.moves = 0
        self.moves_label.config(text="Moves: 0")
        self.timer_label.config(text="Time: 00:00")
        self.timer_running = False
        self.create_grid()
        self.congrats_frame.pack_forget()

    def show_congratulations(self):
        self.timer_running = False
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

        info_text = (
            f"Difficulty: {self.current_difficulty}\n"
            f"Moves: {self.moves}\n"
            f"Time: {formatted_time}"
        )
        stats_label = tk.Label(
            self.congrats_frame,
            text=info_text,
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
            command=self.start_game
        )
        play_again_btn.pack(pady=(10, 20))

        self.congrats_frame.pack()


# Run the application
root = tk.Tk()
flip_window = FlipAndFind(master=root)
root.mainloop()
