import pygame
import sys
import random
from player import Player
from display import Display
from enemy import Enemy

pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Text-Based Game")

# Fonts
font = pygame.font.Font(None, 36)

# Constants
TILE_SIZE = 40
GRID_WIDTH = 5
GRID_HEIGHT = 5

# Game maps
dungeon_map = [
    [' ', ' ', ' ', ' ', ' '],
    [' ', 'E', ' ', 'E', ' '],
    [' ', ' ', ' ', ' ', ' '],
    [' ', 'E', ' ', 'E', ' '],
    [' ', ' ', ' ', ' ', 'E']
]

town_map = [
    ['T', 'T', 'T', 'T', 'T'],
    ['T', ' ', ' ', ' ', 'T'],
    ['T', ' ', 'T', ' ', 'T'],
    ['T', ' ', ' ', ' ', 'T'],
    ['T', 'T', 'T', 'T', 'T']
]

# Initial map
game_map = dungeon_map

# Game objects
player = Player(2, 2)
display = Display(screen, font)
current_enemy = None

def encounter_enemy():
    global current_enemy
    if random.random() < 0.35:  # 35% chance to encounter an enemy
        current_enemy = Enemy("Goblin", 50, 10, 50)
        display.set_display_text(f"You have encountered a {current_enemy.name}!")
        display.set_battle_text(current_enemy.get_stats())
        display.set_menu_options(["Attack", "Move L", "Move U", "Move D", "Move R"])
    else:
        current_enemy = None
        update_menu_options()

def attack_enemy():
    global current_enemy
    if current_enemy:
        damage_to_enemy = player.attack()
        enemy_dead = current_enemy.take_damage(damage_to_enemy)
        damage_to_player = current_enemy.attack()
        player_dead = player.take_damage(damage_to_player)
        display.set_battle_text(f"Dealt {damage_to_enemy} damage, received {damage_to_player} damage.")
        if player_dead:
            display.set_display_text("You have died.")
            return False
        if enemy_dead:
            gold_dropped = random.randint(10, 50)
            player.add_gold(gold_dropped)
            display.set_display_text(f"You have defeated the {current_enemy.name}! You found {gold_dropped} gold.")
            player.gain_experience(current_enemy.experience_reward)
            display.set_battle_text("")
            current_enemy = None
            update_menu_options()
        else:
            display.set_battle_text(f"{current_enemy.get_stats()} - Dealt {damage_to_enemy} damage, received {damage_to_player} damage.")
            display.set_menu_options(["Attack", "Move L", "Move U", "Move D", "Move R"])
    return True

def update_menu_options():
    options = ["Move L", "Move U", "Move D", "Move R"]
    print(f"Player position: ({player.x}, {player.y})")  # Debug print
    if game_map[player.y][player.x] == 'E':
        options.append("Leave")
        print("Player is on an exit tile.")  # Debug print
    if current_enemy:
        options.insert(0, "Attack")
    display.set_menu_options(options)

def process_input(option):
    global game_map
    if option == "Move L":
        player.move(-1, 0, GRID_WIDTH, GRID_HEIGHT)
    elif option == "Move R":
        player.move(1, 0, GRID_WIDTH, GRID_HEIGHT)
    elif option == "Move U":
        player.move(0, -1, GRID_WIDTH, GRID_HEIGHT)
    elif option == "Move D":
        player.move(0, 1, GRID_WIDTH, GRID_HEIGHT)
    elif option == "Attack" and current_enemy:
        if not attack_enemy():
            return False
    elif option == "Leave" and game_map[player.y][player.x] == 'E':
        if game_map == dungeon_map:
            display.set_display_text("You have left the Dungeon and reached the Town!")
            game_map = town_map
        elif game_map == town_map:
            display.set_display_text("You have entered the Dungeon!")
            game_map = dungeon_map
        player.x, player.y = 2, 2  # Reset player position
        update_menu_options()  # Ensure the menu options are updated after changing the map
    else:
        display.set_display_text("Invalid command.")
    
    if game_map == dungeon_map and game_map[player.y][player.x] != 'E':
        encounter_enemy()
    
    display.update_display(player, game_map)
    return True

running = True

update_menu_options()
# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if not process_input(display.get_selected_option()):
                    running = False
            elif event.key == pygame.K_UP:
                display.move_menu_selection(-1)
            elif event.key == pygame.K_DOWN:
                display.move_menu_selection(1)

    display.update_display(player, game_map)
    pygame.display.flip()

pygame.quit()
sys.exit()
