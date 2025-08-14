import json
import random
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = "supersecretkey"

def init_game():
    session["Player1_HP"] = 100
    session["Player2_HP"] = 100
    session["Player1_defending"] = False
    session["Player2_defending"] = False
    session["turn"] = 1  # 1 = Player 1, 2 = Player 2
    session["message"] = "Game started! Player 1’s turn."
    session["battle_log"] = []
    session["game_over"] = False


# Helper: handle a player's action
def handle_player_action(player, action):
    opponent = 2 if player == 1 else 1
    defending_key = f"Player{player}_defending"
    opp_defending_key = f"Player{opponent}_defending"
    hp_key = f"Player{opponent}_HP"
    my_hp_key = f"Player{player}_HP"

    if action == "attack":
        damage = random.randint(10, 20)
        if session[opp_defending_key]:
            damage //= 2
            session[opp_defending_key] = False
        session[hp_key] -= damage
        msg = f"🗡 Player {player} attacks Player {opponent} for {damage} damage!"

    elif action == "defend":
        session[defending_key] = True
        msg = f"🛡 Player {player} is defending!"

    elif action == "heal":
        heal = random.randint(15, 25)
        session[my_hp_key] = min(100, session[my_hp_key] + heal)
        msg = f"💖 Player {player} heals for {heal} HP!"

    else:
        msg = "Invalid move."

    session["battle_log"].insert(0, msg)
    session["message"] = msg

# Check if the game has been won
def check_winner():
    if session["Player1_HP"] <= 0 and session["Player2_HP"] <= 0:
        session["Player1_HP"] = max(0, session["Player1_HP"])
        session["Player2_HP"] = max(0, session["Player2_HP"])
        session["message"] = "🤝 It's a draw!"
        session["game_over"] = True
        session["turn"] = 0
        session["battle_log"].insert(0, "🤝 It's a draw!")

    elif session["Player1_HP"] <= 0:
        session["Player1_HP"] = 0
        session["message"] = "💀 Player 2 wins!"
        session["game_over"] = True
        session["turn"] = 0
        session["battle_log"].insert(0, "💀 Player 2 wins!")

    elif session["Player2_HP"] <= 0:
        session["Player2_HP"] = 0
        session["message"] = "🎉 Player 1 wins!"
        session["game_over"] = True
        session["turn"] = 0
        session["battle_log"].insert(0, "🎉 Player 1 wins!")

# Simple bot logic
def computer_choice(p1_hp, p2_hp, p1_def, p2_def):
    if p1_hp < 20:
        return "attack"
    elif p2_hp < 20 and random.random() < 0.5:
        return "heal"
    elif random.random() < 0.7:
        return "attack"
    else:
        return "defend"

@app.route("/choose_mode", methods=["GET", "POST"])
def choose_mode():
    if request.method == "POST":
        session["game_mode"] = request.form.get("mode")
        init_game()
        return redirect(url_for("index"))
    return render_template("choose_mode.html")

# --- Routes ---
@app.route("/")
def index():

    if "game_mode" not in session:
        return redirect(url_for("choose_mode"))


    highscores = load_highscores()["highscores"]
    highscores = sorted(highscores, key=lambda x: x["wins"], reverse=True)[:5]

    return render_template(
        "index.html",
        Player1_HP=session["Player1_HP"],
        Player2_HP=session["Player2_HP"],
        turn=session["turn"],
        message=session["message"],
        battle_log=session["battle_log"],
        game_over=session["game_over"],

        game_mode=session["game_mode"]

    )

@app.route("/action", methods=["POST"])
def action():
    if "battle_log" not in session:
        init_game()

    if session.get("game_over", False):
        return redirect(url_for("index"))

    action = request.form.get("action")
    turn = session["turn"]
    mode = session.get("game_mode", "pvbot")

    # Player 1's turn
    if turn == 1:

        handle_player_action(1, action)
        session["turn"] = 2

        if mode == "pvbot" and not session.get("game_over"):
            bot_move = computer_choice(
                session["Player1_HP"],
                session["Player2_HP"],
                session["Player1_defending"],
                session["Player2_defending"]
            )
            handle_player_action(2, bot_move)
            session["turn"] = 1

    # Player 2's turn in PvP mode
    elif turn == 2 and mode == "pvp":
        handle_player_action(2, action)
        session["turn"] = 1


    check_winner()
    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    init_game()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)