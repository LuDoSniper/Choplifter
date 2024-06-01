import pygame

class Button:
    def __init__(self, text, x, y, image, image_click, callback, assets, text_color=(255, 255, 255)):
        self.assets = assets
        self.text = text
        self.image = image
        self.image_default = image
        self.image_click = image_click
        self.rect = self.image.get_rect(topleft=(x, y))
        self.callback = callback
        self.text_color = text_color
        self.text_surf = self.assets.custom_font_32.render(text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        screen.blit(self.text_surf, self.text_rect)

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def on_click(self):
        self.image = self.image_click
        self.assets.click_sound.play()

    def up_click(self):
        return self.callback()

    def update(self, mouse_pos):
        pass

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.image = self.image_click
                self.on_click()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.image == self.image_click: 
                self.image = self.image_default
                if self.rect.collidepoint(event.pos):
                    self.up_click()