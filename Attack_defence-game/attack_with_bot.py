import tkinter as tk
from tkinter import messagebox
import random
import json
import os

class BattleGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔥 Battle Game GUI By Bhumika Kadbe🔥")
        self.root.geometry("850x650")
        self.root.configure(bg="#f0ead8")  # cream/light beige background

        # Player info and difficulty
        self.difficulty = tk.StringVar(value="Medium")
        self.player_name = tk.StringVar()

        # Load game data (leaderboard and match history) from file
        self.load_game_data()

        self.setup_difficulty_menu()

    def load_game_data(self):
        """Load leaderboard and match history from a JSON file."""
        if os.path.exists("game_data.json"):
            try:
                with open("game_data.json", "r") as f:
                    data = json.load(f)
                    self.leaderboard = data.get("leaderboard", {})
                    self.match_history = data.get("match_history", [])
            except Exception as e:
                print("Failed to load game data:", e)
                self.leaderboard = {}
                self.match_history = []
        else:
            self.leaderboard = {}
            self.match_history = []

    def save_game_data(self):
        """Save leaderboard and match history to a JSON file."""
        try:
            data = {
                "leaderboard": self.leaderboard,
                "match_history": self.match_history
            }
            with open("game_data.json", "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print("Failed to save game data:", e)

    def setup_difficulty_menu(self):
        # Clear all widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Title label
        tk.Label(self.root, text="Enter Your Name:", font=('Arial', 16), bg="#f0ead8").pack(pady=(35, 5))

        entry_name = tk.Entry(self.root, textvariable=self.player_name, font=('Arial', 14), justify='center')
        entry_name.pack(pady=5)
        entry_name.focus_set()

        tk.Label(self.root, text="Select Difficulty Level:", font=('Arial', 16), bg="#f0ead8").pack(pady=15)

        # Difficulty radio buttons with custom styling
        for level in ["Easy", "Medium", "Hard"]:
            tk.Radiobutton(self.root, text=level, variable=self.difficulty, value=level,
                           font=('Arial', 14), bg="#f0ead8", selectcolor='#a5c7d7').pack()

        tk.Button(self.root, text="Start Game", command=self.validate_and_start,
                  font=('Arial', 14, 'bold'), bg="#4caf50", fg="white", activebackground="#45a049").pack(pady=30)

        # Display leaderboard summary at bottom
        self.leaderboard_label = tk.Label(self.root, text=self.get_leaderboard_text(),
                                          font=('Arial', 12, 'italic'), bg="#f0ead8", fg="#333")
        self.leaderboard_label.pack(side="bottom", pady=10)

    def get_leaderboard_text(self):
        if not self.leaderboard:
            return "Leaderboard: No games played yet."
        sorted_leaderboard = sorted(self.leaderboard.items(), key=lambda x: x[1], reverse=True)
        text = "Leaderboard (Wins): " + ', '.join(f"{name}: {wins}" for name, wins in sorted_leaderboard)
        return text

    def validate_and_start(self):
        if not self.player_name.get().strip():
            messagebox.showwarning("Name Required", "Please enter your name before starting the game.")
        else:
            self.start_game()

    def start_game(self):
        # Initialize game variables
        self.Player1_HP = 100
        self.Player2_HP = 100
        self.Player1_defending = False
        self.Player2_defending = False
        self.round = 1
        self.turn = random.choice([1, 2])  # Random start
        self.turns_played = 0
        self.action_log = []
        self.setup_gui()

    def setup_gui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Heading
        header = tk.Label(self.root, text="🔥 Battle Game 🔥", font=("Arial", 22, "bold"),
                          fg="#d84315", bg="#f0ead8")
        header.pack(pady=10)

        # Round and status frame
        self.status_frame = tk.Frame(self.root, bg="#f0ead8")
        self.status_frame.pack(pady=5)

        self.status_label = tk.Label(self.status_frame, text=f"Round {self.round}",
                                     font=("Arial", 18, "bold"), fg="#2e7d32", bg="#f0ead8")
        self.status_label.grid(row=0, column=0, padx=10)

        self.turn_label = tk.Label(self.status_frame, text="", font=("Arial", 16), bg="#f0ead8")
        self.turn_label.grid(row=0, column=1, padx=40)

        self.player_hp_label = tk.Label(self.status_frame, text="", font=("Arial", 14), bg="#f0ead8",
                                        fg="#1a237e")
        self.player_hp_label.grid(row=1, column=0, pady=5)

        self.ai_hp_label = tk.Label(self.status_frame, text="", font=("Arial", 14), bg="#f0ead8",
                                    fg="#b71c1c")
        self.ai_hp_label.grid(row=1, column=1, pady=5)

        # Log box
        self.log_text = tk.Text(self.root, width=90, height=15, state='disabled', bg="#fff3e0",
                                font=('Courier New', 11))
        self.log_text.pack(pady=10)

        # Action buttons frame
        self.action_frame = tk.Frame(self.root, bg="#f0ead8")
        self.action_frame.pack(pady=15)

        self.btn_light = tk.Button(self.action_frame, text="Light Attack 💢", width=15,
                                   command=lambda: self.player_attack('light'), font=('Arial', 12))
        self.btn_light.grid(row=0, column=0, padx=10)

        self.btn_heavy = tk.Button(self.action_frame, text="Heavy Attack 🔥", width=15,
                                   command=lambda: self.player_attack('heavy'), font=('Arial', 12))
        self.btn_heavy.grid(row=0, column=1, padx=10)

        self.btn_special = tk.Button(self.action_frame, text="Special Attack ⚡", width=15,
                                     command=lambda: self.player_attack('special'), font=('Arial', 12))
        self.btn_special.grid(row=0, column=2, padx=10)

        self.btn_defend = tk.Button(self.action_frame, text="Defend 🛡️", width=15,
                                    command=self.player_defend, font=('Arial', 12))
        self.btn_defend.grid(row=0, column=3, padx=10)

        # Bottom utility buttons
        self.utility_frame = tk.Frame(self.root, bg="#f0ead8")
        self.utility_frame.pack(pady=10)

        tk.Button(self.utility_frame, text="Help ℹ️", command=self.show_help,
                  font=('Arial', 12), bg="#29b6f6", fg="white").grid(row=0, column=0, padx=15)
        tk.Button(self.utility_frame, text="Developer Info 👩‍💻", command=self.show_developer_info,
                  font=('Arial', 12), bg="#7b1fa2", fg="white").grid(row=0, column=1, padx=15)
        tk.Button(self.utility_frame, text="Match History 📜", command=self.show_match_history,
                  font=('Arial', 12), bg="#ff7043", fg="white").grid(row=0, column=2, padx=15)
        tk.Button(self.utility_frame, text="Quit 🔵", command=self.quit_game,
                  font=('Arial', 12), bg="#263238", fg="white").grid(row=0, column=3, padx=15)

        self.update_turn_indicator()
        self.update_hp_labels()

        # If AI starts, schedule its move
        if self.turn == 2:
            self.root.after(1200, self.ai_turn)

    def update_turn_indicator(self):
        if self.turn == 1:
            self.turn_label.config(text=f"Your Turn 🔹 [{self.player_name.get()}]", fg="#1565c0")
            self.set_action_buttons_state("normal")
        else:
            self.turn_label.config(text="AI Turn 🔸", fg="#d32f2f")
            self.set_action_buttons_state("disabled")

    def set_action_buttons_state(self, state):
        self.btn_light.config(state=state)
        self.btn_heavy.config(state=state)
        self.btn_special.config(state=state)
        self.btn_defend.config(state=state)

    def show_help(self):
        instructions = (
            "⚠️ If you quit, you will lose the game!\n\n"
            "📝 Game Instructions:\n\n"
            "- Each player starts with 100 HP.\n"
            "- On your turn, choose one of the following actions:\n"
            "  • Light Attack: Small damage, always hits.\n"
            "  • Heavy Attack: Big damage, may miss (70% hit chance).\n"
            "  • Special Attack: Random high damage, risky (60% hit chance).\n"
            "  • Defend: Halves incoming damage on next attack.\n"
            "- AI will automatically take its turn.\n"
            "- First to reduce the opponent's HP to zero wins.\n"
            "- Clicking Quit means you surrender the match.\n\n"
            "Good luck and have fun!"
        )
        messagebox.showinfo("Help - How to Play", instructions)

    def show_developer_info(self):
        dev_info = (
            "👩‍💻 Developer Information:\n\n"
            "Name: Bhumika Rajkumar Kadbe\n"
            "Contact Info: bhumikakadbe@gmail.com\n"
            "GitHub ID: https://github.com/bhumikakadbe\n"
            "LinkedIn: https://www.linkedin.com/in/bhumika-kadbe-20409331b"
        )
        messagebox.showinfo("Developer Info", dev_info)

    def show_match_history(self):
        if not self.match_history:
            msg = "No match history available yet."
        else:
            lines = []
            for i, match in enumerate(self.match_history[-10:], 1):  # Show last 10 matches
                lines.append(f"Match {i}: Winner - {match['winner']}, Rounds - {match['rounds']}")
            msg = "\n".join(lines)
        messagebox.showinfo("Match History", msg)

    def quit_game(self):
        confirm = messagebox.askyesno(
            "Warning - Quit Game",
            "⚠️ Are you sure you want to quit?\nYou will lose the game!"
        )
        if confirm:
            self.log(f"{self.player_name.get()} quit the game. You lose! ❌")
            self.game_over("Player 2 (AI)")

    def update_hp_labels(self):
        self.player_hp_label.config(text=f"{self.player_name.get()} HP: {self.Player1_HP} "
                                         + ("(Defending)" if self.Player1_defending else ""),
                                    fg="#1a237e")
        self.ai_hp_label.config(text=f"Player 2 (AI) HP: {self.Player2_HP} "
                                    + ("(Defending)" if self.Player2_defending else ""),
                                fg="#b71c1c")

    def log(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.insert(tk.END, "-" * 70 + '\n')
        self.log_text.config(state='disabled')
        self.log_text.see(tk.END)

    def player_attack(self, attack_type):
        if self.turn != 1:
            return
        damage = 0
        hit = True
        msg = f"{self.player_name.get()} used {attack_type.capitalize()} Attack! 💥"

        if attack_type == 'light':
            damage = random.randint(8, 12)
        elif attack_type == 'heavy':
            hit = random.random() < 0.7
            damage = random.randint(15, 25) if hit else 0
        elif attack_type == 'special':
            hit = random.random() < 0.6
            damage = random.randint(10, 35) if hit else 0

        if not hit:
            msg += " But you missed!"
        else:
            if self.Player2_defending:
                damage //= 2
                self.Player2_defending = False
                msg += " Player 2 defended! Damage halved."
            self.Player2_HP = max(0, self.Player2_HP - damage)
            msg += f" You dealt {damage} damage."

        self.log(msg)
        self.update_hp_labels()
        self.end_turn()

    def player_defend(self):
        if self.turn != 1:
            return
        if self.Player1_defending:
            self.log("You're already defending this turn!")
            return
        self.Player1_defending = True
        self.log(f"{self.player_name.get()} is defending this turn! 🛡️")
        self.update_hp_labels()
        self.end_turn()

    def ai_turn(self):
        if self.turn != 2:
            return
        action = self.computer_choice()

        if action == 'attack':
            self.ai_attack()
        else:
            self.ai_defend()

        self.update_hp_labels()
        self.end_turn()

    def ai_attack(self):
        level = self.difficulty.get()

        # AI chooses attack based on difficulty and situation
        if level == "Easy":
            attack_type = random.choice(['light', 'heavy'])  # No special attacks on easy
        elif level == "Medium":
            attack_type = random.choices(['light', 'heavy', 'special'], weights=[0.5, 0.3, 0.2])[0]
        else:  # Hard
            if self.Player1_HP < 40:
                attack_type = random.choices(['heavy', 'special'], weights=[0.6, 0.4])[0]
            else:
                attack_type = random.choices(['light', 'heavy', 'special'], weights=[0.3, 0.4, 0.3])[0]

        damage = 0
        hit = True
        msg = f"Player 2 used {attack_type.capitalize()} Attack! 💥"

        if attack_type == 'light':
            damage = random.randint(8, 12)
        elif attack_type == 'heavy':
            hit = random.random() < 0.7
            damage = random.randint(15, 25) if hit else 0
        elif attack_type == 'special':
            hit = random.random() < 0.6
            damage = random.randint(10, 35) if hit else 0

        if not hit:
            msg += " But it missed!"
        else:
            if self.Player1_defending:
                damage //= 2
                self.Player1_defending = False
                msg += f" {self.player_name.get()} defended! Damage halved."
            self.Player1_HP = max(0, self.Player1_HP - damage)
            msg += f" Player 2 dealt {damage} damage."

        self.log(msg)

    def ai_defend(self):
        self.Player2_defending = True
        self.log("Player 2 is defending this turn! 🛡️")

    def computer_choice(self):
        level = self.difficulty.get()

        if level == "Easy":
            # 70% attack, 30% defend, no HP checks
            return 'attack' if random.random() < 0.7 else 'defend'

        elif level == "Medium":
            if self.Player2_HP < 40:
                return 'defend' if random.random() < 0.6 else 'attack'
            elif self.Player1_defending:
                return 'defend' if random.random() < 0.5 else 'attack'
            else:
                return 'attack' if random.random() < 0.75 else 'defend'

        else:  # Hard
            if self.Player2_HP < 30:
                if self.Player1_HP < 25:
                    return 'attack'  # Aggressive finish
                return 'defend' if random.random() < 0.7 else 'attack'
            if self.Player1_defending:
                return 'defend' if random.random() < 0.6 else 'attack'
            return 'attack' if random.random() < 0.85 else 'defend'

    def end_turn(self):
        winner = self.check_winner()
        if winner:
            self.game_over(winner)
            return

        self.turns_played += 1
        if self.turns_played >= 2:
            self.round += 1
            self.turns_played = 0

        if self.turn == 1:
            self.turn = 2
            self.update_gui()
            self.set_action_buttons_state("disabled")
            self.root.after(1200, self.ai_turn)
        else:
            self.turn = 1
            self.update_gui()
            self.set_action_buttons_state("normal")

    def update_gui(self):
        self.status_label.config(text=f"Round {self.round}")
        self.update_hp_labels()
        self.update_turn_indicator()

    def check_winner(self):
        if self.Player1_HP <= 0:
            return "Player 2 (AI)"
        elif self.Player2_HP <= 0:
            return f"{self.player_name.get()} (You)"
        return None

    def game_over(self, winner):
        self.update_gui()
        self.log(f"🏆 {winner} is the winner! Congratulations! 🏆")

        player_won = "AI" not in winner
        player = self.player_name.get()
        if player_won:
            self.leaderboard[player] = self.leaderboard.get(player, 0) + 1
        else:
            self.leaderboard["AI"] = self.leaderboard.get("AI", 0) + 1

        self.match_history.append({"winner": winner, "rounds": self.round})

        # Save leaderboard and match history persistently
        self.save_game_data()

        if hasattr(self, 'leaderboard_label') and self.leaderboard_label.winfo_exists():
            self.leaderboard_label.config(text=self.get_leaderboard_text())

        self.set_action_buttons_state("disabled")

        # Clear leaderboard and history after 5 matches
        if len(self.match_history) >= 5:
            messagebox.showinfo(
                "Leaderboard Reset",
                "Leaderboard and Match History have been cleared after 5 matches."
            )
            self.leaderboard.clear()
            self.match_history.clear()
            self.save_game_data()
            if hasattr(self, 'leaderboard_label') and self.leaderboard_label.winfo_exists():
                self.leaderboard_label.config(text=self.get_leaderboard_text())

        if player_won:
            msg = f"🎉 Congratulations, {player}! You won the battle! 🎉\n\nTotal rounds played: {self.round}\n\nDo you want to play again?"
        else:
            msg = f"Game Over!\n\nWinner: {winner}\nTotal rounds played: {self.round}\n\nDo you want to try again?"

        play_again = messagebox.askyesno("Game Over", msg)

        if play_again:
            self.setup_difficulty_menu()
        else:
            self.root.destroy()

def main():
    root = tk.Tk()
    game = BattleGameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()