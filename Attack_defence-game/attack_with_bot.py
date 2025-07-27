import random
import time

def game():
    Player1_HP = 100
    Player2_HP = 100
    Player1_defending = False
    Player2_defending = False
    turn = 1

    while Player1_HP > 0 and Player2_HP > 0:
        print("\n------Turn Start-------")
        print('Player 1 HP:', Player1_HP)
        print('Player 2 HP:', Player2_HP)

        if turn == 1:
            print("Player 1's Turn")
            action = input("Choose attack or defend: ").strip().lower()

            if action == 'attack':
                damage = random.randint(10, 20)
                print("Generating attack...💥")
                time.sleep(1)
                
                if Player2_defending:
                    damage //= 2  # Halve the damage if Player 2 was defending
                    Player2_defending = False
                
                Player2_HP -= damage
                print(f"Player 1 has attacked Player 2 for {damage} damage! ⚔️")

            elif action == 'defend':
                Player1_defending = True
                print("Player 1 is defending! 🛡️")
            
            turn = 2  # Switch turn to Player 2

        else:
            print("Player 2's Turn")
            action = computer_choice(Player1_HP, Player2_HP, Player1_defending, Player2_defending)
            print(f"Player 2 chooses to {action}")

            if action == 'attack':
                damage = random.randint(30, 40)
                print("Generating attack...💥")
                time.sleep(1)

                if Player1_defending:
                    damage //= 2  # Halve the damage if Player 1 was defending
                    Player1_defending = False
                
                Player1_HP -= damage
                print(f"Player 2 has attacked Player 1 for {damage} damage! ⚔️")

            elif action == 'defend':
                Player2_defending = True
                print("Player 2 is defending! 🛡️")
            
            turn = 1  # Switch turn to Player 1

    # Determine winner
    if Player1_HP > 0:
        print('Player 1 is the winner! 🏆')
    else:
        print('Player 2 is the winner! 🏆')

def computer_choice(Player1_HP, Player2_HP, Player1_defending, Player2_defending):
  
    if Player1_defending:
        return 'attack'
    elif Player2_defending:
        return 'attack'
    elif Player1_HP < 30:
        return 'attack'
    elif Player2_HP < 20:
        return 'defend'
    elif random.random() < 0.7:
        return 'attack'
    return 'defend'

game()
