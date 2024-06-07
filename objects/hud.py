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
    def __init__(self, group: pygame.sprite.Group, pos: tuple, size: tuple, color: str) -> None:
        super().__init__(group)
        self.__size = size
        self.__color = color
        self.image = pygame.image.load(f"assets/hud_ig/ottages-{self.__color}.png")
        self.image = pygame.transform.scale(self.image, self.__size)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

    def update(self, color: str) -> None:
        self.__color = color
        self.image = pygame.image.load(f"assets/hud_ig/ottages-{self.__color}.png")
        self.image = pygame.transform.scale(self.image, self.__size)

class Logo(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group, logo: str, pos: tuple, size: tuple) -> None:
        super().__init__(group)
        self.image = pygame.image.load(f"assets/hud_ig/{logo}.png")
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

class Saved():
    def __init__(self, screen: pygame.Surface, color: str) -> None:
        self.__screen = screen
        self.__color = color
        self.__items = pygame.sprite.Group()
        self.__background = Civil_Background(self.__items, (self.__screen.get_width() - 75 - 10, 10), (75, 20), self.__color)
        self.__logo = Logo(self.__items, "people-vector-2", (self.__screen.get_width() - 30 - 10 - 2, 12), (30, 15))
        self.__font = pygame.font.Font("assets/font/kenvector_future.ttf", 12)
    
    def update(self, color: str) -> None:
        self.__color = color
        self.__background.update(self.__color)
    
    def afficher(self, saved: int, max_civil: int) -> None:
        self.__items.draw(self.__screen)
        font_surface = self.__font.render(f"{saved}/{max_civil}", True, (255, 255, 255))
        font_rect = font_surface.get_rect()
        font_rect.x, font_rect.y = (
            self.__background.rect.x + ((self.__background.rect.width - 2 * 2 - self.__logo.rect.width) / 2) - font_rect.width / 2,
            self.__background.rect.y + self.__background.rect.height / 2 - font_rect.height / 2
        )
        self.__screen.blit(font_surface, font_rect)

class Dead():
    def __init__(self, screen: pygame.Surface, color: str) -> None:
        self.__screen = screen
        self.__color = color
        self.__items = pygame.sprite.Group()
        self.__background = Civil_Background(self.__items, (self.__screen.get_width() - 75 - 10, 35), (75, 20), self.__color)
        self.__logo = Logo(self.__items, "dead-2", (self.__screen.get_width() - 15 - 10 - 2, 37), (15, 15))
        self.__font = pygame.font.Font("assets/font/kenvector_future.ttf", 12)
    
    def update(self, color: str) -> None:
        self.__color = color
        self.__background.update(self.__color)
    
    def afficher(self, dead: int, max_civil: int) -> None:
        self.__items.draw(self.__screen)
        font_surface = self.__font.render(f"{dead}/{max_civil}", True, (255, 255, 255))
        font_rect = font_surface.get_rect()
        font_rect.x, font_rect.y = (
            self.__background.rect.x + ((self.__background.rect.width - 2 * 2 - self.__logo.rect.width) / 2) - font_rect.width / 2,
            self.__background.rect.y + self.__background.rect.height / 2 - font_rect.height / 2
        )
        self.__screen.blit(font_surface, font_rect)

class Try():
    def __init__(self, screen: pygame.Surface, color: str, nb_try: int) -> None:
        self.__screen = screen
        self.__color = color
        self.__items = pygame.sprite.Group()
        self.__background = Civil_Background(self.__items, (10, 60), (75, 20), self.__color)
        self.__logos = []
        self.update_try(nb_try)
    
    def update_try(self, nb_try: int) -> None:
        if self.__logos != []:
            for logo in self.__logos:
                self.__items.remove(logo)
        self.__logos = []
        for i in range(nb_try):
            self.__logos.append(Logo(self.__items, "helico-icon", (((self.__background.rect.width / 4) * (i + 1) - 15 / 2) + 10, 62), (15, 15)))
    
    def update(self, color: str) -> None:
        self.__color = color
        self.__background.update(self.__color)
    
    def afficher(self) -> None:
        self.__items.draw(self.__screen)

