import pygame

class Button:
    def __init__(self, text, x, y, image, image_click, callback, assets, text_color=(255, 255, 255), font=32, margin_left=None):
        self.assets = assets
        self.text = text
        self.image = image
        self.image_default = image
        self.image_click = image_click
        self.rect = self.image.get_rect(topleft=(x, y))
        self.callback = callback
        self.font = font
        self.text_color = text_color
        self.text_surf = self.assets.get_custom_font(font).render(text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect()
        
        # Calculate margin_left if it's None
        if margin_left is None:
            margin_left = (self.rect.width - self.text_rect.width) // 2
        
        self.margin_left = margin_left
        self.update_text_position()

    def update_text_position(self):
        # Center the text in the vertical direction
        self.text_rect.centery = self.rect.centery
        # Align the text to the left with the specified margin
        self.text_rect.x = self.rect.x + self.margin_left

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        screen.blit(self.text_surf, self.text_rect.topleft)

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def on_click(self):
        self.image = self.image_click
        self.assets.click_sound.play()

    def up_click(self):
        self.assets.up_click_sound.play()
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
