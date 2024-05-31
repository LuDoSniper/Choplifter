from objects.menu.button import Button
from objects.menu.slider import Slider
import pygame

class MenuSon:
    def __init__(self, screen, change_menu_callback, assets):
        self.assets = assets
        self.screen = screen
        self.change_menu_callback = change_menu_callback
        self.create_elements()

    def create_elements(self):
        self.elements = []
        self.elements.append(Button("", 215, 325, self.assets.bouton_confirm, self.assets.bouton_confirm_click, self.confirm, self.assets))
        self.elements.append(Slider("Son", ((self.assets.SCREEN_WIDTH - self.assets.background_menu.get_width()) // 2), 200, 350, 8, self.update_sound, self.assets))
        self.elements.append(Slider("Musique", (self.assets.SCREEN_WIDTH - self.assets.background_menu.get_width()) // 2, 260, 350, 8, self.update_music, self.assets))

    def draw(self):
        bg_x = (self.assets.SCREEN_WIDTH - self.assets.background_menu_options.get_width()) // 2
        bg_y = (self.assets.SCREEN_HEIGHT - self.assets.background_menu_options.get_height()) // 2
        self.screen.blit(self.assets.background_menu_options, (bg_x, bg_y))

        mouse_pos = pygame.mouse.get_pos()
        for element in self.elements:
            element.update(mouse_pos)
            element.draw(self.screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for element in self.elements:
                if isinstance(element, Button) and element.is_hovered(event.pos):
                    self.clicked_element = element
                    element.on_click()
        elif event.type == pygame.MOUSEBUTTONUP:
            for element in self.elements:
                if isinstance(element, Button) and element == self.clicked_element:
                    element.up_click()
                elif isinstance(element, Slider):
                    element.handle_event(event)
            self.clicked_element = None 

    def update_sound(self, value):
        self.assets.click_sound.set_volume(value)
        print(f"Son volume: {value}")

    def update_music(self, value):
        pygame.mixer.music.set_volume(value)
        print(f"Musique volume: {value}")

    def confirm(self):
        print("Options confirmées")
        self.change_menu_callback("pause")