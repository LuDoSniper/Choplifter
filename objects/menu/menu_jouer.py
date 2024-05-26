from objects.menu.button import Button
import pygame

class MenuJouer:
    def __init__(self, screen, change_menu_callback, assets):
        self.assets = assets
        self.screen = screen
        self.change_menu_callback = change_menu_callback
        self.buttons = []
        self.create_buttons()

    def draw(self):
        bg_x = (self.assets.SCREEN_WIDTH - self.assets.background_menu_jouer.get_width()) // 2
        bg_y = (self.assets.SCREEN_HEIGHT - self.assets.background_menu_jouer.get_height()) // 2
        self.screen.blit(self.assets.background_menu_jouer, (bg_x, bg_y))

        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos)
            button.draw(self.screen)

    def create_buttons(self):
        button_width = self.assets.bouton_jouer.get_width()
        button_height = self.assets.bouton_jouer.get_height()
        spacing = 20
        total_height = 4 * button_height + 3 * spacing

        start_y = ((self.assets.SCREEN_HEIGHT - total_height) // 2) + 30
        start_x = (self.assets.SCREEN_WIDTH - button_width) // 2

        self.buttons.append(Button('SOLO', start_x, start_y, self.assets.bouton, self.start_solo, self.assets))
        self.buttons.append(Button('DUEL', start_x, start_y + button_height + spacing, self.assets.bouton, self.start_duel, self.assets))
        self.buttons.append(Button('SANDBOX', start_x, start_y + 2 * (button_height + spacing), self.assets.bouton, self.start_entrainement, self.assets))
        self.buttons.append(Button('RETOUR', start_x, start_y + 3 * (button_height + spacing), self.assets.bouton_jouer, lambda: self.change_menu_callback("main"),self.assets, self.assets.JAUNE))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button.is_hovered(event.pos):
                    response = button.on_click()
                    if response is not None:
                        return response

    def start_solo(self):
        print("Lance solo")
        return "solo"

    def start_duel(self):
        print("Lance duel")

    def start_entrainement(self):
        print("Lance sandbox")