import pygame
import random

TILE_SIZE = 40
GRID_WIDTH = 5
GRID_HEIGHT = 5
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Display:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.display_text = "Welcome to the Text-Based Game!"
        self.battle_text = ""
        self.input_text = ""
        self.menu_options = []
        self.current_option_index = 0

    def update_display(self, player, game_map):
        self.screen.fill((0, 0, 0))
        text = self.font.render(self.display_text, True, (0, 255, 0))
        self.screen.blit(text, (20, 20))
        stats = self.font.render(player.get_stats(), True, (0, 255, 0))
        self.screen.blit(stats, (20, 60))
        if self.battle_text:
            battle = self.font.render(self.battle_text, True, (255, 0, 0))
            self.screen.blit(battle, (20, 100))
        
        self.draw_map(player, game_map)
        self.draw_menu()
        pygame.display.flip()

    def draw_map(self, player, game_map):
        offset_x = (SCREEN_WIDTH - GRID_WIDTH * TILE_SIZE) // 2
        offset_y = (SCREEN_HEIGHT - GRID_HEIGHT * TILE_SIZE) // 2
        
        for y, row in enumerate(game_map):
            for x, tile in enumerate(row):
                if tile.is_empty():
                    pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(offset_x + x * TILE_SIZE, offset_y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)
                elif tile.is_exit():
                    pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(offset_x + x * TILE_SIZE, offset_y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)
                elif tile.is_ladder_up():
                    pygame.draw.rect(self.screen, (0, 255, 255), pygame.Rect(offset_x + x * TILE_SIZE, offset_y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)
                elif tile.is_ladder_down():
                    pygame.draw.rect(self.screen, (255, 255, 0), pygame.Rect(offset_x + x * TILE_SIZE, offset_y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)
                elif tile.is_dungeon_entrance():
                    pygame.draw.rect(self.screen, (255, 165, 0), pygame.Rect(offset_x + x * TILE_SIZE, offset_y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)
                if tile.is_enemy():
                    pygame.draw.circle(self.screen, (255, 0, 0), (offset_x + x * TILE_SIZE + TILE_SIZE // 2, offset_y + y * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 4)
        
        pygame.draw.rect(self.screen, (0, 0, 255), pygame.Rect(offset_x + player.x * TILE_SIZE, offset_y + player.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    def draw_menu(self):
        offset_y = SCREEN_HEIGHT // 2 + GRID_HEIGHT * TILE_SIZE // 2 + 20
        for index, option in enumerate(self.menu_options):
            if index == self.current_option_index:
                option_text = self.font.render(f"> {option}", True, (255, 255, 255))
            else:
                option_text = self.font.render(option, True, (200, 200, 200))
            self.screen.blit(option_text, (20, offset_y + index * 30))

    def set_display_text(self, text):
        self.display_text = text

    def set_battle_text(self, text):
        self.battle_text = text

    def set_input_text(self, text):
        self.input_text = text

    def set_menu_options(self, options):
        self.menu_options = options
        self.current_option_index = 0

    def move_menu_selection(self, direction):
        self.current_option_index = (self.current_option_index + direction) % len(self.menu_options)

    def get_selected_option(self):
        return self.menu_options[self.current_option_index]
