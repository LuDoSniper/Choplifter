import pygame

class Helicopter():
    def __init__(self, screen):
        self.maxspeed = 5
        self.velocity = 0
        self.resistance = 0.9
        self.acceleration = 0.5
        self.flipped = False
        self.image = pygame.image.load("assets/imgs/Helicopter_tmp.png")
        self.image = pygame.transform.scale(self.image, (50, 20))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = screen.get_width() / 2, screen.get_height() / 2
    
    def inertie(self):
        self.velocity *= self.resistance
    
    def afficher(self, screen):
        # Gérer le sens
        if self.velocity != 0: # Vérifier que l'helico est bien en mouvement
            # Tourner à gauche si tourné à droite
            if self.velocity < 0 and not self.flipped:
                self.flipped = True
                self.flip()
            # Tourner à droite si tourné à gauche
            elif self.velocity > 0 and self.flipped:
                self.flipped = False
                self.flip()
        
        # Affichage
        screen.blit(self.image, self.rect)
    
    def changer_velocity(self, dir):
        self.velocity += dir * self.acceleration
        
        # Brider la vitesse
        if self.velocity > self.maxspeed:
            self.velocity = self.maxspeed
        elif self.velocity < -self.maxspeed:
            self.velocity = -self.maxspeed
    
    def deplacer(self):
        self.rect.x += self.velocity
    
    def flip(self):
        self.image = pygame.transform.flip(self.image, True, False)