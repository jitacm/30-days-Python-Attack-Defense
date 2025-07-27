import random
import time

def game():
    Player1_HP = 100
    Player2_HP = 100
    Player1_defending = False
    Player2_defending = False
    turn = 1

    while Player1_HP > 0 and Player2_HP > 0:
        print("\n--------Turn start-----------")
        print("Player1_HP>0 HP", Player1_HP)
        print("Player2_HP>0 HP", Player2_HP)

        if turn == 1:
            print("Player_1's turn")
            action = input("choose to attack or defence:").lower()
            if action != "attack" and action != "defence":
                print("Invalid input. Please enter 'attack' or 'defence'.")
                action = input("choose to attack or defence:").lower() # Ask again if invalid
                while action != "attack" and action != "defence": #Loop if keeps getting invalid input
                    print("Invalid input. Please enter 'attack' or 'defence'.")
                    action = input("choose to attack or defence:").lower()
            if action == "attack":
                input("Press ENTER to attack:")
                damage = random.randint(10, 20)  # Random between 10 to 20
                print("Genrating attack........💥💥")
                time.sleep(2)
                if Player2_defending == True:
                    damage = damage // 2
                    Player2_defending = False
                    print("Player 2 defended! Damage halved.")  # Defending message
                Player2_HP = Player2_HP - damage
                print("player 1 has attacked Player 2 for", damage, "damage!!!!!!🤺🤺🤺🤺")
            else:
                Player1_defending = True

            turn = 2

        else:
            print("Player_2's turn")
            action = input("choose to attack or defence:").lower()
            if action != "attack" and action != "defence":
                print("Invalid input. Please enter 'attack' or 'defence'.")
                action = input("choose to attack or defence:").lower() # Ask again if invalid
                while action != "attack" and action != "defence": #Loop if keeps getting invalid input
                    print("Invalid input. Please enter 'attack' or 'defence'.")
                    action = input("choose to attack or defence:").lower()
            if action == "attack":
                input("Press ENTER to attack:")
                damage = random.randint(30, 40)  # Random between 30 to 40
                print("Genrating attack........💥💥")
                time.sleep(2)
                if Player1_defending == True:
                    damage = damage // 2
                    Player1_defending = False
                    print("Player 1 defended! Damage halved.")  # Defending message
                Player1_HP = Player1_HP - damage
                print("player 2 has attacked Player 1 for", damage, "damage!!!!!!🤺🤺🤺🤺")
            else:
                Player1_defending = True
            turn = 1

    if Player1_HP <= 0:
        print("Player 2 won the game 🏆🏆🏆🏆")
    else:
        print("Player 1 won the game 🏆🏆🏆🏆")

game()