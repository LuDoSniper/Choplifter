import pygame
import objects.game as game

pygame.init()

current_game = game.Game()
current_game.handle()

pygame.quit()