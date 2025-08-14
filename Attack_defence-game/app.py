import json
import random
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = "supersecretkey"

# --- New User and High Score Management ---
USERS_FILE = "users.json"
HIGHSCORE_FILE = "highscore.json"


def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


def load_highscores():
    try:
        with open(HIGHSCORE_FILE, "r") as f:
            data = json.load(f)
            if isinstance(data, dict) and "highscores" in data:
                return data
            elif isinstance(data, list):
                return {"highscores": data}
            else:
                return {"highscores": []}
    except (FileNotFoundError, json.JSONDecodeError):
        return {"highscores": []}


def save_highscores(highscores_data):
    with open(HIGHSCORE_FILE, "w") as f:
        json.dump(highscores_data, f, indent=4)


# --- Initialize Game State ---
def init_game():
    session["Player1_HP"] = 100
    session["Player2_HP"] = 100
    session["Player1_defending"] = False
    session["Player2_defending"] = False
    session["turn"] = 1  # 1 = Player 1, 2 = Player 2
    session["message"] = "Game started! Player 1’s turn."
    session["battle_log"] = []
    session["game_over"] = False


# --- Routes ---
@app.route("/")
def index():
    if "username" not in session:
        return redirect(url_for("login"))

    required_keys = [
        "Player1_HP", "Player2_HP", "Player1_defending", "Player2_defending",
        "turn", "message", "battle_log", "game_over"
    ]
    if not all(k in session for k in required_keys):
        init_game()

    highscores = load_highscores()["highscores"]
    highscores = sorted(highscores, key=lambda x: x["wins"], reverse=True)[:5]

    return render_template(
        "index.html",
        Player1_HP=session["Player1_HP"],
        Player2_HP=session["Player2_HP"],
        Player1_defending=session["Player1_defending"],
        Player2_defending=session["Player2_defending"],
        turn=session["turn"],
        message=session["message"],
        battle_log=session["battle_log"],
        game_over=session["game_over"],
        username=session["username"],
        highscores=highscores
    )


@app.route("/action", methods=["POST"])
def action():
    if "battle_log" not in session:
        init_game()

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
            msg = f"🗡 {session['username']} attacks Player 2 for {damage} damage!"
        elif action == "defend":
            session["Player1_defending"] = True
            msg = f"🛡 {session['username']} is defending!"
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
            msg = f"🗡 Player 2 attacks {session['username']} for {damage} damage!"
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
        session["message"] = f"🎉 {session['username']} wins!"
        session["game_over"] = True
        session["turn"] = 0
        session["battle_log"].insert(0, f"🎉 {session['username']} wins!")
        # Update high score for the winner
        update_highscores(session["username"])

    return redirect(url_for("index"))


@app.route("/reset")
def reset():
    init_game()
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


# --- New User Authentication Routes ---
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        users = load_users()
        if username in users and users[username]["password"] == password:
            session["username"] = username
            init_game()
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid username or password.")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        users = load_users()
        if username in users:
            return render_template("register.html", error="Username already exists.")
        
        users[username] = {"password": password, "wins": 0}
        save_users(users)
        
        highscores = load_highscores()
        highscores["highscores"].append({"username": username, "wins": 0})
        save_highscores(highscores)

        session["username"] = username
        init_game()
        return redirect(url_for("index"))
    return render_template("register.html")


# --- New High Score Logic ---
def update_highscores(username):
    highscores = load_highscores()
    found = False
    for player in highscores["highscores"]:
        if player["username"] == username:
            player["wins"] += 1
            found = True
            break
    if not found:
        highscores["highscores"].append({"username": username, "wins": 1})
    save_highscores(highscores)


# --- Computer AI logic ---
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