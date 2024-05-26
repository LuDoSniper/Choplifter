from objects.menu.menu import Menu
from objects.menu.menu_jouer import MenuJouer
from objects.menu.menu_options import MenuOptions
from objects.menu.menu_credits import MenuCredits

import pygame
import sys

class Link:
    def __init__(self, assets):
        self.assets = assets
        self.current_menu = "main"
        self.menus = {
            "main": Menu(self.assets.screen, self.change_menu, self.assets),
            "play": MenuJouer(self.assets.screen, self.change_menu, self.assets),
            "options": MenuOptions(self.assets.screen, self.change_menu, self.update_theme, self.assets),
            "credits": MenuCredits(self.assets.screen, self.change_menu, self.assets),
        }
        self.update_theme(self.assets.THEME) 

    def change_menu(self, menu_name):
        self.current_menu = menu_name

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        self.menus[self.current_menu].handle_event(event)

    def draw(self):
        self.menus[self.current_menu].draw()

    def update_theme(self, new_theme):
        self.assets.THEME = new_theme
        self.assets.bouton = pygame.image.load(f'assets/menu/bouton_{self.assets.THEME.lower()}.png').convert_alpha()
        self.assets.bouton = pygame.transform.scale(self.assets.bouton, (self.assets.new_button_width, self.assets.new_button_height))
        
        self.menus["options"].update_sound(self.assets.click_sound.get_volume())
        self.menus["options"].update_music(pygame.mixer.music.get_volume())

        for menu_name in self.menus:
            if hasattr(self.menus[menu_name], 'buttons'):
                self.menus[menu_name].create_buttons()
