import pygame
import random
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

screen = assets_manager.SCREEN
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
print("Resolution : ", screen.get_size())

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
    steps = None
    mission = None
    monde = None
    if response is not None and "-" in response:
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
    elif response == "new_try_survie":
        mode = f"new_try_survie{current_game.get_player().get_try()}"
        monde = current_game.get_monde_id()
        mission = current_game.get_mission_id()
        intensity = "low"
        musique = f"monde{monde}-{intensity}"
    elif response in ("survie", "survie_retry"):
        mode = "survie"
        monde = random.randint(1, 4)
        mission = 1
        intensity = "low"
        musique = f"monde{monde}-{intensity}"
        steps = 0
    elif response == "survie_next":
        mode = "survie"
        monde = random.randint(1, 4)
        mission = current_game.get_mission_id() + 1
        intensity = "low"
        musique = f"monde{monde}-{intensity}"
        steps = current_game.get_steps()
        if steps is None:
            steps = 0
        steps += 1
        
    # Antibug
    if response is None:
        current_game.change_menu(current_game.get_current_menu())
    else:  
        music_manager.switch(musique)
        current_game = game.Game(screen, assets_manager, music_manager, mode, steps, mission, monde)
        current_game.set_data(data)
        current_game.handle()
        save_manager.save(current_game.get_data())
        response = current_game.get_response()

save_manager.save(current_game.get_data())

pygame.quit()