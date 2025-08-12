
# ⚔️ Attack & Defense – Turn-Based Game

A **Python-based turn-based battle game** with **two modes**:  
1. **Player vs Player (PvP)** – Local multiplayer mode  
2. **Player vs Computer (Bot)** – Battle against an AI opponent  

The **PvP version** is a graphical game using **Pygame**, while the **Bot mode** is a text-based console game.

---

## 📂 Project Structure
```

Attack\_defence-game/
│
├── assets/                 # Game graphics for Pygame version
│   ├── P1\_Shot.png
│   └── P2\_Shot.png
│
├── Attack\_game.py          # Player vs Player (Graphical - Pygame)
├── attack\_with\_bot.py      # Player vs Computer (Console)
└── README.md               # Documentation

````

---

## 🎯 Features

### **PvP (Attack_game.py)** – Graphical Mode
- Built with **Pygame**
- Visual HP bars and battle log
- Multiple move types: Quick, Normal, Heavy, Defend, Heal, Special
- Critical hit chance
- Restart option after a win

### **Bot Mode (attack_with_bot.py)** – Console Mode
- Simple text-based gameplay
- Two actions: **Attack** (10–20 damage) or **Defend** (halve next damage)
- Computer makes strategic decisions based on HP and chance
- Quick to run in any terminal

---

## 🛠 Requirements

### For **PvP (Pygame)**:
- Python 3.x
- Install Pygame:
```bash
pip install pygame
````

### For **Bot Mode**:

* Python 3.x
* No extra libraries required

---

## 🚀 How to Run

### **PvP (Graphical Mode)**

```bash
python Attack_game.py
```

### **Bot Mode (Console)**

```bash
python attack_with_bot.py
```

---

## 🎮 How to Play

### **PvP**

1. Player 1 and Player 2 take turns clicking attack/defend/heal/special buttons.
2. HP bars update in real time.
3. First player to bring the opponent’s HP to 0 wins.

### **Bot Mode**

1. Player 1 types `attack` or `defend` when prompted.
2. Player 2 (the bot) chooses its action automatically.
3. First to reduce opponent’s HP to 0 wins.

---

## 💡 Future Improvements

* Add online multiplayer
* Improve bot AI for more challenge
* More animations and sound effects
* Expand console mode to include PvP
