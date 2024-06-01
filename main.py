import pygame
import os
import json
import objects.game as game
import objects.music as music

# Fonctions pour sauvegarder / charger des données

def save(data: dict) -> None:
    with open('save.json', 'w') as file:
        json.dump(data, file, indent=4)
        
def load() -> dict:
    if os.path.exists('save.json'):
        with open('save.json') as file:
            return json.load(file)
    else:
        return {
            "music" : 0.5,
            "sfx" : 0.5,
            "theme" : "Gris"
        }

# Main

pygame.init()
pygame.font.init()
pygame.mixer.init()

music_manager = music.Music()

data = load()
current_game = game.Game(music_manager, "menu")
current_game.set_data(data)
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

save(current_game.get_data())

pygame.quit()