class Stored():
    def __init__(self, screen: pygame.Surface, color: str) -> None:
        self.__screen = screen
        self.__color = color
        self.__items = pygame.sprite.Group()
        self.__background = Civil_Background(self.__items, (86, 60), (75, 20), self.__color)
        self.__logo = Logo(self.__items, "storage", ((152 + 10) - 19, 62), (15, 15))
        self.__font = pygame.font.Font("assets/font/kenvector_future.ttf", 12)
    
    def update(self, color: str) -> None:
        self.__color = color
        self.__background.update(self.__color)
    
    def afficher(self, stored: int, max_storage: int) -> None:
        self.__items.draw(self.__screen)
        font_surface = self.__font.render(f"{stored}/{max_storage}", True, (255, 255, 255))
        font_rect = font_surface.get_rect()
        font_rect.x, font_rect.y = (
            (self.__background.rect.width + 10 + 4) + ((self.__background.rect.width - (15 + 2 * 2)) / 2) - font_rect.width / 2,
            60 + (font_rect.height / 5)
        )
        self.__screen.blit(font_surface, font_rect)

class Score():
    def __init__(self, screen: pygame.Surface, color: str) -> None:
        self.__screen = screen
        self.__color = color
        self.__font = pygame.font.Font("assets/font/kenvector_future.ttf", 12)
        self.__group = pygame.sprite.Group()
        self.__background = Civil_Background(self.__group, (self.__screen.get_width() / 2 - 100 / 2, 10), (100, 22), self.__color)

    def update(self, color: str) -> None:
        self.__color = color
        self.__background.update(self.__color)

    def afficher(self, score: int):
        self.__group.draw(self.__screen)
        font_surface = self.__font.render(f"Score : {score}", True, (255, 255, 255))
        font_rect = font_surface.get_rect()
        font_rect.x = self.__background.rect.x + self.__background.rect.width / 2 - font_rect.width / 2
        font_rect.y = 10 + self.__background.rect.height / 2 - font_rect.height / 2
        self.__screen.blit(font_surface, font_rect)
   
class HUD():
    def __init__(self, screen: pygame.Surface, color: str, nb_try: int, survival: bool) -> None:
        self.__screen = screen
        self.__color = color
        self.__survival = survival
        self.__items = pygame.sprite.Group()
        self.__health = Health(self.__items, self.__screen)
        self.__fuel = Fuel(self.__items, self.__screen)
        self.__stored = Stored(self.__screen, self.__color)
        self.__saved = Saved(self.__screen, self.__color)
        self.__dead = Dead(self.__screen, self.__color)
        self.__try = Try(self.__screen, self.__color, nb_try)
        if self.__survival:
            self.__score = Score(self.__screen, self.__color)
    
    # Geter / Seter
    
    def get_screen(self) -> pygame.Surface:
        return self.__screen
    def set_screen(self, screen: pygame.Surface) -> None:
        self.__screen = screen
    
    # Méthodes
    
    def update(self, color: str) -> None:
        self.__color = color
        elements = [self.__stored, self.__saved, self.__dead, self.__try]
        if self.__survival:
            elements.append(self.__score)
        for item in elements:
            item.update(self.__color)
    
    def update_try(self, nb_int: int) -> None:
        self.__try.update_try(nb_int)
    
    def afficher(self, health: int, fuel: int, stored: int, max_storage: int, saved: int, max_civil: int, dead: int, score: int) -> None:
        self.__health.afficher(health)
        self.__fuel.afficher(fuel)
        self.__stored.afficher(stored, max_storage)
        self.__saved.afficher(saved, max_civil)
        self.__dead.afficher(dead, max_civil)
        self.__try.afficher()
        if self.__survival:
            self.__score.afficher(score)
        
        self.__items.draw(self.__screen)