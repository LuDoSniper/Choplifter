import pygame
import objects.game as game
import objects.music as music
import objects.saver as saver
import objects.menu.assets as assets

pygame.init()
pygame.font.init()
pygame.mixer.init()

pygame.display.set_icon(pygame.image.load("assets/icon/Icon.png"))
pygame.display.set_caption("Choplifter")
assets_manager = assets.Assets()
screen = pygame.display.set_mode((assets_manager.SCREEN_WIDTH, assets_manager.SCREEN_HEIGHT))

music_manager = music.Music(main=True)
save_manager = saver.Saver()

data = save_manager.load()
current_game = game.Game(screen, assets_manager, music_manager, "menu")
current_game.set_data(data)
current_game.handle()
data = current_game.get_data()
save_manager.save(data)

response = current_game.get_response()
while response != "exit":
    mission = None
    monde = None
    if "-" in response:
        tmp = response.split('-')
        mission = int(tmp[1])
        if tmp[0].split(' ')[0] == "Ile":
            monde = 1
        elif tmp[0].split(' ')[0] == "Foret":
            monde = 2
        elif tmp[0].split(' ')[0] == "Desert":
            monde = 3
        elif tmp[0].split(' ')[0] == "Montagne":
            monde = 4
        mode = "solo"
        if mission in (1, 2):
            intensity = "low"
        elif mission in (3, 4):
            intensity = "high"
        musique = f"monde{monde}-{intensity}"
    elif response == "solo":
        musique = "mission1"
        mode = "solo"
    elif response == "sandbox":
        musique = "mission1"
        mode = "sandbox"
    elif response == "restart":
        musique = "main_background_layer2" # Lancera le layer 1 car le changement de musique à l'air d'être detecté comme un SONG_END donc la loop se met en place et donc interverti layer1 avec layer2
        mode = "menu"
    elif response == "new_try":
        mode = "solo"
        monde = current_game.get_monde_id()
        mission = current_game.get_mission_id()
        if mission in (1, 2):
            intensity = "low"
        elif mission in (3, 4):
            intensity = "high"
        musique = f"monde{monde}-{intensity}"
        
    # Antibug
    if response is None:
        current_game.change_menu(current_game.get_current_menu())
    else:  
        music_manager.switch(musique)
        current_game = game.Game(screen, assets_manager, music_manager, mode, mission, monde)
        current_game.set_data(data)
        current_game.handle()
        save_manager.save(current_game.get_data())
        response = current_game.get_response()

save_manager.save(current_game.get_data())

pygame.quit()