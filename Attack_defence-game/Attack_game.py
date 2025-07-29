import random
import time

def game():
    Player1_HP = 100
    Player2_HP = 100
    Player1_defending = False
    Player2_defending = False
    turn = 1

    # Simplified attack types with damage ranges only
    attacks = {
        "quick": [5, 10],    # [min_damage, max_damage]
        "normal": [10, 20],
        "heavy": [15, 25]
    }
    
    while Player1_HP > 0 and Player2_HP > 0:
        print("\n--------Turn start-----------")
        print("Player1_HP:", Player1_HP)
        print("Player2_HP:", Player2_HP)

        if turn == 1:
            print("Player_1's turn")
            action = input("Choose to attack or defence: ").lower()
            while action not in ["attack", "defence"]:
                print("Invalid input. Please enter 'attack' or 'defence'.")
                action = input("Choose to attack or defence: ").lower()
                
            if action == "attack":
                # Let player choose attack type with damage info instead of descriptions
                print("\nChoose attack type:")
                print(f"1. Quick (damage: 5-10)")
                print(f"2. Normal (damage: 10-20)")
                print(f"3. Heavy (damage: 15-25)")
                choice = input("Enter attack type (1-3): ")
                
                # Simplified attack type selection
                attack_type = "normal"  # Default
                if choice == "1": attack_type = "quick"
                if choice == "3": attack_type = "heavy"
                
                # Simpler damage calculation
                damage = random.randint(attacks[attack_type][0], attacks[attack_type][1])
                
                input("Press ENTER to attack:")
                print(f"Player 1 is attacking Player 2 with a {attack_type} attack")
                print("Generating attack........💥💥")
                time.sleep(1)
                
                if Player2_defending:
                    damage //= 2
                    Player2_defending = False
                    print("Player 2 defended! Damage halved.")
                    
                Player2_HP -= damage
                print(f"Player 1 hit Player 2 for {damage} damage with a {attack_type} attack! 🤺")
            else:
                Player1_defending = True
                print("Player 1 prepares to defend! 🛡️")

            turn = 2

        else:
            print("Player_2's turn")
            action = input("Choose to attack or defence: ").lower()
            while action not in ["attack", "defence"]:
                print("Invalid input. Please enter 'attack' or 'defence'.")
                action = input("Choose to attack or defence: ").lower()
                
            if action == "attack":
                # Let player choose attack type with damage info instead of descriptions
                print("\nChoose attack type:")
                print(f"1. Quick (damage: 5-10)")
                print(f"2. Normal (damage: 10-20)")
                print(f"3. Heavy (damage: 15-25)")
                choice = input("Enter attack type (1-3): ")
                
                # Simplified attack type selection
                attack_type = "normal"  # Default
                if choice == "1": attack_type = "quick"
                if choice == "3": attack_type = "heavy"
                
                # Simpler damage calculation
                damage = random.randint(attacks[attack_type][0], attacks[attack_type][1])
                
                input("Press ENTER to attack:")
                print(f"Player 2 is attacking Player 1 with a {attack_type} attack")
                print("Generating attack........💥💥")
                time.sleep(1)
                
                if Player1_defending:
                    damage //= 2
                    Player1_defending = False
                    print("Player 1 defended! Damage halved.")
                    
                Player1_HP -= damage
                print(f"Player 2 hit Player 1 for {damage} damage with a {attack_type} attack! 🤺")
            else:
                Player2_defending = True
                print("Player 2 prepares to defend! 🛡️")
                
            turn = 1

    print("\n==== GAME OVER ====")
    if Player1_HP <= 0:
        print("Player 2 won the game 🏆")
    else:
        print("Player 1 won the game 🏆")

game()