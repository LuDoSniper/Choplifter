from objects.menu.menu import Menu
from objects.menu.menu_jouer import MenuJouer
from objects.menu.menu_options import MenuOptions
from objects.menu.menu_credits import MenuCredits
from objects.menu.menu_pause import MenuPause
from objects.menu.menu_son import MenuSon
from objects.menu.menu_score import MenuScore
from objects.menu.menu_mission import MenuMission
from objects.menu.menu_lose import MenuLose
from objects.menu.menu_win import MenuWin
from objects.menu.lose_step import LoseStep
from objects.menu.win_step import WinStep
from objects.menu.menu_palier import MenuPalier
import objects.music as music
import objects.requester as requester
import objects.saver as saver

import pygame

def max_score(data: list, palier: bool = False) -> list:
    key = "score"
    if palier:
        key = "palier"
    data = list(data)
    max = data[0]
    for score in data:
        if score[key] > max[key]:
            max = score
    return max

def trier_score(data: list, palier: bool = False) -> list:
    data = list(data)
    scores = []
    while data != []:
        max = max_score(data, palier)
        data.pop(data.index(max))
        scores.append(max)
    return scores

requests_manager = requester.Requester()
data = requests_manager.download(True, True)

classement_score = []
data["all"]["score"] = trier_score(data["all"]["score"])
for player in data["scoreboard"]["score"]:
    classement_score.append((player["username"], player["score"]))
if "self" not in data or data["self"] not in data["all"]["score"]:
    positionnement_score = "Aucune données"
    points_vous = "Aucune données"
else:
    positionnement_score = data["all"]["score"].index(data["self"]) + 1
    points_vous = data["self"]["score"]

save_manager = saver.Saver()

classement_palier = []
data["all"]["palier"] = trier_score(data["all"]["palier"], palier=True)
for player in data["scoreboard"]["palier"]:
    classement_palier.append((player["username"], player["score"]))
if "self" not in data or data["self"] not in data["all"]["palier"]:
    positionnement_palier = "Aucune données"
    palier_vous = "Aucune données"
else:
    positionnement_palier = data["all"]["palier"].index(data["self"]) + 1
    palier_vous = data["self"]["palier"]

data = save_manager.load()
missions = data["missions"]

if data["survival"]["score"] is None:
    score = 0
else:
    score = data["survival"]["score"]
if data["survival"]["palier"] is None:
    palier = 0
else:
    palier = data["survival"]["palier"]

class Link:
    def __init__(self, assets):
        self.missions = save_manager.load()["missions"]
        self.stop = False
        self.restart = False
        self.assets = assets
        self.current_menu = "main"
        self.classement_score = classement_score
        self.positionnement_score = positionnement_score
        self.points_vous = points_vous
        self.classement_palier = classement_palier
        self.positionnement_palier = positionnement_palier
        self.palier_vous = palier_vous
        self.score = score
        self.palier = palier
        self.son = music.Music()
        self.menus = {
            "main": Menu(self.assets.screen, self.change_menu, self.quit_game, self.assets),
            "play": MenuJouer(self.assets.screen, self.change_menu, self.assets),
            "options": MenuOptions(self.assets.screen, self.change_menu, self.update_theme, self.update_resolution, self.assets),
            "credits": MenuCredits(self.assets.screen, self.change_menu, self.assets),
            "pause": MenuPause(self.assets.screen, self.change_menu, self.restart_game, self.quit_game, assets),
            "son": MenuSon(self.assets.screen, self.change_menu, assets),
            "survie": MenuScore(self.assets.screen, self.change_menu, assets, self.classement_score, self.positionnement_score, self.points_vous),
            "palier": MenuPalier(self.assets.screen, self.change_menu, assets, classement_palier, positionnement_palier, palier_vous),
            "mission": MenuMission(self.assets.screen, self.change_menu, assets, missions, "Ile Alloca"),
            "lose": MenuLose(self.assets.screen, self.change_menu, assets),
            "win": MenuWin(self.assets.screen, self.change_menu, assets),
            "lose_step": LoseStep(self.assets.screen, self.change_menu, assets, score, palier),
            "win_step": WinStep(self.assets.screen, self.change_menu, assets, score, palier)
        }
        self.update_theme(self.assets.THEME)
        self.update_resolution(self.assets.RESOLUTION)

    def change_menu(self, menu_name):
        if menu_name == "survie":
            data = self.get_scoreboard()
            self.classement_score = data[0][0]
            self.positionnement_score = data[0][1]
            self.points_vous = data[0][2]
            self.classement_palier = data[1][0]
            self.positionnement_palier = data[1][1]
            self.palier_vous = data[1][2]
            self.menus["survie"].set_scoreboard(data[0])
            self.menus["palier"].set_scoreboard(data[1])
        elif menu_name in ("win_step", "lose_step"):
            data = self.get_score_palier()
            self.score = data[0]
            self.palier = data[1]
            self.menu[menu_name].set_score_palier(data)
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

    def get_score_palier(self) -> tuple:
        if data["survival"]["score"] is None:
            score = 0
        else:
            score = data["survival"]["score"]
        if data["survival"]["palier"] is None:
            palier = 0
        else:
            palier = data["survival"]["palier"]
        return (score, palier)

    def get_scoreboard(self) -> list:
        classment = []
        positionnement = 0
        points = 0
        data = requests_manager.download(True, True)
        data["all"]["score"] = trier_score(data["all"]["score"])
        for player in data["scoreboard"]["score"]:
            classment.append((player["username"], player["score"]))
        if "self" not in data or data["self"] not in data["all"]["score"]:
            positionnement = "Aucune données"
            points = "Aucune données"
        else:
            positionnement = data["all"]["score"].index(data["self"]) + 1
            points = data["self"]["score"]
        
        classement_palier = []
        positionnement_palier = 0
        palier_vous = 0
        data["all"]["palier"] = trier_score(data["all"]["palier"])
        for player in data["scoreboard"]["palier"]:
            classement_palier.append((player["username"], player["palier"]))
        if "self" not in data or data["self"] not in data["all"]["palier"]:
            positionnement_palier = "Aucune données"
            palier_vous = "Aucune données"
        else:
            positionnement_palier = data["all"]["palier"].index(data["self"]) + 1
            palier_vous = data["self"]["palier"]
        
        return ((classment, positionnement, points), (classement_palier, positionnement_palier, palier_vous))

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