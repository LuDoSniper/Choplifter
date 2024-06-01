from objects.menu.button import Button
import pygame

class MenuCredits:
    def __init__(self, screen, change_menu_callback, assets):
        self.screen = screen
        self.change_menu_callback = change_menu_callback
        self.assets = assets
        self.create_elements()

    def create_elements(self):
        self.elements = []
        self.elements.append(Button("", (((self.assets.SCREEN_WIDTH + (self.assets.background_menu_credits.get_width() // 2)) // 2) - self.assets.bouton_continue.get_width()), 
                                      (self.assets.background_menu_credits.get_height()), 
                                      self.assets.bouton_continue, self.assets.bouton_continue_click,
                                      self.continuer, self.assets))

    def draw(self):
        bg_x = (self.assets.SCREEN_WIDTH - self.assets.background_menu_credits.get_width()) // 2
        bg_y = (self.assets.SCREEN_HEIGHT - self.assets.background_menu_credits.get_height()) // 2
        self.screen.blit(self.assets.background_menu_credits, (bg_x, bg_y))

        mouse_pos = pygame.mouse.get_pos()
        for element in self.elements:
            element.update(mouse_pos)
            element.draw(self.screen)

        dev_surf = self.assets.custom_font_16.render("DEVELOPPE PAR", True, self.assets.GRIS_FONCE)
        self.screen.blit(dev_surf, (bg_x + 135, bg_y + 120))
        names = ["Donnarieix Lucien", "Falchero Maxime", "Da Cunha Mathys"]
        for i, name in enumerate(names):
            name_surf = self.assets.custom_font_16.render(name, True, self.assets.GRIS_CLAIR)
            self.screen.blit(name_surf, (bg_x + 135, bg_y + 140 + i * 20))

        des_surf = self.assets.custom_font_16.render("DESIGNE PAR", True, self.assets.GRIS_FONCE)
        self.screen.blit(des_surf, (bg_x + 135, bg_y + 220))
        for i, name in enumerate(names):
            name_surf = self.assets.custom_font_16.render(name, True, self.assets.GRIS_CLAIR)
            self.screen.blit(name_surf, (bg_x + 135, bg_y + 240 + i * 20))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for element in self.elements:
                if element.is_hovered(event.pos):
                    self.clicked_element = element
                    element.on_click()
        elif event.type == pygame.MOUSEBUTTONUP:
            for element in self.elements:
                if element == self.clicked_element:
                    element.image = element.image_default
                    if element.is_hovered(event.pos):
                        element.up_click()
            self.clicked_element = None 

    def continuer(self):
        self.change_menu_callback("main")