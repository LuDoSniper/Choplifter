import pygame

class Dropdown:
    def __init__(self, label, x, y, width, height, options, callback, assets):
        self.assets = assets
        self.label = label
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options
        self.callback = callback
        self.selected_index = 0
        self.expanded = False
        self.dropdown_img = pygame.image.load('assets/menu/dropdown_background.png').convert_alpha()
        self.dropdown_img = pygame.transform.scale(self.dropdown_img, (int(self.dropdown_img.get_width() * 0.7), int(self.dropdown_img.get_height() * 0.7)))

    def draw(self, screen):
        screen.blit(self.dropdown_img, self.rect)
        label_surf = self.assets.custom_font_16.render(self.label, True, self.assets.GRIS_CLAIR)
        screen.blit(label_surf, (self.rect.x, self.rect.y - 20))

        selected_option = self.assets.custom_font_16.render(self.assets.THEME, True, self.assets.GRIS_FONCE)
        screen.blit(selected_option, (self.rect.x + 10, self.rect.y + (self.rect.height - selected_option.get_height()) // 2))

        if self.expanded:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height, self.rect.width, self.rect.height)
                pygame.draw.rect(screen, self.assets.GRIS_CLAIR, option_rect)
                option_surf = self.assets.custom_font_16.render(option, True, (255, 255, 255))
                screen.blit(option_surf, (option_rect.x + 10, option_rect.y + (option_rect.height - option_surf.get_height()) // 2))

    def update(self, mouse_pos):
        pass

    def handle_event(self, event):
        if self.expanded:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height, self.rect.width, self.rect.height)
                if option_rect.collidepoint(event.pos):
                    self.selected_index = i
                    self.callback(self.options[self.selected_index])
                    self.expanded = False
                    return
        if self.rect.collidepoint(event.pos):
            self.expanded = not self.expanded

