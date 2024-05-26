import pygame
import objects.game as game
import objects.menu.assets as assets

pygame.init()
pygame.font.init()
pygame.mixer.init()

current_game = game.Game()
current_game.handle()

pygame.quit()