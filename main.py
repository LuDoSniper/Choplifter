import pygame
import objects.game as game
import objects.music as music

pygame.init()
pygame.font.init()
pygame.mixer.init()

music_manager = music.Music()

current_game = game.Game(music_manager, "menu")
current_game.handle()
data = current_game.get_data()

while current_game.get_response() != "exit":
    if current_game.get_response() == "solo":
        musique = "mission1"
        mode = "solo"
        
    music_manager.switch(musique)
    current_game = game.Game(music_manager, mode)
    current_game.set_data(data)
    current_game.handle()

pygame.quit()