import tkinter as tk
import random

BACKGROUND_COLOR = "#fafafa"
PRIMARY_COLOR = "#1abc9c"
ALERT_COLOR = "#e67e22"
TEXT_COLOR = "#34495e"
TITLE_FONT = ("Verdana", 22, "bold")
BUTTON_FONT = ("Verdana", 12)
RESULT_FONT = ("Verdana", 14, "bold")

class ChoiceBattleGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Choice Battle Game")
        self.geometry("620x650")
        self.config(bg=BACKGROUND_COLOR)
        self.resizable(False, False)

        self.player_score = 0
        self.ai_score = 0
        self.current_round = 0
        self.round_history = []
        self.options = ["rock", "paper", "scissors"]

        self.build_interface()

    def build_interface(self):
        tk.Label(self, text="Rock-Paper-Scissors Duel", font=TITLE_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=(20,10))
        self.round_label = tk.Label(self, text=f"Round: {self.current_round}", font=BUTTON_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.round_label.pack(pady=5)

        button_frame = tk.Frame(self, bg=BACKGROUND_COLOR)
        button_frame.pack(pady=15)
        tk.Button(button_frame, text="🪨 ROCK", width=15, height=2, bg=PRIMARY_COLOR, fg="white", font=BUTTON_FONT, command=lambda: self.play_turn("rock")).grid(row=0, column=0, padx=8, pady=5)
        tk.Button(button_frame, text="📄 PAPER", width=15, height=2, bg=PRIMARY_COLOR, fg="white", font=BUTTON_FONT, command=lambda: self.play_turn("paper")).grid(row=0, column=1, padx=8, pady=5)
        tk.Button(button_frame, text="✂️ SCISSORS", width=15, height=2, bg=PRIMARY_COLOR, fg="white", font=BUTTON_FONT, command=lambda: self.play_turn("scissors")).grid(row=0, column=2, padx=8, pady=5)

        self.result_label = tk.Label(self, text="Choose your move!", font=RESULT_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.result_label.pack(pady=20)
        self.score_label = tk.Label(self, text=self.get_score_text(), font=BUTTON_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.score_label.pack(pady=10)

        tk.Label(self, text="Match History:", font=("Verdana", 13, "bold"), bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=10)
        list_frame = tk.Frame(self, bg=BACKGROUND_COLOR)
        list_frame.pack()
        self.scroll = tk.Scrollbar(list_frame)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_box = tk.Listbox(list_frame, width=72, height=12, font=("Courier", 10), yscrollcommand=self.scroll.set)
        self.history_box.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=5)
        self.scroll.config(command=self.history_box.yview)

        tk.Button(self, text="🔁 RESET GAME", width=20, font=BUTTON_FONT, bg=ALERT_COLOR, fg="white", command=self.reset_game).pack(pady=20)

    def get_score_text(self):
        return f"Player: {self.player_score} | AI: {self.ai_score}"

    def play_turn(self, player_choice):
        ai_choice = random.choice(self.options)
        self.current_round += 1
        self.round_label.config(text=f"Round: {self.current_round}")

        winner = self.evaluate_winner(player_choice, ai_choice)

        if winner == "player":
            self.player_score += 1
            message = f"You chose {player_choice.upper()}, AI chose {ai_choice.upper()} → You WIN! 🎯"
        elif winner == "ai":
            self.ai_score += 1
            message = f"You chose {player_choice.upper()}, AI chose {ai_choice.upper()} → You LOSE. 💻"
        else:
            message = f"You chose {player_choice.upper()}, AI chose {ai_choice.upper()} → TIE! 🤝"

        self.result_label.config(text=message)
        self.score_label.config(text=self.get_score_text())

        history_record = f"Round {self.current_round}: Player-{player_choice} | AI-{ai_choice} | Winner: {winner.upper()}"
        self.round_history.append(history_record)
        self.update_history_box()

    def evaluate_winner(self, player, ai):
        if player == ai:
            return "tie"
        elif (player == "rock" and ai == "scissors") or (player == "scissors" and ai == "paper") or (player == "paper" and ai == "rock"):
            return "player"
        else:
            return "ai"

    def update_history_box(self):
        self.history_box.delete(0, tk.END)
        for record in reversed(self.round_history):
            self.history_box.insert(tk.END, record)

    def reset_game(self):
        self.player_score = 0
        self.ai_score = 0
        self.current_round = 0
        self.round_history.clear()
        self.result_label.config(text="Game Reset! Make your move!")
        self.round_label.config(text=f"Round: {self.current_round}")
        self.score_label.config(text=self.get_score_text())
        self.history_box.delete(0, tk.END)
        popup = tk.Toplevel(self)
        popup.title("Reset Complete")
        popup.geometry("250x100")
        popup.config(bg=BACKGROUND_COLOR)
        tk.Label(popup, text="Game has been reset!", font=BUTTON_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=15)
        tk.Button(popup, text="OK", command=popup.destroy).pack(pady=5)

if __name__ == "__main__":
    app = ChoiceBattleGUI()
    app.mainloop()
