import pygame
import objects.game as game
import objects.music as music

pygame.init()
pygame.font.init()
pygame.mixer.init()

music_manager = music.Music()

current_game = game.Game(music_manager, "menu")
current_game.handle()

while current_game.get_response() != "exit":
    if current_game.get_response() == "solo":
        music_manager.switch("mission1")
        current_game = game.Game(music_manager, "solo")
        current_game.handle()

pygame.quit()