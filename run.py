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

        # Sidebar with background gradient
        self.sidebar = tk.Frame(self.bg_canvas, bg="#1a1a40", height=70)
        self.bg_canvas.create_window(
            0, 0,
            window=self.sidebar,
            anchor="nw",
            width=1000
        )

        self.title_container = tk.Frame(self.sidebar, bg="#1a1a40")
        self.title_container.pack(side="left", padx=10)

        self.sidebar_label = tk.Label(
            self.title_container,
            text="Flip and Find Game",
            fg="#fff",
            bg="#1a1a40",
            font=("Helvetica", 18, "bold")
        )
        self.sidebar_label.pack(anchor="w")

        self.subtitle_label = tk.Label(
            self.title_container,
            text="Test your memory!",
            fg="#aaa",
            bg="#1a1a40",
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

        # Adjusted grid wrapper to move the grid closer to the right panel
        self.grid_wrapper = tk.Frame(self.body, bg="#0d0d2b", padx=10)
        self.grid_wrapper.pack(expand=True, fill="both", side="left")

        # Adjusting the position of the grid within the wrapper
        self.grid_frame = tk.Frame(self.grid_wrapper, bg="#0d0d2b")
        self.grid_frame.place(relx=0.75, rely=0.5, anchor="center")

        self.right_panel = tk.Frame(self.body, bg="#0d0d2b", padx=20)
        self.right_panel.pack(side="right", fill="y", padx=(50, 10), pady=5)

        # Listbox for difficulty selection
        self.difficulty_label = tk.Label(
            self.right_panel,
            text="Current Level:",
            bg="#0d0d2b",
            fg="#FFFF00",
            font=("Helvetica", 17, "bold")
        )
        self.difficulty_label.pack(pady=(60, 5))

        self.difficulty_listbox = tk.Listbox(
            self.right_panel,
            height=3,
            width=15,
            font=("Helvetica", 20, "bold"),
            selectmode=tk.SINGLE,
            bd=3,
            relief="groove",
            bg="#1a1a40",
            fg="#FFFF00",
            highlightthickness=2,
            highlightcolor="#00ffff",
        )

        self.difficulty_listbox.insert(tk.END, "Easy", "Medium", "Hard")
        self.difficulty_listbox.select_set(0)  # Default selection
        self.difficulty_listbox.bind(
            "<<ListboxSelect>>",
            self.set_difficulty_from_listbox)
        self.difficulty_listbox.pack(pady=(10, 60))

        # Timer and Moves
        self.stats_frame = tk.Frame(self.right_panel, bg="#0d0d2b")
        self.stats_frame.pack(side="top", pady=(50, 0), anchor="center")

        self.timer_label = tk.Label(
            self.stats_frame,
            text="Time: 00:00",
            fg="#FF3131",
            bg="#0d0d2b",
            font=("Helvetica", 22, "bold")
        )
        self.timer_label.pack(pady=10)

        self.moves_label = tk.Label(
            self.stats_frame,
            text="Moves: 0",
            fg="#00ffff",
            bg="#0d0d2b",
            font=("Helvetica", 22, "bold")
        )
        self.moves_label.pack(pady=10)

        # Footer removed as the Start button is moved to the right panel

        # Adding Start Game Button to the Right Panel
        self.start_game_btn = tk.Button(
            self.right_panel,
            text="Start Game",
            command=self.toggle_game,
            bg="#00adb5",
            fg="#fff",
            font=("Helvetica", 14, "bold"),
            padx=15,
            pady=10,
            relief="raised",
            bd=3
        )
        self.start_game_btn.pack(pady=(30, 0))

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

    def set_difficulty_from_listbox(self, event):
        selection_index = self.difficulty_listbox.curselection()
        selected_difficulty = self.difficulty_listbox.get(selection_index)
        self.current_difficulty = selected_difficulty
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
                    relief="raised",
                    bd=3,
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
            command=self.reset_game,
            bg="#FF3131",
            fg="#FFF",
            font=("Helvetica", 14),
            relief="raised",
            bd=2
        )
        play_again_btn.pack(pady=10)

        self.congrats_frame.pack()


if __name__ == "__main__":
    root = tk.Tk()
    game = FlipAndFind(root)
    root.mainloop()
