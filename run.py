import tkinter as tk
import time
import random


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

        # Timer and moves display
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

        # Grid Frame
        self.grid_frame = tk.Frame(self.master, bg="#3a3a3a")
        self.grid_frame.pack(pady=20)

        self.create_grid()
        self.update_timer()

    def create_grid(self):
        # Get grid size and symbols based on current difficulty
        grid_size = self.difficulty_levels[self.current_difficulty]["grid"]
        symbols = self.difficulty_levels[self.current_difficulty]["symbols"]

        # Double the symbols for pairs
        symbols = symbols + symbols
        random.shuffle(symbols)

        # Create grid of buttons
        self.buttons = {}
        row_count = grid_size[0]
        col_count = grid_size[1]

        for row in range(row_count):
            for col in range(col_count):
                btn = tk.Button(
                    self.grid_frame,
                    text="?",
                    width=8,
                    height=3,
                    command=lambda r=row, c=col: self.reveal_card(r, c)
                )

            btn.grid(row=row, column=col, padx=5, pady=5)
            self.buttons[(row, col)] = {"button": btn, "symbol": symbols.pop()}

    def reveal_card(self, row, col):
        button = self.buttons[(row, col)]["button"]
        symbol = self.buttons[(row, col)]["symbol"]

        # Show the symbol on the button
        button.config(text=symbol)

        # Add to revealed cards
        self.revealed.append((row, col))

        # Increment move count
        self.increment_moves()

        # Check if two cards are revealed
        if len(self.revealed) == 2:
            self.check_match()

    def check_match(self):
        first_card = self.revealed[0]
        second_card = self.revealed[1]

        first_symbol = self.buttons[first_card]["symbol"]
        second_symbol = self.buttons[second_card]["symbol"]

        # If they match, mark them as matched
        if first_symbol == second_symbol:
            self.matched_pairs += 1
            self.matched_cards.extend([first_card, second_card])
            if self.matched_pairs == len(self.buttons) // 2:
                print("You won!")

        # Hide the cards after a short delay if they don't match
        self.master.after(500, self.hide_cards, first_card, second_card)

        self.revealed = []

    def hide_cards(self, first_card, second_card):
        if (first_card not in self.matched_cards) and \
           (second_card not in self.matched_cards):
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

    def increment_moves(self):
        self.moves += 1
        self.moves_label.config(text=f"Moves: {self.moves}")

    def set_easy_difficulty(self):
        self.current_difficulty = "Easy"
        print(f"Difficulty set to: {self.current_difficulty}")
        self.reset_game()

    def set_medium_difficulty(self):
        self.current_difficulty = "Medium"
        print(f"Difficulty set to: {self.current_difficulty}")
        self.reset_game()

    def set_hard_difficulty(self):
        self.current_difficulty = "Hard"
        print(f"Difficulty set to: {self.current_difficulty}")
        self.reset_game()

    def reset_game(self):
        self.revealed = []
        self.matched_pairs = 0
        self.matched_cards = []
        self.moves = 0
        self.start_time = time.time()
        self.create_grid()


# Launch the app
root = tk.Tk()
flip_window = FlipAndFind(master=root)
root.mainloop()
