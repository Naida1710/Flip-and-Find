import tkinter as tk
import time
import random


class FlipAndFind:
    def __init__(self, master=None):
        self.master = master
        self.master.title("Flip and Find")
        self.master.geometry("1000x600")
        self.master.configure(bg="#0d0d2b")

        # Background canvas with gradient
        self.bg_canvas = tk.Canvas(
            self.master,
            width=1000,
            height=600,
            highlightthickness=0
        )
        self.bg_canvas.pack(fill="both", expand=True)
        self.draw_gradient(self.bg_canvas, 1000, 600, "#0d0d2b", "#1a1a40")

        self.difficulty_levels = {
            "Easy": {
                "grid": (4, 3),
                "symbols": ["⭐", "❤️", "🔺", "🔵", "🐱", "🍀"]
            },
            "Medium": {
                "grid": (5, 4),
                "symbols": ["⭐", "❤️", "🔺", "🔵", "🐱", "🍀", "🎵", "🌙", "🌈", "⚽"]
            },
            "Hard": {
                "grid": (5, 6),
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

        # Sidebar
        self.sidebar = tk.Frame(self.bg_canvas, bg="#16213e", height=70)
        self.bg_canvas.create_window(
            0, 0,
            window=self.sidebar,
            anchor="nw",
            width=1000
        )

        self.title_container = tk.Frame(self.sidebar, bg="#16213e")
        self.title_container.pack(side="left", padx=10)

        self.sidebar_label = tk.Label(
            self.title_container,
            text="Flip and Find Game",
            fg="#fff",
            bg="#16213e",
            font=("Helvetica", 16, "bold")
        )
        self.sidebar_label.pack(anchor="w")

        self.subtitle_label = tk.Label(
            self.title_container,
            text="Test your memory!",
            fg="#aaa",
            bg="#16213e",
            font=("Helvetica", 12, "italic")
        )
        self.subtitle_label.pack(anchor="w")

        # Body
        self.body = tk.Frame(self.bg_canvas, bg="#0d0d2b")
        self.bg_canvas.create_window(
            0, 70,
            window=self.body,
            anchor="nw",
            width=1000,
            height=460
        )

        self.grid_frame = tk.Frame(self.body, bg="#0d0d2b")
        self.grid_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.right_panel = tk.Frame(self.body, bg="#0d0d2b")
        self.right_panel.pack(side="right", padx=20, fill="y")

        # Move the difficulty label and dropdown more down
        self.difficulty_label = tk.Label(
            self.right_panel,
            text="Current Level:",
            bg="#0d0d2b",
            fg="#FFFF00",
            font=("Helvetica", 14, "bold")
        )
        self.difficulty_label.pack(pady=(80, 0))

        self.difficulty_var = tk.StringVar(value=self.current_difficulty)
        self.difficulty_menu = tk.OptionMenu(
            self.right_panel,
            self.difficulty_var,
            "Easy", "Medium", "Hard",
            command=self.set_difficulty_from_dropdown
        )
        self.difficulty_menu.config(
            bg="#00adb5",
            fg="white",
            font=("Helvetica", 14, "bold"),
            width=12,
            highlightthickness=0
        )
        self.difficulty_menu.pack(pady=(10, 10))

        # Timer and Moves near the center of the right panel (not affected)
        self.stats_frame = tk.Frame(self.right_panel, bg="#0d0d2b")
        self.stats_frame.pack(side="top", pady=100, anchor="center")

        self.timer_label = tk.Label(
            self.stats_frame,
            text="Time: 00:00",
            fg="#FF3131",  # Red for the timer
            bg="#0d0d2b",
            font=("Helvetica", 20, "bold")  # Larger font size
        )
        self.timer_label.pack(pady=5)

        self.moves_label = tk.Label(
            self.stats_frame,
            text="Moves: 0",
            fg="#00ffff",  # Cyan for moves
            bg="#0d0d2b",
            font=("Helvetica", 20, "bold")  # Larger font size
        )
        self.moves_label.pack(pady=10)

        # Footer
        self.footer = tk.Frame(self.bg_canvas, bg="#16213e", height=70)
        self.bg_canvas.create_window(
            0, 540,
            window=self.footer,
            anchor="nw",
            width=1000
        )

        self.start_game_btn = tk.Button(
            self.footer,
            text="Start Game",
            command=self.toggle_game,
            bg="#0d0d2b",
            fg="#ff007f",
            font=("Helvetica", 14, "bold"),
            padx=10,
            pady=5
        )
        self.start_game_btn.pack(pady=15)

        # Congrats frame
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

    def draw_gradient(self, canvas, width, height, start_color, end_color):
        r1, g1, b1 = self.master.winfo_rgb(start_color)
        r2, g2, b2 = self.master.winfo_rgb(end_color)

        r_ratio = (r2 - r1) / height
        g_ratio = (g2 - g1) / height
        b_ratio = (b2 - b1) / height

        for i in range(height):
            nr = int(r1 + (r_ratio * i)) >> 8
            ng = int(g1 + (g_ratio * i)) >> 8
            nb = int(b1 + (b_ratio * i)) >> 8
            color = f"#{nr:02x}{ng:02x}{nb:02x}"
            canvas.create_line(0, i, width, i, fill=color)

    def toggle_game(self):
        if self.timer_running:
            self.reset_game()
        else:
            self.start_game()

    def set_difficulty_from_dropdown(self, value):
        self.current_difficulty = value
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
        self.start_game_btn.config(text="New Game", fg="#00ff00")
        self.update_timer()

    def reset_game(self):
        self.revealed = []
        self.matched_pairs = 0
        self.matched_cards = []
        self.moves = 0
        self.moves_label.config(text="Moves: 0")
        self.timer_label.config(text="Time: 00:00")
        self.timer_running = False
        self.start_game_btn.config(text="Start Game", fg="#ff007f")
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
            fg="black",
            command=self.start_game
        )
        play_again_btn.pack(pady=(10, 20))

        self.congrats_frame.pack(side="bottom", pady=20)


# Run the application
root = tk.Tk()
flip_window = FlipAndFind(master=root)
root.mainloop()
