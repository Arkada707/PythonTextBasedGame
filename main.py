import pygame
import sys
import random
from player import Player
from display import Display
from enemy import Enemy
from tile import Tile

pygame.init()
pygame.mixer.init()

# Load music
pygame.mixer.music.load('music_ai_2024-6-10.wav')
pygame.mixer.music.play(-1)  # Play the music in a loop

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tower of Trials")

# Fonts
font = pygame.font.Font(None, 36)

# Constants
TILE_SIZE = 40
GRID_WIDTH = 5
GRID_HEIGHT = 5

def generate_dungeon(level):
    dungeon_map = [[Tile() for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    exit_x = random.randint(0, GRID_WIDTH - 1)
    exit_y = random.randint(0, GRID_HEIGHT - 1)
    dungeon_map[exit_y][exit_x] = Tile('exit')

    ladder_up_x = ladder_up_y = None
    if level > 0:
        ladder_up_x = random.randint(0, GRID_WIDTH - 1)
        ladder_up_y = random.randint(0, GRID_HEIGHT - 1)
        dungeon_map[ladder_up_y][ladder_up_x] = Tile('ladder_up')

    ladder_down_x = random.randint(0, GRID_WIDTH - 1)
    ladder_down_y = random.randint(0, GRID_HEIGHT - 1)
    while (ladder_down_x, ladder_down_y) == (exit_x, exit_y) or (ladder_down_x, ladder_down_y) == (ladder_up_x, ladder_up_y):
        ladder_down_x = random.randint(0, GRID_WIDTH - 1)
        ladder_down_y = random.randint(0, GRID_HEIGHT - 1)
    dungeon_map[ladder_down_y][ladder_down_x] = Tile('ladder_down')

    for _ in range(1 + level):
        enemy_x = random.randint(0, GRID_WIDTH - 1)
        enemy_y = random.randint(0, GRID_HEIGHT - 1)
        while dungeon_map[enemy_y][enemy_x].type != 'empty':
            enemy_x = random.randint(0, GRID_WIDTH - 1)
            enemy_y = random.randint(0, GRID_HEIGHT - 1)
        dungeon_map[enemy_y][enemy_x].set_enemy(Enemy("Goblin", 50, 10, 50))

    return dungeon_map

# Game maps using Tile objects
town_map = [
    [Tile('town'), Tile('town'), Tile('town'), Tile('town'), Tile('town')],
    [Tile('town'), Tile(), Tile(), Tile(), Tile('town')],
    [Tile('town'), Tile(), Tile('dungeon_entrance'), Tile(), Tile('town')],
    [Tile('town'), Tile(), Tile(), Tile(), Tile('town')],
    [Tile('town'), Tile('town'), Tile('town'), Tile('town'), Tile('town')]
]

# Initial map and level
game_map = town_map
dungeon_level = 0

# Game objects
player = Player(2, 2)
display = Display(screen, font)
current_enemy = None

def main_menu():
    title_font = pygame.font.Font(None, 74)
    menu_font = pygame.font.Font(None, 50)
    
    title_text = title_font.render("Tower of Trials", True, (255, 255, 255))
    start_text = menu_font.render("Start Game", True, (255, 255, 255))
    settings_text = menu_font.render("Settings", True, (255, 255, 255))
    
    selected_option = 0
    options = ["Start Game", "Settings"]

    while True:
        screen.fill((0, 0, 0))
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))
        
        for i, option in enumerate(options):
            if i == selected_option:
                text = menu_font.render(f"> {option}", True, (255, 255, 255))
            else:
                text = menu_font.render(option, True, (200, 200, 200))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 250 + i * 60))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[selected_option] == "Start Game":
                        return "start_game"
                    elif options[selected_option] == "Settings":
                        return "settings"

def settings_menu():
    menu_font = pygame.font.Font(None, 50)
    
    volume = pygame.mixer.music.get_volume()
    
    while True:
        screen.fill((0, 0, 0))
        
        volume_text = menu_font.render(f"Music Volume: {int(volume * 100)}%", True, (255, 255, 255))
        screen.blit(volume_text, (SCREEN_WIDTH // 2 - volume_text.get_width() // 2, 250))
        
        back_text = menu_font.render("Back", True, (255, 255, 255))
        screen.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, 350))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    volume = min(1, volume + 0.1)
                    pygame.mixer.music.set_volume(volume)
                elif event.key == pygame.K_DOWN:
                    volume = max(0, volume - 0.1)
                    pygame.mixer.music.set_volume(volume)
                elif event.key == pygame.K_RETURN:
                    return

