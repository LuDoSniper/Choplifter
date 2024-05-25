import pygame

class Health(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group, screen: pygame.Surface) -> None:
        super().__init__(group)
        self.__screen = screen
        self.image = pygame.image.load("assets/hud_ig/health-2.png")
        self.image = pygame.transform.scale(self.image, (15, 15))
        self.rect = self.image.get_rect()
        self.rect.x = 12
        self.rect.y = 12
        self.health_rect_border = (9, 9, 102, 22)
        self.health_rect = (10, 10, 100, 20)
    
    def afficher(self, health: int):
        self.health_rect = (self.health_rect[0], self.health_rect[1], health, self.health_rect[3])
        pygame.draw.rect(self.__screen, (63, 118, 40), self.health_rect_border)
        pygame.draw.rect(self.__screen, (103, 226, 93), self.health_rect)

class Fuel(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group, screen: pygame.Surface) -> None:
        super().__init__(group)
        self.__screen = screen
        self.image = pygame.image.load("assets/hud_ig/fuel-2.png")
        self.image = pygame.transform.scale(self.image, (15, 15))
        self.rect = self.image.get_rect()
        self.rect.x = 12
        self.rect.y = 37
        self.fuel_rect_border = (9, 34, 102, 22)
        self.fuel_rect = (10, 35, 100, 20)
    
    def afficher(self, fuel: int):
        self.fuel_rect = (self.fuel_rect[0], self.fuel_rect[1], fuel, self.fuel_rect[3])
        pygame.draw.rect(self.__screen, (131, 102, 27), self.fuel_rect_border)
        pygame.draw.rect(self.__screen, (255, 199, 54), self.fuel_rect)

class HUD():
    def __init__(self, screen: pygame.Surface) -> None:
        self.__screen = screen
        self.__items = pygame.sprite.Group()
        self.__health = Health(self.__items, self.__screen)
        self.__fuel = Fuel(self.__items, self.__screen)
    
    # Geter / Seter
    
    def get_screen(self) -> pygame.Surface:
        return self.__screen
    def set_screen(self, screen: pygame.Surface) -> None:
        self.__screen = screen
    
    # Méthodes
    
    def afficher(self, health: int, fuel: int) -> None:
        self.__health.afficher(health)
        self.__fuel.afficher(fuel)
        
        self.__items.draw(self.__screen)