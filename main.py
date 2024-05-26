import pygame
import objects.game as game
import objects.menu.assets as assets

pygame.init()
pygame.font.init()
pygame.mixer.init()

current_game = game.Game("menu")
current_game.handle()

while current_game.get_response() != "exit":
    if current_game.get_response() == "solo":
        current_game = game.Game("solo")
        current_game.handle()

pygame.quit()