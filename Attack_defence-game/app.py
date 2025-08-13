from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"


# Initialize game state
def init_game():
    session["Player1_HP"] = 100
    session["Player2_HP"] = 100
    session["Player1_defending"] = False
    session["Player2_defending"] = False
    session["turn"] = 1  # 1 = Player 1, 2 = Player 2
    session["message"] = "Game started! Player 1’s turn."
    session["battle_log"] = []
    session["game_over"] = False  # New key to track game end


@app.route("/")
def index():
    # Ensure session is initialized
    required_keys = [
        "Player1_HP", "Player2_HP", "Player1_defending", "Player2_defending",
        "turn", "message", "battle_log", "game_over"
    ]
    if not all(k in session for k in required_keys):
        init_game()

    return render_template(
        "index.html",
        Player1_HP=session["Player1_HP"],
        Player2_HP=session["Player2_HP"],
        Player1_defending=session["Player1_defending"],
        Player2_defending=session["Player2_defending"],
        turn=session["turn"],
        message=session["message"],
        battle_log=session["battle_log"],
        game_over=session["game_over"]
    )


@app.route("/action", methods=["POST"])
def action():
    # Safety check if session somehow lost its keys
    if "battle_log" not in session:
        init_game()

    # Stop moves if game already ended
    if session.get("game_over", False):
        return redirect(url_for("index"))

    action = request.form.get("action")
    turn = session["turn"]

    # PLAYER 1 TURN
    if turn == 1:
        if action == "attack":
            damage = random.randint(10, 20)
            if session["Player2_defending"]:
                damage //= 2
                session["Player2_defending"] = False
            session["Player2_HP"] -= damage
            msg = f"🗡 Player 1 attacks Player 2 for {damage} damage!"
        elif action == "defend":
            session["Player1_defending"] = True
            msg = "🛡 Player 1 is defending!"
        else:
            msg = "Invalid move."

        session["battle_log"].insert(0, msg)
        session["turn"] = 2
        session["message"] = msg

    # PLAYER 2 TURN (Computer)
    elif turn == 2:
        comp_action = computer_choice(
            session["Player1_HP"],
            session["Player2_HP"],
            session["Player1_defending"],
            session["Player2_defending"]
        )

        if comp_action == "attack":
            damage = random.randint(10, 20)
            if session["Player1_defending"]:
                damage //= 2
                session["Player1_defending"] = False
            session["Player1_HP"] -= damage
            msg = f"🗡 Player 2 attacks Player 1 for {damage} damage!"
        elif comp_action == "defend":
            session["Player2_defending"] = True
            msg = "🛡 Player 2 is defending!"
        else:
            msg = "Invalid move."

        session["battle_log"].insert(0, msg)
        session["turn"] = 1
        session["message"] = msg

    # CHECK WIN CONDITION
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

    return redirect(url_for("index"))


@app.route("/reset")
def reset():
    init_game()
    return redirect(url_for("index"))


# Computer AI logic
def computer_choice(p1_hp, p2_hp, p1_def, p2_def):
    if p1_hp < 20:
        return "attack"
    elif p2_hp < 20 and random.random() < 0.5:
        return "defend"
    elif random.random() < 0.7:
        return "attack"
    else:
        return "defend"


if __name__ == "__main__":
    app.run(debug=True)
