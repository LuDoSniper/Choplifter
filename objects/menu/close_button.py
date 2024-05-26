import pygame

class CloseButton:
    def __init__(self, x, y, callback):
        self.image = pygame.image.load('assets/menu/leave.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x - (self.image.get_width() // 2), y))
        self.callback = callback

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()