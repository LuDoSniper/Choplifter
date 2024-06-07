from objects.menu.button import Button
import pygame
from typing import List, Dict, Callable, Tuple

class MenuMission:
    def __init__(self, screen: pygame.Surface, change_menu_callback: Callable, assets: object, missions: Dict[str, List[bool]], monde: str):
        self.screen = screen
        self.change_menu_callback = change_menu_callback
        self.assets = assets
        self.missions = missions
        self.monde = monde
        self.buttons = []
        self.quit_button = None
        self.clicked_element = None
        self.circle_positions = [(71, 219), (266, 178), (107, 111), (250, 14)]
        self.create_buttons()
        self.spacing = 10

    def draw(self):
        map_dimension = 350
        bg_x = (self.assets.SCREEN_WIDTH - self.assets.background_menu_mission.get_width()) // 2
        bg_y = (self.assets.SCREEN_HEIGHT - self.assets.background_menu_mission.get_height()) // 2

        map_x = bg_x + (self.assets.background_menu_mission.get_width() // 2) + self.spacing
        map_y = (self.assets.SCREEN_HEIGHT - map_dimension) // 2

        map_image = pygame.transform.scale(self.assets.map, (map_dimension, map_dimension))
        map_rect = map_image.get_rect(topleft=(map_x, map_y))
        
        self.screen.blit(map_image, map_rect)

        self.screen.blit(self.assets.background_menu_mission, (bg_x - (self.assets.background_menu_mission.get_width() // 2) - self.spacing, bg_y))
        
        monde_text = self.assets.get_custom_font(16).render(self.monde, True, self.assets.GRIS_FONCE)
        monde_text_rect = monde_text.get_rect(center=(bg_x - self.spacing // 2, bg_y + self.assets.background_menu_mission.get_height() // 5))
        self.screen.blit(monde_text, monde_text_rect)

        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos)
            button.draw(self.screen)
        
        if self.quit_button:
            self.quit_button.update(mouse_pos)
            self.quit_button.draw(self.screen)

        for idx, (monde, test) in enumerate(list(self.missions.items())):
            circle_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
            if monde == self.monde:
                color = (78, 216, 101, 255)
            elif test[0]:
                color = (0, 0, 0, 0)
            else:
                color = (0, 0, 0, 150)
            
            pygame.draw.circle(circle_surface, color, (20, 20), 11)
            self.screen.blit(circle_surface, (map_x + self.circle_positions[idx][0] - 20, map_y + self.circle_positions[idx][1] - 20))

    def create_buttons(self):
        monde_missions = self.missions[self.monde]
        
        original_button_width = self.assets.bouton_unlock.get_width()
        original_button_height = self.assets.bouton_unlock.get_height()
        button_width = original_button_width // 1.25
        button_height = original_button_height // 1.25

        spacing_buttons = 15 
        button_x = (((self.assets.SCREEN_WIDTH - self.assets.background_menu_mission.get_width()) // 2) - self.assets.background_menu_mission.get_width() // 2) + ((self.assets.background_menu_mission.get_width() - button_width) // 2) - 10
        y_start = (self.assets.SCREEN_HEIGHT - (len(monde_missions) * (button_height + spacing_buttons)) + spacing_buttons) // 2 + 50
        x_center = self.assets.SCREEN_WIDTH // 2
        text_offset_x = 80

        self.buttons = []
        for i, mission_unlocked in enumerate(monde_missions):
            button_image = pygame.transform.scale(self.assets.bouton_unlock, (button_width, button_height))
            button_image_click = pygame.transform.scale(self.assets.bouton_unlock_clicked, (button_width, button_height))
            if mission_unlocked:
                action = lambda m=i+1: self.start_mission(m)
            else:
                action = None

            button_y = y_start + i * (button_height + spacing_buttons)
            button = Button(f'Mission {i + 1}', button_x, button_y, button_image, button_image_click, action, self.assets, (255, 255, 255), 20, text_offset_x)
            
            if not mission_unlocked:
                self.apply_lock_filter(button.image, button_width, button_height)
                button.on_click = None

            self.buttons.append(button)

        quit_button_image = pygame.transform.scale(self.assets.bouton, (button_width, button_height))
        quit_button_image_click = pygame.transform.scale(self.assets.bouton_click, (button_width, button_height))
        quit_button_x = x_center - button_width // 2
        quit_button_y = y_start + len(monde_missions) * (button_height + spacing_buttons) + 20
        self.quit_button = Button('Retour', quit_button_x, quit_button_y, quit_button_image, quit_button_image_click, lambda: self.change_menu_callback("play"), self.assets, (255, 255, 255), 20)

    def apply_lock_filter(self, surface, button_width, button_height):
        lock_image = pygame.transform.scale(self.assets.bouton_lock, (button_width, button_height))
        surface.blit(lock_image, (0, 0))

    def variable_exists(self, var_name):
        return hasattr(self, var_name)

    def handle_event(self, event):
        map_dimension = 350
        bg_x = (self.assets.SCREEN_WIDTH - self.assets.background_menu_mission.get_width()) // 2
        map_x = bg_x + (self.assets.background_menu_mission.get_width() // 2) + self.spacing
        map_y = (self.assets.SCREEN_HEIGHT - map_dimension) // 2
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button.is_hovered(event.pos) and button.on_click is not None:
                    self.clicked_element = button
                    button.on_click()
                elif button.is_hovered(event.pos) and button.on_click is None:
                    self.assets.error.play()
            if self.quit_button and self.quit_button.is_hovered(event.pos):
                self.clicked_element = self.quit_button
                self.quit_button.on_click()

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.variable_exists('clicked_element') and self.clicked_element is not None:
                for button in self.buttons:
                    if button == self.clicked_element:
                        button.image = button.image_default
                        if button.is_hovered(event.pos) and button.up_click is not None:
                            response = button.up_click()
                            if response is not None:
                                return response
                if self.quit_button == self.clicked_element:
                    self.quit_button.image = self.quit_button.image_default
                    self.quit_button.up_click()
                self.clicked_element = None
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for idx, (monde, test) in enumerate(list(self.missions.items())):
                position = self.circle_positions[idx]
                if pygame.Rect(map_x + position[0] - 20, map_y + position[1] - 20, 40, 40).collidepoint(event.pos) and test[0]:
                    self.monde = monde
                    self.create_buttons()
                    self.assets.up_click_sound.play()
                    break
                elif pygame.Rect(map_x + position[0] - 20, map_y + position[1] - 20, 40, 40).collidepoint(event.pos): 
                    self.assets.error.play()

    def start_mission(self, mission_number):
        print(f"Mission {mission_number} dans le {self.monde} démarrée")
        return f"{self.monde.split('-')[0]}-{mission_number}"

    def set_missions(self, data_missions: dict) -> None:
        self.missions = data_missions
        self.create_buttons()
