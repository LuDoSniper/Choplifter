import pygame
import sys
from objects.menu.button import Button

class WinStep:
    def __init__(self, screen, change_menu_callback, assets, score, palier):
        self.assets = assets
        self.screen = screen
        self.change_menu_callback = change_menu_callback
        self.score = score
        self.palier = palier
        self.buttons = []
        self.clicked_element = None 
        self.create_buttons()

    def draw(self):
        bg_x = (self.assets.SCREEN_WIDTH - self.assets.background_lose.get_width()) // 2
        bg_y = (self.assets.SCREEN_HEIGHT - self.assets.background_lose.get_height()) // 2
        self.screen.blit(self.assets.background_lose, (bg_x, bg_y))

        game_win_text = self.assets.get_custom_font(32).render("Etape terminé !", True, self.assets.GRIS_FONCE)
        game_win_rect = game_win_text.get_rect(center=(self.assets.SCREEN_WIDTH // 2, bg_y + 50))
        self.screen.blit(game_win_text, game_win_rect)

        score_text = self.assets.get_custom_font(24).render(f"Palier: {self.palier}", True, self.assets.GRIS_CLAIR)
        score_rect = score_text.get_rect(center=(self.assets.SCREEN_WIDTH // 2, game_win_rect.bottom + 40))
        self.screen.blit(score_text, score_rect)

        score_text = self.assets.get_custom_font(24).render(f"Score: {self.score}", True, self.assets.GRIS_CLAIR)
        score_rect = score_text.get_rect(center=(self.assets.SCREEN_WIDTH // 2, game_win_rect.bottom + 90))
        self.screen.blit(score_text, score_rect)

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

        self.buttons.append(Button('SUIVANT', start_x, start_y + button_height + spacing, self.assets.bouton, self.assets.bouton_click, self.next_game, self.assets))
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

    def set_score_palier(self, data: tuple) -> None:
        self.score = data[0]
        self.palier = data[1]

    def next_game(self):
        # print("Lancement de la partie suivante")
        return "survie_next"

    def quit_game(self):
        pygame.quit()
        sys.exit()
