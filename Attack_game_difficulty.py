import random
import time

def choose_difficulty():
    print("Select Difficulty Level:")
    print("1. Easy 😌")
    print("2. Medium 😐")
    print("3. Hard 😈")
    choice = input("Enter 1, 2, or 3: ").strip()
    while choice not in ["1", "2", "3"]:
        print("Invalid input. Please enter 1, 2, or 3.")
        choice = input("Enter 1, 2, or 3: ").strip()

    if choice == "1":
        return "easy"
    elif choice == "2":
        return "medium"
    else:
        return "hard"

def ai_action(difficulty):
    if difficulty == "easy":
        return random.choices(["attack", "defend"], weights=[0.4, 0.6])[0]
    elif difficulty == "medium":
        return random.choice(["attack", "defend"])
    else:  # hard
        return random.choices(["attack", "defend"], weights=[0.8, 0.2])[0]

def game():
    Player1_HP = 100
    Player2_HP = 100
    Player1_defending = False
    Player2_defending = False
    turn = 1

    difficulty = choose_difficulty()

    while Player1_HP > 0 and Player2_HP > 0:
        print("\n-------- Turn Start --------")
        print(f"Player 1 HP: {Player1_HP}")
        print(f"Player 2 HP: {Player2_HP}")

        if turn == 1:
            print("\n🧍‍♀️ Player 1's Turn")
            action = input("Choose to attack or defend: ").lower().strip()
            while action not in ["attack", "defend"]:
                print("Invalid input. Please enter 'attack' or 'defend'.")
                action = input("Choose to attack or defend: ").lower().strip()

            if action == "attack":
                input("Press ENTER to attack...")
                damage = random.randint(10, 20)
                print("Generating attack........💥💥")
                time.sleep(1)
                if Player2_defending:
                    damage //= 2
                    Player2_defending = False
                    print("🛡️ Player 2 defended! Damage halved.")
                Player2_HP -= damage
                print(f"⚔️ Player 1 attacked Player 2 for {damage} damage!")
            else:
                Player1_defending = True
                print("🛡️ Player 1 is defending this turn.")
            turn = 2

        else:
            print("\n🤖 Player 2's Turn (AI)")
            action = ai_action(difficulty)
            print(f"AI chooses to {action}.")
            time.sleep(1)

            if action == "attack":
                damage = random.randint(10, 20)
                print("Generating attack........💥💥")
                time.sleep(1)
                if Player1_defending:
                    damage //= 2
                    Player1_defending = False
                    print("🛡️ Player 1 defended! Damage halved.")
                Player1_HP -= damage
                print(f"⚔️ Player 2 attacked Player 1 for {damage} damage!")
            else:
                Player2_defending = True
                print("🛡️ Player 2 is defending this turn.")
            turn = 1

    print("\n========== GAME OVER ==========")
    if Player1_HP <= 0:
        print("💀 Player 1 has been defeated.")
        print("🏆 Player 2 (AI) wins!")
    else:
        print("💀 Player 2 has been defeated.")
        print("🏆 Player 1 wins!")

# Run the game
game()
