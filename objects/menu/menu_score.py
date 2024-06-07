from objects.menu.button import Button
import pygame

class MenuScore:
    def __init__(self, screen, change_menu_callback, assets, classement, positionnement, points_vous):
        self.screen = screen
        self.change_menu_callback = change_menu_callback
        self.assets = assets
        self.classement = classement
        self.positionnement = positionnement
        self.points_vous = points_vous
        self.buttons = []
        self.clicked_element = None
        self.create_buttons()

    def draw(self):
        bg_x = (self.assets.SCREEN_WIDTH - self.assets.background_menu_score.get_width()) // 2
        bg_y = (self.assets.SCREEN_HEIGHT - self.assets.background_menu_score.get_height()) // 2
        self.screen.blit(self.assets.background_menu_score, (bg_x, bg_y))
        
        font = self.assets.get_custom_font(20)
        y_start = 125
        spacing = 50

        if len(self.classement) == 0:
            text = "Le classement est vide !"
            text_surface = font.render(text, True, self.assets.GRIS_FONCE)
            text_rect = text_surface.get_rect(center=(self.assets.SCREEN_WIDTH // 2, self.assets.SCREEN_HEIGHT // 2 - 16))
            self.screen.blit(text_surface, text_rect)
        else:
            for i, (joueur, points) in enumerate(self.classement):
                text = f"TOP {i + 1} : {joueur} - {points} pts"
                text_surface = font.render(text, True, self.assets.GRIS_FONCE)
                text_rect = text_surface.get_rect(center=(self.assets.SCREEN_WIDTH // 2, bg_y + y_start + i * spacing))
                self.screen.blit(text_surface, text_rect)
        
            if self.positionnement == "Aucune données":
                text = "Aucune données sur vous !"
            else:
                text = f"TOP {self.positionnement} : Vous - {self.points_vous} pts"
            text_surface = font.render(text, True, self.assets.GRIS_CLAIR)
            text_rect = text_surface.get_rect(center=(self.assets.SCREEN_WIDTH // 2, bg_y + y_start + len(self.classement) * spacing))
            self.screen.blit(text_surface, text_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos)
            button.draw(self.screen)


    def create_buttons(self):
        multi = 0.8

        button_width = self.assets.bouton_jouer.get_width() * multi
        button_height = self.assets.bouton_jouer.get_height() * multi

        spacing = 10
        font = 20


        y_start = (self.assets.SCREEN_HEIGHT + self.assets.background_menu_score.get_height()) // 2 - self.assets.bouton_continue.get_height() - 20
        x_start = (self.assets.SCREEN_WIDTH - self.assets.background_menu_score.get_width()) / 2  + (self.assets.background_menu_score.get_width() - (button_width * 2 + spacing)) // 2
        self.bouton_survie = pygame.transform.scale(self.assets.bouton, (button_width, button_height))
        self.bouton_click_survie = pygame.transform.scale(self.assets.bouton_click, (button_width, button_height))

        self.buttons.append(Button('RETOUR', x_start, y_start, self.bouton_survie, self.bouton_click_survie, lambda: self.change_menu_callback("play"), self.assets, (255,255,255), font))
        self.buttons.append(Button('JOUER', x_start + button_width + spacing , y_start, self.bouton_survie, self.bouton_click_survie, self.start_survie, self.assets, (255,255,255), font))
        self.buttons.append(Button('', ((self.assets.SCREEN_WIDTH + self.assets.background_menu_score.get_width()) // 2) - (self.assets.fleche_droite.get_width()) + 10, (self.assets.SCREEN_HEIGHT) // 2 - (self.assets.fleche_droite.get_width() // 2) - 10, self.assets.fleche_droite, self.assets.fleche_droite_click, lambda: self.change_menu_callback("palier"), self.assets))

    def variable_exists(self, var_name):
        return hasattr(self, var_name)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button.is_hovered(event.pos):
                    self.clicked_element = button
                    button.on_click()
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.variable_exists('clicked_element') and self.clicked_element is not None:
                for button in self.buttons:
                    if button == self.clicked_element:
                        button.image = button.image_default
                        if button.is_hovered(event.pos):
                            response = button.up_click()
                            if response is not None:
                                return response
                self.clicked_element = None

    def set_scoreboard(self, data: tuple) -> None:
        self.classement = data[0]
        self.positionnement = data[1]
        self.points_vous = data[2]

    def start_survie(self):
        print("Lance survie")
        return "survie"
