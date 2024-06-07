from objects.menu.menu import Menu
from objects.menu.menu_jouer import MenuJouer
from objects.menu.menu_options import MenuOptions
from objects.menu.menu_credits import MenuCredits
from objects.menu.menu_pause import MenuPause
from objects.menu.menu_son import MenuSon
from objects.menu.menu_survie import MenuSurvie
from objects.menu.menu_mission import MenuMission
from objects.menu.menu_lose import MenuLose
from objects.menu.menu_win import MenuWin
from objects.menu.lose_step import LoseStep
from objects.menu.win_step import WinStep
import objects.requester as requester
import objects.saver as saver

import pygame

requests_manager = requester.Requester()
data = requests_manager.download(True, True)

classement = []
for player in data["scoreboard"]:
    classement.append((player["username"], player["score"]))
if "self" not in data:
    positionnement = "Aucune données"
    points_vous = "Aucune données"
else:
    positionnement = data["all"].index(data["self"]) + 1
    points_vous = data["self"]["score"]

save_manager = saver.Saver()

missions = save_manager.load()["missions"]

score = 1487
palier = 4

class Link:
    def __init__(self, assets):
        self.missions = save_manager.load()["missions"]
        self.stop = False
        self.restart = False
        self.assets = assets
        self.current_menu = "main"
        self.menus = {
            "main": Menu(self.assets.screen, self.change_menu, self.quit_game, self.assets),
            "play": MenuJouer(self.assets.screen, self.change_menu, self.assets),
            "options": MenuOptions(self.assets.screen, self.change_menu, self.update_theme, self.update_resolution, self.assets),
            "credits": MenuCredits(self.assets.screen, self.change_menu, self.assets),
            "pause": MenuPause(self.assets.screen, self.change_menu, self.restart_game, self.quit_game, assets),
            "son": MenuSon(self.assets.screen, self.change_menu, assets),
            "survie": MenuSurvie(self.assets.screen, self.change_menu, assets, classement, positionnement, points_vous),
            "mission": MenuMission(self.assets.screen, self.change_menu, assets, missions, "Ile Alloca"),
            "lose": MenuLose(self.assets.screen, self.change_menu, assets),
            "win": MenuWin(self.assets.screen, self.change_menu, assets),
            "lose_step": LoseStep(self.assets.screen, self.change_menu, assets, score, palier),
            "win_step": WinStep(self.assets.screen, self.change_menu, assets, score, palier)
        }
        self.update_theme(self.assets.THEME)
        self.update_resolution(self.assets.RESOLUTION)

    def change_menu(self, menu_name):
        save_manager.save(self.get_data())
        self.current_menu = menu_name

    def handle_event(self, event):
        return self.menus[self.current_menu].handle_event(event)

    def draw(self):
        self.menus[self.current_menu].draw()

    def update_theme(self, new_theme):
        self.assets.THEME = new_theme
        self.assets.retire_theme = [self.assets.theme for self.assets.theme in self.assets.THEMES if self.assets.theme != self.assets.THEME]
        
        self.assets.bouton = pygame.image.load(f'assets/menu/bouton_{self.assets.THEME.lower()}.png').convert_alpha()
        self.assets.bouton = pygame.transform.scale(self.assets.bouton, (self.assets.new_button_width, self.assets.new_button_height))
        self.assets.bouton_click = pygame.image.load(f'assets/menu/button-on-{self.assets.THEME.lower()}.png').convert_alpha()
        self.assets.bouton_click = pygame.transform.scale(self.assets.bouton_click, (self.assets.new_button_width, self.assets.new_button_height))

        
        self.assets.background_menu = pygame.image.load(f'assets/menu/background-{self.assets.THEME.lower()}.png')
        self.assets.background_menu = pygame.transform.scale(self.assets.background_menu, (int(self.assets.background_menu.get_width() * 0.7), int(self.assets.background_menu.get_height() * 0.7)))

        self.assets.bouton_jouer = pygame.image.load(f'assets/menu/bouton_jouer_{self.assets.THEME.lower()}.png').convert_alpha()
        self.assets.bouton_jouer_click = pygame.image.load(f'assets/menu/bouton_jouer_click_{self.assets.THEME.lower()}.png').convert_alpha()
        self.assets.bouton_jouer = pygame.transform.scale(self.assets.bouton_jouer, (self.assets.new_button_width, self.assets.new_button_height))
        self.assets.bouton_jouer_click = pygame.transform.scale(self.assets.bouton_jouer_click, (self.assets.new_button_width, self.assets.new_button_height))

        self.assets.bouton_unlock = pygame.image.load(f'assets/menu/unlock_{self.assets.THEME.lower()}.png').convert_alpha()
        self.assets.bouton_lock = pygame.image.load(f'assets/menu/lock_{self.assets.THEME.lower()}.png').convert_alpha()
        self.assets.bouton_unlock_clicked = pygame.image.load(f'assets/menu/unlock_clicked_{self.assets.THEME.lower()}.png').convert_alpha()

        self.menus["options"].update_sound(self.assets.click_sound.get_volume())
        self.menus["options"].update_music(pygame.mixer.music.get_volume())
        self.menus["options"].update_dropdown()

        self.menus["son"].update_sound(self.assets.click_sound.get_volume())
        self.menus["son"].update_music(pygame.mixer.music.get_volume())

        for menu_name in self.menus:
            if hasattr(self.menus[menu_name], 'buttons'):
                self.menus[menu_name].create_buttons()

    def update_resolution(self, new_resolution):
        self.assets.RESOLUTION = new_resolution
        self.assets.retire_resolution = [self.assets.resolution for self.assets.resolution in self.assets.RESOLUTIONS if self.assets.resolution != self.assets.RESOLUTION]
        if new_resolution == "600x800":
            self.assets.SCREEN_WIDTH = 800
            self.assets.SCREEN_HEIGHT = 600
            pygame.display.set_mode((self.assets.SCREEN_WIDTH, self.assets.SCREEN_HEIGHT))
        elif new_resolution == "FULL":
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.assets.SCREEN_WIDTH, self.assets.SCREEN_HEIGHT = self.assets.screen.get_size()
        print(self.assets.SCREEN_WIDTH, self.assets.SCREEN_HEIGHT)

        for menu_name in self.menus:
            if hasattr(self.menus[menu_name], 'elements'):
                self.menus[menu_name].elements = []
                self.menus[menu_name].create_elements()
            elif hasattr(self.menus[menu_name], 'buttons'):
                self.menus[menu_name].buttons = []
                self.menus[menu_name].create_buttons()

    def quit_game(self) -> None:
        self.stop = True

    def restart_game(self) -> None:
        self.restart = True

    def get_data(self) -> dict:
        data = self.menus["options"].get_volume()
        data["theme"] = self.assets.THEME
        data["missions"] = self.missions
        data["resolution"] = self.assets.RESOLUTION
        data_origine = save_manager.load()
        data["survival"] = data_origine["survival"]
        data["username"] = data_origine["username"]
        if "ID" in data_origine:
            data["ID"] = data_origine["ID"]
        return data
    
    def set_volume(self, data: dict) -> None:
        self.menus["options"].set_volume(data)
        self.menus["son"].set_volume(data)
    
    def set_missions(self, data_missions: dict) -> None:
        self.menus["mission"].set_missions(data_missions)
        self.missions = data_missions