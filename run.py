import tkinter as tk
import time
import random


class FlipAndFind:
    def __init__(self, master=None):
        self.master = master
        self.master.title("Flip and Find")
        self.master.geometry("1000x600")
        self.master.configure(bg="#0d0d2b")

        self.first_start = True

        self.bg_canvas = tk.Canvas(
            self.master, width=1000, height=600, highlightthickness=0
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
                "symbols": [
                    "⭐", "❤️", "🔺", "🔵", "🐱", "🍀", "🎵", "🌙", "🌈", "⚽"
                ]
            },
            "Hard": {
                "grid": (5, 6),
                "symbols": [
                    "⭐", "❤️", "🔺", "🔵", "🐱", "🍀", "🎵", "🌙", "🌈", "⚽",
                    "🍕", "🐶", "📚", "☀️", "🎮"
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
        self.locked = False

        self.sidebar = tk.Frame(self.bg_canvas, bg="#1a1a40", height=70)
        sidebar_coords = (0, 0)
        self.bg_canvas.create_window(
            sidebar_coords[0], sidebar_coords[1],
            window=self.sidebar, anchor="nw", width=1000
        )

        self.title_container = tk.Frame(self.sidebar, bg="#1a1a40")
        self.title_container.pack(side="left", padx=10)

        tk.Label(
            self.title_container,
            text="Flip and Find Game",
            fg="#fff", bg="#1a1a40",
            font=("Helvetica", 24, "bold")
        ).pack(anchor="w")

        tk.Label(
            self.title_container,
            text="Test your memory!",
            fg="#aaa", bg="#1a1a40",
            font=("Helvetica", 20, "italic")
        ).pack(anchor="w")

        self.body = tk.Frame(self.bg_canvas, bg="#0d0d2b")
        self.bg_canvas.create_window(
            0, 70,
            window=self.body,
            anchor="nw",
            width=1000,
            height=460
        )

        self.grid_wrapper = tk.Frame(self.body, bg="#0d0d2b", padx=10)
        self.grid_wrapper.pack(expand=True, fill="both", side="left")

        self.grid_frame = tk.Frame(self.grid_wrapper, bg="#0d0d2b")
        self.grid_frame.place(relx=0.53, rely=0.5, anchor="center")

        self.right_panel = tk.Frame(self.body, bg="#0d0d2b", padx=20)
        self.right_panel.pack(side="right", fill="y", padx=(50, 10), pady=5)

        self.difficulty_label = tk.Label(
            self.right_panel,
            text="Current Level:", bg="#0d0d2b", fg="#FFFF00",
            font=("Helvetica", 17, "bold")
        )
        self.difficulty_label.pack(pady=(45, 0))

        self.difficulty_listbox = tk.Listbox(
            self.right_panel,
            height=3, width=15, font=("Helvetica", 20, "bold"),
            selectmode=tk.SINGLE, bd=3, relief="groove",
            bg="#1a1a40", fg="#FFFF00", highlightthickness=2,
            highlightcolor="#00ffff"
        )
        self.difficulty_listbox.insert(tk.END, "Easy", "Medium", "Hard")
        self.difficulty_listbox.select_set(0)
        self.difficulty_listbox.bind(
            "<<ListboxSelect>>",
            self.set_difficulty_from_listbox
        )

        self.difficulty_listbox.pack(pady=(20, 0))

        self.stats_frame = tk.Frame(self.right_panel, bg="#0d0d2b")
        self.stats_frame.pack(side="top", pady=(20, 0), anchor="center")

        self.start_game_btn = tk.Button(
            self.stats_frame, text="Start Game", command=self.toggle_game,
            bg="#00adb5", fg="#ff007f", font=("Helvetica", 20, "bold"),
            padx=15, pady=10, relief="raised", bd=3
        )
        self.start_game_btn.grid(row=3, column=0, pady=(55, 0))

        self.timer_label = tk.Label(
            self.stats_frame,
            text="Time: 00:00", fg="#FF3131", bg="#0d0d2b",
            font=("Helvetica", 22, "bold")
        )
        self.timer_label.grid(row=1, column=0, pady=(20, 5))

        self.moves_label = tk.Label(
            self.stats_frame,
            text="Moves: 0", fg="#00ffff", bg="#0d0d2b",
            font=("Helvetica", 22, "bold")
        )
        self.moves_label.grid(row=2, column=0, pady=(0, 5))

        # Add this overlay just before self.congrats_frame is defined
        self.overlay = tk.Frame(
            self.bg_canvas,
            bg='black',
            width=1000,
            height=600
        )

        self.overlay_window = self.bg_canvas.create_window(
            0, 0, window=self.overlay, anchor="nw", state="hidden"
        )

        self.overlay.lower()  # Send it behind any other widgets
        self.bg_canvas.itemconfigure(self.overlay_window, state="hidden")

        self.congrats_frame_width = 400
        self.congrats_frame_height = 300

        self.congrats_frame = tk.Frame(
            self.bg_canvas,
            bg="#222831",
            bd=4,
            relief="ridge",
            width=self.congrats_frame_width,
            height=self.congrats_frame_height
        )

# Move to left side (e.g., x=50). Adjust y if needed.
        window_coords = (
            (1000 - self.congrats_frame_width) // 2 + 90,
            (600 - self.congrats_frame_height) // 2
        )
        self.congrats_window = self.bg_canvas.create_window(
            window_coords[0], window_coords[1],
            window=self.congrats_frame, anchor="nw", state="hidden"
        )

        self.bg_canvas.itemconfigure(self.congrats_window, state="hidden")

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
        if self.first_start:
            self.start_game()
        else:
            self.reset_game()
            self.start_game()

    def start_game(self):
        self.reset_game()
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()
        self.start_game_btn.config(text="New Game", fg="#00ff00")
        self.first_start = False

    def reset_game(self):
        self.bg_canvas.itemconfigure(self.congrats_window, state="hidden")
        self.bg_canvas.itemconfigure(self.overlay_window, state="hidden")
        self.revealed = []
        self.matched_pairs = 0
        self.matched_cards = []
        self.moves = 0
        self.moves_label.config(text="Moves: 0")
        self.timer_label.config(text="Time: 00:00")
        self.timer_running = False
        self.create_grid()
        self.bg_canvas.itemconfigure(self.congrats_window, state="hidden")
        self.start_game_btn.config(text="Start Game", fg="#ff007f")

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
        symbol_pool = self.shuffle_without_adjacent_duplicates(
            symbol_pool,
            row_count,
            col_count
        )

        self.buttons = {}
        for row in range(row_count):
            for col in range(col_count):
                btn = tk.Button(
                    self.grid_frame, text="?", font=("Helvetica", 28),
                    width=4, height=2, relief="raised", bd=3,
                    command=lambda r=row, c=col: self.reveal_card(r, c)
                )
                btn.grid(row=row, column=col, padx=5, pady=5)
                button_info = {
                    "button": btn,
                    "symbol": symbol_pool.pop()
                }
                self.buttons[(row, col)] = button_info

    def shuffle_without_adjacent_duplicates(self, symbol_pool, rows, cols):
        max_attempts = 1000
        for _ in range(max_attempts):
            random.shuffle(symbol_pool)
            grid = [
                [symbol_pool[row * cols + col] for col in range(cols)]
                for row in range(rows)
            ]
            if not self.has_adjacent_duplicates(grid, rows, cols):
                return [symbol for row in grid for symbol in row]
        return symbol_pool  # fallback: give up after many tries

    def has_adjacent_duplicates(self, grid, rows, cols):
        for row in range(rows):
            for col in range(cols):
                symbol = grid[row][col]
                if col < cols - 1 and symbol == grid[row][col + 1]:
                    return True
                if row < rows - 1 and symbol == grid[row + 1][col]:
                    return True
        return False

    def reveal_card(self, row, col):
        if not self.timer_running or self.locked:
            return

        if (row, col) in self.revealed or (row, col) in self.matched_cards:
            return

        button = self.buttons[(row, col)]["button"]
        symbol = self.buttons[(row, col)]["symbol"]

        button.config(text=symbol)
        self.revealed.append((row, col))

        if len(self.revealed) == 2:
            self.locked = True  # Lock further clicks
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
            self.locked = False  # Unlock after successful match
        else:
            self.master.after(500, self.hide_cards, first_card, second_card)

        self.revealed = []

    def hide_cards(self, first_card, second_card):
        self.buttons[first_card]["button"].config(text="?")
        self.buttons[second_card]["button"].config(text="?")
        self.locked = False

    def update_timer(self):
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
            formatted_time = f"{minutes:02}:{seconds:02}"

            self.timer_label.config(text=f"Time: {formatted_time}")
            self.master.after(1000, self.update_timer)

    def show_congratulations(self):
        self.timer_running = False
        elapsed = int(time.time() - self.start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60
        formatted_time = f"{minutes:02}:{seconds:02}"

        for widget in self.congrats_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.congrats_frame, text="🎉 Congratulations! 🎉", bg="#222831",
            fg="#00ffcc", font=("Helvetica", 22, "bold")
        ).pack(pady=(20, 20))

        info_text = (
            f"Difficulty: {self.current_difficulty}\n"
            f"Moves: {self.moves}\n"
            f"Time: {formatted_time}"
        )

        tk.Label(
            self.congrats_frame, text=info_text, bg="#222831",
            fg="#eeeeee", font=("Helvetica", 22)
        ).pack(pady=20)

        tk.Button(
            self.congrats_frame, text="Play Again", command=self.reset_game,
            bg="#FF3131", fg="#FF5F1F", font=("Helvetica", 22),
            relief="raised", bd=2
        ).pack(pady=15)

        self.bg_canvas.itemconfigure(self.overlay_window, state="normal")
        self.bg_canvas.itemconfigure(self.congrats_window, state="normal")
        self.overlay.lift()  # Bring overlay to front
        self.congrats_frame.lift()  # Bring popup above overlay
        self.bg_canvas.update_idletasks()


if __name__ == "__main__":
    root = tk.Tk()
    game = FlipAndFind(root)
    root.mainloop()