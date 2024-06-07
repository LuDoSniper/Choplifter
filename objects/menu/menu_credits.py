from objects.menu.button import Button
import pygame
import webbrowser

class MenuCredits:
    def __init__(self, screen, change_menu_callback, assets):
        self.screen = screen
        self.change_menu_callback = change_menu_callback
        self.assets = assets
        self.clicked_element = None
        self.create_elements()

    def create_elements(self):
        self.elements = []
        button_x = (self.assets.SCREEN_WIDTH - self.assets.bouton_continue.get_width()) // 2
        button_y = (self.assets.SCREEN_HEIGHT + self.assets.background_menu_credits.get_height()) // 2 - self.assets.bouton_continue.get_height() - 20
        discord_button = pygame.image.load(f'assets/menu/bouton_cache.png').convert_alpha()
        discord_button_click = pygame.image.load(f'assets/menu/bouton_cache_click.png').convert_alpha()

        self.elements.append(Button("Rejoindre notre discord", (self.assets.SCREEN_WIDTH - discord_button.get_width()) // 2, button_y - discord_button.get_height() - 5,
                                    discord_button, discord_button_click,
                                    self.get_discord, self.assets, (255,255,255), 16))
        
        self.elements.append(Button("", button_x, button_y,
                                      self.assets.bouton_continue, self.assets.bouton_continue_click,
                                      self.continuer, self.assets))

    def draw(self):
        bg_x = (self.assets.SCREEN_WIDTH - self.assets.background_menu_credits.get_width()) // 2
        bg_y = (self.assets.SCREEN_HEIGHT // 2 - self.assets.background_menu_credits.get_height() // 5)
        self.screen.blit(self.assets.background_menu_credits, (bg_x, (self.assets.SCREEN_HEIGHT - self.assets.background_menu_credits.get_height()) // 2))

        base = 1
        spacing = 20

        mouse_pos = pygame.mouse.get_pos()
        for element in self.elements:
            element.update(mouse_pos)
            element.draw(self.screen)

        dev_surf = self.assets.custom_font_16.render("DEVELOPPE PAR", True, self.assets.GRIS_FONCE)
        dev_surf_rect = dev_surf.get_rect(center=(self.assets.SCREEN_WIDTH // 2, bg_y))
        self.screen.blit(dev_surf, dev_surf_rect.topleft)

        names = ["Donnarieix Lucien", "Falchero Maxime", "Da Cunha Mathys"]
        for i, name in enumerate(names):
            name_surf = self.assets.custom_font_16.render(name, True, self.assets.GRIS_CLAIR)
            name_surf_rect = name_surf.get_rect(center=(self.assets.SCREEN_WIDTH // 2, bg_y + spacing * i + spacing))
            self.screen.blit(name_surf, name_surf_rect.topleft)

        des_surf = self.assets.custom_font_16.render("DESIGNE PAR", True, self.assets.GRIS_FONCE)
        des_surf_rect = des_surf.get_rect(center=(self.assets.SCREEN_WIDTH // 2, bg_y + spacing * 5))
        self.screen.blit(des_surf, des_surf_rect.topleft)

        for i, name in enumerate(names):
            name_surf = self.assets.custom_font_16.render(name, True, self.assets.GRIS_CLAIR)
            name_surf_rect = name_surf.get_rect(center=(self.assets.SCREEN_WIDTH // 2, bg_y + spacing * 5 + spacing * i + spacing))
            self.screen.blit(name_surf, name_surf_rect.topleft)

    def variable_exists(self, var_name):
        return hasattr(self, var_name)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for element in self.elements:
                if element.is_hovered(event.pos):
                    self.clicked_element = element
                    element.on_click()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.variable_exists('clicked_element') and self.clicked_element is not None:
                for element in self.elements:
                    if element == self.clicked_element:
                        element.image = element.image_default
                        if element.is_hovered(event.pos):
                            element.up_click()
                self.clicked_element = None 

    def continuer(self):
        self.change_menu_callback("main")

    def get_discord(self):
        webbrowser.open("https://discord.gg/SNv4enf68V")
