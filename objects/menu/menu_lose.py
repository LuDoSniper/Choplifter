import pygame
import sys
from objects.menu.button import Button

class MenuLose:
    def __init__(self, screen, change_menu_callback, assets):
        self.assets = assets
        self.screen = screen
        self.change_menu_callback = change_menu_callback
        self.buttons = []
        self.clicked_element = None 
        self.create_buttons()

    def draw(self):
        bg_x = (self.assets.SCREEN_WIDTH - self.assets.background_lose.get_width()) // 2
        bg_y = (self.assets.SCREEN_HEIGHT - self.assets.background_lose.get_height()) // 2
        self.screen.blit(self.assets.background_lose, (bg_x, bg_y))

        game_over_text = self.assets.get_custom_font(32).render("PERDU !", True, self.assets.GRIS_FONCE)
        game_over_rect = game_over_text.get_rect(center=(self.assets.SCREEN_WIDTH // 2, bg_y + 50))
        self.screen.blit(game_over_text, game_over_rect)

        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos)
            button.draw(self.screen)

    def create_buttons(self):
        button_width = self.assets.bouton_jouer.get_width()
        button_height = self.assets.bouton_jouer.get_height()
        spacing = 15
        total_height = 2 * button_height + spacing

        start_y = ((self.assets.SCREEN_HEIGHT - total_height) // 2)
        start_x = (self.assets.SCREEN_WIDTH - button_width) // 2

        self.buttons.append(Button('RESTART', start_x, start_y, self.assets.bouton, self.assets.bouton_click, self.restar_game, self.assets))
        self.buttons.append(Button('MISSION', start_x, start_y + button_height + spacing, self.assets.bouton, self.assets.bouton_click, lambda: self.change_menu_callback("mission"), self.assets))
        self.buttons.append(Button('MENU', start_x, start_y + (button_height + spacing) * 2 , self.assets.bouton, self.assets.bouton_click, lambda: self.change_menu_callback("main"), self.assets))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button.is_hovered(event.pos):
                    self.clicked_element = button
                    button.on_click()
                    response = button.on_click()
                    if response is not None:
                        return response
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for button in self.buttons:
                if button == self.clicked_element:
                    button.image = button.image_default
                    if button.is_hovered(event.pos):
                        response = button.up_click()
                        if response is not None:
                            return response
            self.clicked_element = None

    def restar_game(self):
        print("Restart de la partie")
        return "new_try"

    def quit_game(self):
        pygame.quit()
        sys.exit()
