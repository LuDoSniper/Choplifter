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
        self.health_rect_border = (9, 9, 152, 22)
        self.health_rect = (10, 10, 150, 20)
    
    def afficher(self, health: int):
        self.health_rect = (self.health_rect[0], self.health_rect[1], health / 100 * 150, self.health_rect[3])
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
        self.fuel_rect_border = (9, 34, 152, 22)
        self.fuel_rect = (10, 35, 150, 20)
    
    def afficher(self, fuel: int):
        self.fuel_rect = (self.fuel_rect[0], self.fuel_rect[1], fuel / 100 * 150, self.fuel_rect[3])
        pygame.draw.rect(self.__screen, (131, 102, 27), self.fuel_rect_border)
        pygame.draw.rect(self.__screen, (255, 199, 54), self.fuel_rect)

class Civil_Background(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group, pos: tuple) -> None:
        super().__init__(group)
        self.image = pygame.image.load("assets/hud_ig/ottages.png")
        self.image = pygame.transform.scale(self.image, (75, 20))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

class Logo(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group, logo: str, pos: tuple) -> None:
        super().__init__(group)
        self.image = pygame.image.load(f"assets/hud_ig/{logo}.png")
        self.image = pygame.transform.scale(self.image, (15, 15))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

class Saved():
    def __init__(self, group: pygame.sprite.Group, screen: pygame.Surface) -> None:
        super().__init__(group)
        self.image = None

class Stored():
    def __init__(self, screen: pygame.Surface) -> None:
        self.__screen = screen
        self.__items = pygame.sprite.Group()
        self.__background = Civil_Background(self.__items, (86, 60))
        self.__logo = Logo(self.__items, "storage", ((152 + 10) - 19, 62))
        self.__font = pygame.font.Font("assets/font/kenvector_future.ttf", 12)
    
    def afficher(self, stored: int, max_storage: int) -> None:
        self.__items.draw(self.__screen)
        font_surface = self.__font.render(f"{stored}/{max_storage}", True, (255, 255, 255))
        font_rect = font_surface.get_rect()
        font_rect.x, font_rect.y = (
            (self.__background.rect.width + 10 + 4) + ((self.__background.rect.width - (15 + 2 * 2)) / 2) - font_rect.width / 2,
            60 + (font_rect.height / 5)
        )
        self.__screen.blit(font_surface, font_rect)
        

class HUD():
    def __init__(self, screen: pygame.Surface) -> None:
        self.__screen = screen
        self.__items = pygame.sprite.Group()
        self.__health = Health(self.__items, self.__screen)
        self.__fuel = Fuel(self.__items, self.__screen)
        self.__stored = Stored(self.__screen)
    
    # Geter / Seter
    
    def get_screen(self) -> pygame.Surface:
        return self.__screen
    def set_screen(self, screen: pygame.Surface) -> None:
        self.__screen = screen
    
    # Méthodes
    
    def afficher(self, health: int, fuel: int, stored: int, max_storage: int) -> None:
        self.__health.afficher(health)
        self.__fuel.afficher(fuel)
        self.__stored.afficher(stored, max_storage)
        
        self.__items.draw(self.__screen)