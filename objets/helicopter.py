import pygame

class Helicopter():
    def __init__(self, screen):
        self.speed = 5
        self.image = pygame.image.load("assets/imgs/Helicopter_tmp.png")
        self.image = pygame.transform.scale(self.image, (50, 20))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = screen.get_width() / 2, screen.get_height() / 2
    
    def afficher(self, screen):
        screen.blit(self.image, self.rect)
    
    def deplacer(self, dir):
        self.rect.x += dir * self.speed