from objects.menu.button import Button
from objects.menu.slider import Slider
from objects.menu.dropdown import Dropdown
import pygame

class MenuOptions:
    def __init__(self, screen, change_menu_callback, update_theme_callback, update_resolution_callback, assets):
        self.assets = assets
        self.screen = screen
        self.change_menu_callback = change_menu_callback
        self.update_theme_callback = update_theme_callback
        self.update_resolution_callback = update_resolution_callback
        self.clicked_element = None 
        self.elements = []
        self.create_elements()

    def create_elements(self):
        self.elements.append(Button("", 215, 475, self.assets.bouton_confirm, self.assets.bouton_confirm_click, self.confirm, self.assets))
        self.elements.append(Slider("Son", ((self.assets.SCREEN_WIDTH - self.assets.background_menu.get_width()) // 2), 200, 350, 8, self.update_sound, self.assets))
        self.elements.append(Slider("Musique", (self.assets.SCREEN_WIDTH - self.assets.background_menu.get_width()) // 2, 260, 350, 8, self.update_music, self.assets))
        self.elements.append(Dropdown("Thème", (self.assets.SCREEN_WIDTH - self.assets.background_menu.get_width()) // 2, 325, 133, 30, self.assets.retire_theme, self.update_theme, self.assets))
        self.elements.append(Dropdown("Résolution", ((self.assets.SCREEN_WIDTH - self.assets.background_menu.get_width()) // 2) + 150, 325, 133, 30, self.assets.retire_resolution, self.update_resolution, self.assets, False))

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
                elif isinstance(element, Slider) or isinstance(element, Dropdown):
                    element.handle_event(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            for element in self.elements:
                if isinstance(element, Button) and element == self.clicked_element:
                    element.image = element.image_default
                    if element.is_hovered(event.pos):
                        element.up_click()
                elif isinstance(element, Slider):
                    element.handle_event(event)
            self.clicked_element = None 
            
    def update_sound(self, value):
        self.assets.click_sound.set_volume(value)
        self.assets.up_click_sound.set_volume(value)
        print(f"Son volume: {value}")

    def update_music(self, value):
        pygame.mixer.music.set_volume(value)
        print(f"Musique volume: {value}")

    def update_theme(self, value):
        print(f"Theme: {value}")
        self.update_theme_callback(value)
        for element in self.elements:
            if isinstance(element, Dropdown) and element.label == "Thème":
                element.options = [self.assets.theme for self.assets.theme in self.assets.THEMES if self.assets.theme != self.assets.THEME]

    def update_resolution(self, value):
        self.update_resolution_callback(value)
        print(f"Resolution: {value}")
        for element in self.elements:
            if isinstance(element, Dropdown) and element.label == "Résolution":
                element.options = [self.assets.resolution for self.assets.resolution in self.assets.RESOLUTIONS if self.assets.resolution != self.assets.RESOLUTION]

    def update_dropdown(self):
        for element in self.elements:
            if isinstance(element, Dropdown) and element.label == "Thème":
                element.options = [self.assets.theme for self.assets.theme in self.assets.THEMES if self.assets.theme != self.assets.THEME]
            elif isinstance(element, Dropdown) and element.label == "Résolution":
                element.options = [self.assets.resolution for self.assets.resolution in self.assets.RESOLUTIONS if self.assets.resolution != self.assets.RESOLUTION]
            
    def update_elements(self):
        self.create_elements()

    def confirm(self):
        print("Options confirmées")
        self.change_menu_callback("main")
    
    def get_sliders(self) -> list:
        sliders = []
        for element in self.elements:
            if type(element) == Slider:
                sliders.append(element)
        return sliders
    
    def get_volume(self) -> dict:
        data = {}
        for slider in self.get_sliders():
            if slider.label == "Son":
                data["sfx"] = slider.value
            elif slider.label == "Musique":
                data["music"] = slider.value
        return data

    def set_volume(self, data: dict) -> None:
        for slider in self.get_sliders():
            if slider.label == "Son":
                slider.value = data["sfx"]
            elif slider.label == "Musique":
                slider.value = data["music"]
