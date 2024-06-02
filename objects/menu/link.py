from objects.menu.menu import Menu
from objects.menu.menu_jouer import MenuJouer
from objects.menu.menu_options import MenuOptions
from objects.menu.menu_credits import MenuCredits
from objects.menu.dropdown import Dropdown
from objects.menu.menu_pause import MenuPause
from objects.menu.menu_son import MenuSon

import pygame

class Link:
    def __init__(self, assets):
        self.stop = False
        self.assets = assets
        self.current_menu = "main"
        self.menus = {
            "main": Menu(self.assets.screen, self.change_menu, self.quit_game, self.assets),
            "play": MenuJouer(self.assets.screen, self.change_menu, self.assets),
            "options": MenuOptions(self.assets.screen, self.change_menu, self.update_theme, self.assets),
            "credits": MenuCredits(self.assets.screen, self.change_menu, self.assets),
            "pause": MenuPause(self.assets.screen, self.change_menu, self.quit_game, assets),
            "son": MenuSon(self.assets.screen, self.change_menu, assets)
        }
        self.update_theme(self.assets.THEME) 

    def change_menu(self, menu_name):
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

        self.menus["options"].update_sound(self.assets.click_sound.get_volume())
        self.menus["options"].update_music(pygame.mixer.music.get_volume())
        self.menus["options"].update_dropdown()

        for menu_name in self.menus:
            if hasattr(self.menus[menu_name], 'buttons'):
                self.menus[menu_name].create_buttons()

    def quit_game(self) -> None:
        self.stop = True

    def get_data(self) -> dict:
        # Récupérer le volume
        data = self.menus["options"].get_volume()
        # Récupérer le theme
        data["theme"] = self.assets.THEME
        return data
    
    def set_volume(self, data: dict) -> None:
        self.menus["options"].set_volume(data)