import tkinter as tk
from tkinter import messagebox
import random
import json
import os


class BattleGameGUI:
    DATA_FILE = "game_data.json"
    SAVE_FILE = "savegame.json"

    def __init__(self, root):
        self.root = root
        self.root.title("🔥 Battle Game GUI by Bhumika Kadbe 🔥")
        self.root.geometry("950x700")
        self.root.configure(bg="#f0ead8")

        # Player info and game state
        self.player1_name = None
        self.player2_name = None  # None means AI player
        self.difficulty = tk.StringVar(value="Medium")

        self.Player1_HP = 100
        self.Player2_HP = 100
        self.Player1_defending = False
        self.Player2_defending = False

        self.round = 1
        self.turn = 1  # 1 or 2 indicates current turn
        self.turns_played = 0

        self.multiplayer = False  # True if two human players
        self.action_log = []

        # Persistent data
        self.leaderboard = {}
        self.match_history = []
        self.load_game_data()

        self.setup_main_menu()

    # Persistence methods
    def load_game_data(self):
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, "r") as f:
                    data = json.load(f)
                    self.leaderboard = data.get("leaderboard", {})
                    self.match_history = data.get("match_history", [])
            except Exception as e:
                print(f"Failed to load game data: {e}")
                self.leaderboard = {}
                self.match_history = []
        else:
            self.leaderboard = {}
            self.match_history = []

    def save_game_data(self):
        try:
            with open(self.DATA_FILE, "w") as f:
                json.dump({"leaderboard": self.leaderboard, "match_history": self.match_history}, f, indent=4)
        except Exception as e:
            print(f"Failed to save game data: {e}")

    def save_game_state(self):
        state = {
            "Player1_HP": self.Player1_HP,
            "Player2_HP": self.Player2_HP,
            "Player1_defending": self.Player1_defending,
            "Player2_defending": self.Player2_defending,
            "round": self.round,
            "turn": self.turn,
            "turns_played": self.turns_played,
            "multiplayer": self.multiplayer,
            "player1_name": self.player1_name,
            "player2_name": self.player2_name,
            "difficulty": self.difficulty.get(),
            "action_log": self.action_log
        }
        try:
            with open(self.SAVE_FILE, "w") as f:
                json.dump(state, f, indent=4)
            messagebox.showinfo("Save Game", "Game saved successfully.")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save game: {e}")

    def load_game_state(self):
        if os.path.exists(self.SAVE_FILE):
            try:
                with open(self.SAVE_FILE, "r") as f:
                    state = json.load(f)
                # Basic validation
                req_keys = ["Player1_HP", "Player2_HP", "Player1_defending", "Player2_defending",
                            "round", "turn", "turns_played", "multiplayer", "player1_name", "player2_name", "difficulty"]
                if not all(k in state for k in req_keys):
                    raise ValueError("Invalid save game data")

                self.Player1_HP = state["Player1_HP"]
                self.Player2_HP = state["Player2_HP"]
                self.Player1_defending = state["Player1_defending"]
                self.Player2_defending = state["Player2_defending"]
                self.round = state["round"]
                self.turn = state["turn"]
                self.turns_played = state["turns_played"]
                self.multiplayer = state["multiplayer"]
                self.player1_name = state["player1_name"]
                self.player2_name = state["player2_name"]
                self.difficulty.set(state["difficulty"])
                self.action_log = state.get("action_log", [])
                self.setup_gui()

                self.log_text.config(state='normal')
                self.log_text.delete(1.0, tk.END)
                for entry in self.action_log:
                    self.log_text.insert(tk.END, entry + "\n" + ("-" * 70) + "\n")
                self.log_text.config(state='disabled')

                messagebox.showinfo("Load Game", "Game loaded successfully.")
            except Exception as e:
                messagebox.showerror("Load Error", f"Failed to load saved game: {e}")
        else:
            messagebox.showinfo("Load Game", "No saved game to load.")

    def delete_save_file(self):
        if os.path.exists(self.SAVE_FILE):
            os.remove(self.SAVE_FILE)
            messagebox.showinfo("Delete Save", "Saved game deleted.")
        else:
            messagebox.showinfo("Delete Save", "No saved game found.")

    # ========== UI Screens ========== #

    def setup_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Enter Player 1 Name:", font=('Arial', 16), bg="#f0ead8").pack(pady=(20, 5))
        self.entry_p1_name = tk.Entry(self.root, font=('Arial', 14), justify='center')
        self.entry_p1_name.pack(pady=5)
        self.entry_p1_name.focus_set()

        tk.Label(self.root, text="Enter Player 2 Name (leave blank for AI):", font=('Arial', 16), bg="#f0ead8").pack(pady=(20, 5))
        self.entry_p2_name = tk.Entry(self.root, font=('Arial', 14), justify='center')
        self.entry_p2_name.pack(pady=5)

        tk.Label(self.root, text="Select AI Difficulty (if Player 2 is AI):", font=('Arial', 16), bg="#f0ead8").pack(pady=15)
        self.difficulty = tk.StringVar(value="Medium")
        for level in ["Easy", "Medium", "Hard"]:
            tk.Radiobutton(self.root, text=level, variable=self.difficulty, value=level,
                           font=('Arial', 14), bg="#f0ead8", selectcolor='#a5c7d7').pack()

        tk.Button(self.root, text="Start Game", command=self.validate_and_start,
                  font=('Arial', 14, 'bold'), bg="#4caf50", fg="white", activebackground="#45a049").pack(pady=30)

        frame_adv = tk.Frame(self.root, bg="#f0ead8")
        frame_adv.pack(pady=5)
        tk.Button(frame_adv, text="Load Game", command=self.load_game_state,
                  font=('Arial', 12), bg="#2196f3", fg="white").grid(row=0, column=0, padx=10)
        tk.Button(frame_adv, text="Delete Saved Game", command=self.delete_save_file,
                  font=('Arial', 12), bg="#d32f2f", fg="white").grid(row=0, column=1, padx=10)

        self.leaderboard_label = tk.Label(self.root, text=self.get_leaderboard_text(),
                                          font=('Arial', 12, 'italic'), bg="#f0ead8", fg="#333")
        self.leaderboard_label.pack(side="bottom", pady=10)

    def get_leaderboard_text(self):
        if not self.leaderboard:
            return "Leaderboard: No games played yet."
        sorted_board = sorted(self.leaderboard.items(), key=lambda i: i[1], reverse=True)
        return "Leaderboard (Wins): " + ", ".join(f"{name}: {wins}" for name, wins in sorted_board)

    def validate_and_start(self):
        p1 = self.entry_p1_name.get().strip()
        if not p1:
            messagebox.showwarning("Input needed", "Please enter Player 1's name.")
            return
        p2 = self.entry_p2_name.get().strip()
        self.player1_name = p1
        self.player2_name = p2 if p2 else None
        self.multiplayer = True if p2 else False
        self.start_game()

    # ========== Game Setup ========== #

    def start_game(self):
        self.Player1_HP = 100
        self.Player2_HP = 100
        self.Player1_defending = False
        self.Player2_defending = False
        self.round = 1
        self.turn = 1
        self.turns_played = 0
        self.action_log = []
        self.setup_gui()

    # ========== Game UI ========== #

    def setup_gui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        header = tk.Label(self.root, text="🔥 Battle Game 🔥", font=("Arial", 24, "bold"), fg="#d84315", bg="#f0ead8")
        header.pack(pady=10)

        self.status_frame = tk.Frame(self.root, bg="#f0ead8")
        self.status_frame.pack(pady=5)

        self.status_label = tk.Label(self.status_frame, text=f"Round {self.round}", font=("Arial", 18, "bold"),
                                     fg="#2e7d32", bg="#f0ead8")
        self.status_label.grid(row=0, column=0, padx=10)

        self.turn_label = tk.Label(self.status_frame, text="", font=("Arial", 16), bg="#f0ead8")
        self.turn_label.grid(row=0, column=1, padx=40)

        self.player1_hp_label = tk.Label(self.status_frame, text="", font=("Arial", 16, "bold"),
                                         bg="#f0ead8", fg="#1a237e")
        self.player1_hp_label.grid(row=1, column=0, pady=5)

        self.player2_hp_label = tk.Label(self.status_frame, text="", font=("Arial", 16, "bold"),
                                         bg="#f0ead8", fg="#b71c1c")
        self.player2_hp_label.grid(row=1, column=1, pady=5)

        self.log_text = tk.Text(self.root, width=95, height=15, state='disabled', bg="#fff3e0", font=('Courier New', 11))
        self.log_text.pack(pady=10)

        self.action_frame = tk.Frame(self.root, bg="#f0ead8")
        self.action_frame.pack(pady=10)

        self.btn_light = tk.Button(self.action_frame, text="Light Attack 💢", width=16,
                                   command=lambda: self.player_action('light'), font=('Arial', 12))
        self.btn_light.grid(row=0, column=0, padx=10, pady=5)
        self.btn_heavy = tk.Button(self.action_frame, text="Heavy Attack 🔥", width=16,
                                   command=lambda: self.player_action('heavy'), font=('Arial', 12))
        self.btn_heavy.grid(row=0, column=1, padx=10, pady=5)
        self.btn_special = tk.Button(self.action_frame, text="Special Attack ⚡", width=16,
                                     command=lambda: self.player_action('special'), font=('Arial', 12))
        self.btn_special.grid(row=0, column=2, padx=10, pady=5)

        self.btn_quick = tk.Button(self.action_frame, text="Quick Strike ⚡", width=16,
                                   command=lambda: self.player_action('quick_strike'), font=('Arial', 12))
        self.btn_quick.grid(row=1, column=0, padx=10, pady=5)
        self.btn_heal = tk.Button(self.action_frame, text="Heal 💖", width=16,
                                  command=lambda: self.player_action('heal'), font=('Arial', 12))
        self.btn_heal.grid(row=1, column=1, padx=10, pady=5)
        self.btn_defend = tk.Button(self.action_frame, text="Defend 🛡️", width=16,
                                    command=lambda: self.player_action('defend'), font=('Arial', 12))
        self.btn_defend.grid(row=1, column=2, padx=10, pady=5)

        self.utility_frame = tk.Frame(self.root, bg="#f0ead8")
        self.utility_frame.pack(pady=10)

        tk.Button(self.utility_frame, text="Help ℹ️", font=('Arial', 12), bg="#29b6f6", fg="white",
                  command=self.show_help).grid(row=0, column=0, padx=10)
        tk.Button(self.utility_frame, text="Developer Info 👩‍💻", font=('Arial', 12), bg="#7b1fa2", fg="white",
                  command=self.show_developer_info).grid(row=0, column=1, padx=10)
        tk.Button(self.utility_frame, text="Match History 📜", font=('Arial', 12), bg="#ff7043", fg="white",
                  command=self.show_match_history).grid(row=0, column=2, padx=10)
        tk.Button(self.utility_frame, text="Save Game 💾", font=('Arial', 12), bg="#009688", fg="white",
                  command=self.save_game_state).grid(row=0, column=3, padx=10)
        tk.Button(self.utility_frame, text="Quit 🔵", font=('Arial', 12), bg="#263238", fg="white",
                  command=self.quit_game).grid(row=0, column=4, padx=10)

        self.update_gui()

        if not self.multiplayer and self.player2_name is None:
            self.set_action_buttons_state("disabled")
            self.root.after(1200, self.ai_turn)
        else:
            self.set_action_buttons_state("normal")

    def update_gui(self):
        self.status_label.config(text=f"Round {self.round}")

        p1_name = self.player1_name or "Player 1"
        p2_name = self.player2_name or "Player 2 (AI)"

        self.player1_hp_label.config(text=f"{p1_name} HP: {self.Player1_HP} " + ("(Defending)" if self.Player1_defending else ""))
        self.player2_hp_label.config(text=f"{p2_name} HP: {self.Player2_HP} " + ("(Defending)" if self.Player2_defending else ""))

        if self.turn == 1:
            self.turn_label.config(text=f"{p1_name}'s Turn 🔹", fg="#1565c0")
        else:
            self.turn_label.config(text=f"{p2_name}'s Turn 🔸", fg="#d32f2f")

    def set_action_buttons_state(self, state):
        self.btn_light.config(state=state)
        self.btn_heavy.config(state=state)
        self.btn_special.config(state=state)
        self.btn_quick.config(state=state)
        self.btn_heal.config(state=state)
        self.btn_defend.config(state=state)

    # ========== Game Logic ========== #

    def player_action(self, action_type):
        if self.turn == 1 or (self.turn == 2 and self.multiplayer and self.player2_name):
            self.process_move(self.turn, action_type)

    def process_move(self, player, action_type):
        attacker_name = self.player1_name if player == 1 else (self.player2_name or "Player 2 (AI)")
        defender_name = self.player2_name or "Player 2 (AI)" if player == 1 else self.player1_name or "Player 1"

        if action_type == "defend":
            if player == 1:
                if self.Player1_defending:
                    self.log(f"{attacker_name} is already defending!")
                    return
                self.Player1_defending = True
            else:
                if self.Player2_defending:
                    self.log(f"{attacker_name} is already defending!")
                    return
                self.Player2_defending = True
            self.log(f"{attacker_name} is defending this turn! 🛡️")

        elif action_type == "heal":
            healed = random.randint(15, 25)
            if player == 1:
                self.Player1_HP = min(100, self.Player1_HP + healed)
            else:
                self.Player2_HP = min(100, self.Player2_HP + healed)
            self.log(f"{attacker_name} healed for {healed} HP! 💖")

        else:
            damage, hit = self.calculate_damage(action_type)

            if not hit:
                self.log(f"{attacker_name} tried {action_type.replace('_', ' ').title()} but missed! ❌")
            else:
                if player == 1 and self.Player2_defending:
                    damage //= 2
                    self.Player2_defending = False
                    self.log(f"{defender_name} defended and reduced damage! 🛡️")
                elif player == 2 and self.Player1_defending:
                    damage //= 2
                    self.Player1_defending = False
                    self.log(f"{defender_name} defended and reduced damage! 🛡️")

                if player == 1:
                    self.Player2_HP = max(0, self.Player2_HP - damage)
                else:
                    self.Player1_HP = max(0, self.Player1_HP - damage)

                self.log(f"{attacker_name} used {action_type.replace('_', ' ').title()} and dealt {damage} damage! 💥")

        self.update_hp_labels()
        self.end_turn()

    def calculate_damage(self, attack_type):
        damage = 0
        hit = True
        if attack_type == 'light':
            damage = random.randint(8, 12)
        elif attack_type == 'heavy':
            hit = random.random() < 0.7
            damage = random.randint(15, 25) if hit else 0
        elif attack_type == 'special':
            hit = random.random() < 0.6
            damage = random.randint(10, 35) if hit else 0
        elif attack_type == 'quick_strike':
            damage = random.randint(5, 10)
        else:
            hit = False
        return damage, hit

    def ai_turn(self):
        if not self.multiplayer and self.turn == 2 and self.player2_name is None:
            action = self.ai_decision()
            self.player_action(action)

    def ai_decision(self):
        level = self.difficulty.get()
        if self.Player2_HP < 30 and random.random() < 0.7:
            return 'defend'
        if level == "Easy":
            return 'attack' if random.random() < 0.7 else 'defend'
        elif level == "Medium":
            if self.Player1_HP < 40 and random.random() < 0.5:
                return 'special'
            elif random.random() < 0.6:
                return 'attack'
            else:
                return 'defend'
        else:
            choices = ['light', 'heavy', 'special', 'quick_strike', 'defend']
            weights = [0.1, 0.4, 0.3, 0.1, 0.1]
            if self.Player1_defending:
                weights[2] = 0.05
                weights[0] += 0.05
                weights[3] += 0.1
            choice = random.choices(choices, weights=weights)[0]
            if choice == 'defend':
                return 'defend'
            else:
                return choice

    def update_hp_labels(self):
        p1_name = self.player1_name or "Player 1"
        p2_name = self.player2_name or "Player 2 (AI)"
        self.player1_hp_label.config(text=f"{p1_name} HP: {self.Player1_HP} " + ("(Defending)" if self.Player1_defending else ""))
        self.player2_hp_label.config(text=f"{p2_name} HP: {self.Player2_HP} " + ("(Defending)" if self.Player2_defending else ""))

    def log(self, message):
        self.action_log.append(message)
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n" + ("-" * 70) + "\n")
        self.log_text.config(state='disabled')
        self.log_text.see(tk.END)

    def end_turn(self):
        winner = self.check_winner()
        if winner:
            self.game_over(winner)
            return
        self.turns_played += 1
        if self.turns_played >= 2:
            self.round += 1
            self.turns_played = 0
        self.turn = 2 if self.turn == 1 else 1
        self.update_gui()
        if self.turn == 1 or (self.multiplayer and self.turn == 2):
            self.set_action_buttons_state("normal")
        else:
            self.set_action_buttons_state("disabled")
            self.root.after(1200, self.ai_turn)

    def check_winner(self):
        if self.Player1_HP <= 0:
            return self.player2_name or "Player 2 (AI)"
        elif self.Player2_HP <= 0:
            return self.player1_name
        return None

    def game_over(self, winner):
        self.update_gui()
        self.set_action_buttons_state("disabled")
        self.log(f"🏆 {winner} wins the battle! Congratulations! 🏆")
        self.leaderboard[winner] = self.leaderboard.get(winner, 0) + 1
        self.match_history.append({"winner": winner, "rounds": self.round})
        self.save_game_data()

        if len(self.match_history) >= 5:
            messagebox.showinfo("Leaderboard Reset", "Leaderboard and match history cleared after 5 matches.")
            self.leaderboard.clear()
            self.match_history.clear()
            self.save_game_data()

        if hasattr(self, 'leaderboard_label') and self.leaderboard_label.winfo_exists():
            self.leaderboard_label.config(text=self.get_leaderboard_text())

        if winner == self.player1_name:
            play_again = messagebox.askyesno("You Won!",
                                             f"🎉 Congratulations {winner}! You won in {self.round} rounds!\nPlay again?")
        else:
            play_again = messagebox.askyesno("Game Over",
                                             f"Game Over!\nWinner: {winner}\nRounds: {self.round}\nTry again?")

        if play_again:
            self.setup_main_menu()
        else:
            self.root.destroy()

    # ========== Utility dialogs ========== #

    def show_help(self):
        instructions = (
            "⚠️ Quitting will forfeit the game.\n\n"
            "Moves:\n"
            "• Light Attack: Moderate damage, guaranteed hit.\n"
            "• Heavy Attack: Higher damage, 70% chance.\n"
            "• Special Attack: Random high damage, 60% chance.\n"
            "• Quick Strike: Lower damage, guaranteed hit.\n"
            "• Heal: Restore HP.\n"
            "• Defend: Halve next taken damage.\n\n"
            "Two-player mode supports 2 human players on same PC.\n"
            "If Player 2 is blank, AI will play.\n"
            "Win by reducing opponent HP to zero."
        )
        messagebox.showinfo("Help - How to Play", instructions)

    def show_developer_info(self):
        info = (
            "👩‍💻 Developer: Bhumika Rajkumar Kadbe\n"
            "Email: bhumikakadbe@gmail.com\n"
            "GitHub: https://github.com/bhumikakadbe\n"
            "LinkedIn: https://www.linkedin.com/in/bhumika-kadbe-20409331b"
        )
        messagebox.showinfo("Developer Info", info)

    def show_match_history(self):
        if not self.match_history:
            messagebox.showinfo("Match History", "No match history yet.")
            return
        lines = [f"Match {i + 1}: Winner - {m['winner']}, Rounds - {m['rounds']}" for i, m in enumerate(self.match_history[-10:])]
        messagebox.showinfo("Match History (Last 10)", "\n".join(lines))

    def quit_game(self):
        if messagebox.askyesno("Quit", "⚠️ Are you sure you want to quit? You will forfeit."):
            self.root.destroy()


def main():
    root = tk.Tk()
    BattleGameGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
