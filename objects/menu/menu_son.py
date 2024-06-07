from objects.menu.button import Button
from objects.menu.slider import Slider
import pygame
import objects.saver as saver

class MenuSon:
    def __init__(self, screen, change_menu_callback, assets):
        self.assets = assets
        self.screen = screen
        self.change_menu_callback = change_menu_callback
        self.clicked_element = None 
        self.elements = []
        self.create_elements()

    def create_elements(self):
        element_height = 50
        spacing = 20 
        num_elements = 5
        
        total_height = (element_height * num_elements) + (spacing * (num_elements - 1))
        
        start_y = (self.assets.SCREEN_HEIGHT - total_height) // 2
        
        current_y = start_y
        
        current_y += (element_height + spacing) // 2

        self.elements.append(Slider("Son", (self.assets.SCREEN_WIDTH - self.assets.background_menu.get_width()) // 2, current_y, 350, 8, self.update_sound, self.assets, self.assets.sfx_volume))
        current_y += element_height + spacing
        
        self.elements.append(Slider("Musique", (self.assets.SCREEN_WIDTH - self.assets.background_menu.get_width()) // 2, current_y, 350, 8, self.update_music, self.assets, self.assets.music_volume))
        current_y += element_height + spacing

        self.elements.append(Button("", (self.assets.SCREEN_WIDTH - self.assets.background_menu.get_width()) // 2, current_y, self.assets.bouton_confirm, self.assets.bouton_confirm_click, self.confirm, self.assets))

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
                elif isinstance(element, Slider):
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
        self.assets.set_sfx_sound(value)
        print(f"Son volume: {value}")

    def update_music(self, value):
        pygame.mixer.music.set_volume(value)
        print(f"Musique volume: {value}")

    def confirm(self):
        print("Options confirmées")
        save_manager = saver.Saver()
        data = save_manager.load()
        volumes = self.get_volume()
        data["music"] = volumes["music"]
        data["sfx"] = volumes["sfx"]
        save_manager.save(data)
        self.change_menu_callback("pause")
    
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
