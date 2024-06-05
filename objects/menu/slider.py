import pygame

class Slider:
    def __init__(self, label, x, y, width, height, callback, assets, value=0):
        self.assets = assets
        self.label = label
        self.rect = pygame.Rect(x, y, width, height)
        self.callback = callback
        self.value = value
        self.dragging = False
        self.cursor_img = pygame.image.load('assets/menu/cursor.png').convert_alpha()

    def draw(self, screen):
        pygame.draw.rect(screen, self.assets.GRIS_CLAIR, self.rect)
        pygame.draw.rect(screen, self.assets.GRIS_FONCE, (self.rect.x, self.rect.y, self.rect.width * self.value, self.rect.height))
        label_surf = self.assets.custom_font_16.render(self.label, True, self.assets.GRIS_CLAIR)
        screen.blit(label_surf, (self.rect.x, self.rect.y - 20))

        cursor_x = self.rect.x + self.rect.width * self.value - self.cursor_img.get_width() // 2
        cursor_y = self.rect.y - (self.cursor_img.get_height() - self.rect.height) // 2
        screen.blit(self.cursor_img, (cursor_x, cursor_y))

        zero_label = self.assets.custom_font_16.render("0", True, self.assets.GRIS_CLAIR)
        hundred_label = self.assets.custom_font_16.render("100", True, self.assets.GRIS_CLAIR)
        screen.blit(zero_label, (self.rect.x, self.rect.y + self.rect.height + 5))
        screen.blit(hundred_label, (self.rect.right - 30, self.rect.y + self.rect.height + 5))

    def update(self, mouse_pos):
        if self.dragging:
            relative_x = mouse_pos[0] - self.rect.x
            self.value = max(0, min(1, relative_x / self.rect.width))
            self.callback(self.value)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        if self.dragging:
            relative_x = event.pos[0] - self.rect.x
            self.value = max(0, min(1, relative_x / self.rect.width))
            self.callback(self.value)

    def update_sound(self, value):
        self.assets.click_sound.set_volume(value)
        print(f"Volume des clicks clicks: {value}")

    def update_music(self, value):
        pygame.mixer.music.set_volume(value)
        print(f"Musique volume: {value}")