def encounter_enemy():
    global current_enemy
    tile = game_map[player.y][player.x]
    if tile.is_enemy():
        current_enemy = tile.enemy
        display.set_display_text(f"You have encountered a {current_enemy.name}!")
        display.set_battle_text(current_enemy.get_stats())
        display.set_menu_options(["Attack", "Run Away", "Avoid", "Move L", "Move U", "Move D", "Move R"])
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
            game_map[player.y][player.x].remove_enemy()
            current_enemy = None
            update_menu_options()
        else:
            display.set_battle_text(f"{current_enemy.get_stats()} - Dealt {damage_to_enemy} damage, received {damage_to_player} damage.")
            display.set_menu_options(["Attack", "Run Away", "Avoid", "Move L", "Move U", "Move D", "Move R"])
    return True

def run_away():
    global current_enemy
    current_enemy = None
    update_menu_options()
    display.set_display_text("You ran away from the enemy!")

def update_menu_options():
    global current_enemy
    options = ["Move L", "Move U", "Move D", "Move R"]
    print(f"Player position: ({player.x}, {player.y})")  # Debug print
    tile = game_map[player.y][player.x]
    if tile.is_exit():
        options.append("Leave")
        print("Player is on an exit tile.")  # Debug print
    if tile.is_ladder_up():
        options.append("Go Up")
        print("Player is on a ladder up tile.")  # Debug print
    if tile.is_ladder_down():
        options.append("Go Down")
        print("Player is on a ladder down tile.")  # Debug print
    if tile.is_dungeon_entrance():
        options.append("Enter Dungeon")
        print("Player is on a dungeon entrance tile.")  # Debug print
    if current_enemy:
        options = ["Attack", "Run Away", "Avoid"] + options
    display.set_menu_options(options)

def check_tile():
    global current_enemy
    tile = game_map[player.y][player.x]
    if tile.is_exit():
        display.set_display_text("You are on an exit tile.")
        update_menu_options()
    elif tile.is_enemy():
        display.set_display_text(f"You have encountered a {tile.enemy.name}!")
        display.set_battle_text(tile.enemy.get_stats())
        display.set_menu_options(["Attack", "Run Away", "Avoid", "Move L", "Move U", "Move D", "Move R"])
        current_enemy = tile.enemy
    elif tile.is_ladder_up():
        display.set_display_text("You are on a ladder up tile.")
        update_menu_options()
    elif tile.is_ladder_down():
        display.set_display_text("You are on a ladder down tile.")
        update_menu_options()
    elif tile.is_dungeon_entrance():
        display.set_display_text("You are on a dungeon entrance tile.")
        update_menu_options()
    else:
        display.set_display_text("The tile is empty.")
        current_enemy = None
        update_menu_options()

def process_input(option):
    global game_map, dungeon_level, current_enemy
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
    elif option == "Run Away" and current_enemy:
        run_away()
    elif option == "Avoid" and current_enemy:
        display.set_display_text("You avoided the enemy!")
        current_enemy = None
        update_menu_options()
    elif option == "Leave" and game_map[player.y][player.x].is_exit():
        display.set_display_text("You have left the Dungeon and reached the Town!")
        game_map = town_map
        player.x, player.y = 2, 2  # Reset player position
        update_menu_options()  # Ensure the menu options are updated after changing the map
    elif option == "Go Up" and game_map[player.y][player.x].is_ladder_up():
        if dungeon_level > 0:
            dungeon_level -= 1
            game_map = generate_dungeon(dungeon_level)
            display.set_display_text(f"You have moved up to Dungeon Level {dungeon_level}!")
        player.x, player.y = 2, 2  # Reset player position
        update_menu_options()  # Ensure the menu options are updated after changing the map
    elif option == "Go Down" and game_map[player.y][player.x].is_ladder_down():
        dungeon_level += 1
        game_map = generate_dungeon(dungeon_level)
        display.set_display_text(f"You have moved down to Dungeon Level {dungeon_level}!")
        player.x, player.y = 2, 2  # Reset player position
        update_menu_options()  # Ensure the menu options are updated after changing the map
    elif option == "Enter Dungeon" and game_map[player.y][player.x].is_dungeon_entrance():
        display.set_display_text("You have entered the Dungeon!")
        dungeon_level = 0
        game_map = generate_dungeon(dungeon_level)
        player.x, player.y = 2, 2  # Reset player position
        update_menu_options()  # Ensure the menu options are updated after changing the map
    else:
        display.set_display_text("Invalid command.")
    
    check_tile()  # Check the tile after any move
    
    display.update_display(player, game_map)
    return True

def main():
    global game_map
    while True:
        action = main_menu()
        if action == "start_game":
            game_map = town_map
            player.x, player.y = 2, 2  # Reset player position
            break
        elif action == "settings":
            settings_menu()

    update_menu_options()
    running = True
    
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

if __name__ == "__main__":
    main()
