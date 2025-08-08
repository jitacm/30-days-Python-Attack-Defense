import pygame
import random
import sys
import os

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Screen setup
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("⚔️ Turn-Based Battle Game")

# Load assets
BASE_PATH = r"Attack_defence-game\assets"
PLAYER1_IMG = pygame.image.load(os.path.join(BASE_PATH, "P1_Shot.png"))
PLAYER2_IMG = pygame.image.load(os.path.join(BASE_PATH, "P2_Shot.png"))

# Resize images
PLAYER1_IMG = pygame.transform.scale(PLAYER1_IMG, (150, 150))
PLAYER2_IMG = pygame.transform.scale(PLAYER2_IMG, (150, 150))

# Colors and font
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)
FONT = pygame.font.SysFont('Arial', 24)

# Attack types
ATTACK_TYPES = {
    "quick": (5, 10),
    "normal": (10, 20),
    "heavy": (15, 25)
}

# Game state
def reset_game():
    return {
        "p1_hp": 100,
        "p2_hp": 100,
        "p1_def": False,
        "p2_def": False,
        "p1_special": False,
        "p2_special": False,
        "turn": 1,
        "log": [],
        "game_over": False,
    }

game_state = reset_game()

# Button class
class Button:
    def __init__(self, text, x, y, w, h, action):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.action = action

    def draw(self):
        pygame.draw.rect(screen, BLACK, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        txt_surf = FONT.render(self.text, True, WHITE)
        screen.blit(txt_surf, (self.rect.x + (self.rect.width - txt_surf.get_width()) // 2,
                               self.rect.y + (self.rect.height - txt_surf.get_height()) // 2))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Action functions
def log_action(msg):
    game_state["log"].append(msg)
    if len(game_state["log"]) > 4:
        game_state["log"].pop(0)

def next_turn():
    game_state["turn"] = 2 if game_state["turn"] == 1 else 1

def attack(attack_type="normal"):
    if game_state["game_over"]:
        return

    if attack_type not in ATTACK_TYPES:
        attack_type = "normal"

    min_dmg, max_dmg = ATTACK_TYPES[attack_type]
    damage = random.randint(min_dmg, max_dmg)
    crit = False

    if random.random() < 0.2:
        damage *= 2
        crit = True

    if game_state["turn"] == 1:
        if game_state["p2_def"]:
            damage //= 2
            game_state["p2_def"] = False
            log_action("Player 2 defended! Damage halved.")
        game_state["p2_hp"] -= damage
        log_action(f"Player 1 {'CRIT ' if crit else ''}used {attack_type} attack for {damage}!")
    else:
        if game_state["p1_def"]:
            damage //= 2
            game_state["p1_def"] = False
            log_action("Player 1 defended! Damage halved.")
        game_state["p1_hp"] -= damage
        log_action(f"Player 2 {'CRIT ' if crit else ''}used {attack_type} attack for {damage}!")

    next_turn()

def defend():
    if game_state["turn"] == 1:
        game_state["p1_def"] = True
        log_action("Player 1 is defending. 🛡️")
    else:
        game_state["p2_def"] = True
        log_action("Player 2 is defending. 🛡️")
    next_turn()

def heal():
    heal_amt = random.randint(10, 20)
    if game_state["turn"] == 1:
        if game_state["p1_hp"] >= 100:
            log_action("Player 1 is already at full HP.")
            return
        game_state["p1_hp"] = min(game_state["p1_hp"] + heal_amt, 100)
        log_action(f"Player 1 healed for {heal_amt}. ❤️")
    else:
        if game_state["p2_hp"] >= 100:
            log_action("Player 2 is already at full HP.")
            return
        game_state["p2_hp"] = min(game_state["p2_hp"] + heal_amt, 100)
        log_action(f"Player 2 healed for {heal_amt}. ❤️")
    next_turn()

def special():
    if game_state["turn"] == 1:
        if game_state["p1_special"]:
            log_action("Player 1 already used special.")
            return
        damage = random.randint(25, 35)
        if game_state["p2_def"]:
            damage //= 2
            game_state["p2_def"] = False
        game_state["p2_hp"] -= damage
        game_state["p1_special"] = True
        log_action(f"Player 1 used SPECIAL for {damage}! 🔥")
    else:
        if game_state["p2_special"]:
            log_action("Player 2 already used special.")
            return
        damage = random.randint(25, 35)
        if game_state["p1_def"]:
            damage //= 2
            game_state["p1_def"] = False
        game_state["p1_hp"] -= damage
        game_state["p2_special"] = True
        log_action(f"Player 2 used SPECIAL for {damage}! 🔥")
    next_turn()

# Restart function
def restart_game():
    global game_state
    game_state = reset_game()

# Buttons for during gameplay
game_buttons = [
    Button("Quick", 80, 450, 80, 40, lambda: attack("quick")),
    Button("Normal", 170, 450, 80, 40, lambda: attack("normal")),
    Button("Heavy", 260, 450, 80, 40, lambda: attack("heavy")),
    Button("Defend", 350, 450, 90, 40, defend),
    Button("Heal", 450, 450, 90, 40, heal),
    Button("Special", 550, 450, 90, 40, special),
]

# Restart button (only appears after game ends)
restart_button = Button("Restart", 375, 500, 150, 50, restart_game)

# Game loop
def draw_game():
    screen.blit(PLAYER1_IMG, (100, 150))
    screen.blit(PLAYER2_IMG, (650, 150))

    # HP bars
    pygame.draw.rect(screen, RED, (100, 100, game_state["p1_hp"] * 2, 20))
    pygame.draw.rect(screen, GREEN, (650, 100, game_state["p2_hp"] * 2, 20))
    screen.blit(FONT.render(f"Player 1 HP: {game_state['p1_hp']}", True, WHITE), (100, 70))
    screen.blit(FONT.render(f"Player 2 HP: {game_state['p2_hp']}", True, WHITE), (650, 70))

    # Action log
    y = 320
    screen.blit(FONT.render("Log:", True, WHITE), (50, y))
    for line in game_state["log"]:
        y += 25
        screen.blit(FONT.render(line, True, WHITE), (50, y))

    # Buttons
    if not game_state["game_over"]:
        for btn in game_buttons:
            btn.draw()
    else:
        restart_button.draw()

    # Victory message
    if game_state["p1_hp"] <= 0:
        game_state["game_over"] = True
        screen.blit(FONT.render("🎉 Player 2 Wins!", True, RED), (350, 250))
    elif game_state["p2_hp"] <= 0:
        game_state["game_over"] = True
        screen.blit(FONT.render("🎉 Player 1 Wins!", True, GREEN), (350, 250))

def run_game():
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill(BLACK)
        draw_game()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_state["game_over"]:
                    for btn in game_buttons:
                        if btn.is_clicked(event.pos):
                            btn.action()
                else:
                    if restart_button.is_clicked(event.pos):
                        restart_button.action()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_game()
