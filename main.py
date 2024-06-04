import pygame
import objects.game as game
import objects.music as music
import objects.saver as saver

pygame.init()
pygame.font.init()
pygame.mixer.init()

music_manager = music.Music()
save_manager = saver.Saver()

data = save_manager.load()
current_game = game.Game(music_manager, "menu")
current_game.set_data(data)
current_game.handle()
data = current_game.get_data()

response = current_game.get_response()
while response != "exit":
    if response == "solo":
        musique = "mission1"
        mode = "solo"
    elif response == "restart":
        musique = "main_background_layer2" # Lancera le layer 1 car le changement de musique à l'air d'être detecté comme un SONG_END donc la loop se met en place et donc interverti layer1 avec layer2
        mode = "menu"
        
    # Antibug
    if response is None:
        current_game.change_menu(current_game.get_current_menu())
    else:  
        music_manager.switch(musique)
        current_game = game.Game(music_manager, mode)
        current_game.set_data(data)
        current_game.handle()
        response = current_game.get_response()

save_manager.save(current_game.get_data())

pygame.quit()