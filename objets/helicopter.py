import pygame

class Helicopter():
    def __init__(self, screen):
        self.speed = 5
        self.image = pygame.image.load("assets/imgs/Helicopter_tmp.png")
        self.image = pygame.transform.scale(self.image, (50, 20))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = screen.get_width() / 2, screen.get_height() / 2
        self.velocity = 0
        self.resistance = 0.9
    
    def inertie(self):
        self.velocity *= self.resistance
    
    def afficher(self, screen):
        screen.blit(self.image, self.rect)
    
    def changer_velocity(self, dir):
        self.velocity = dir * self.speed
    
    def deplacer(self):
        self.rect.x += self.velocity