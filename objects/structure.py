import pygame
import objects.civil as civil

class Structure(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group, local_x: int, local_y: int, pos: tuple, type: str, theme: str) -> None:
        super().__init__(group)
        self.__pos = pos
        self.__type = type
        self.__theme = theme
        
        self.__destroyed = False
        self.__civils_group = pygame.sprite.Group()
        self.__civils_list = []
        
        self.image = pygame.image.load(f"assets/structure/{self.__type}/{self.__theme}.png")
        self.rect = self.image.get_rect()
        self.rect.x = local_x
        self.rect.y = local_y

    # Geter / Seter
    
    def get_pos(self) -> tuple:
        return self.__pos
    def set_pos(self, pos: tuple) -> None:
        self.__pos = pos
    
    def get_type(self) -> int:
        return self.__type
    def set_type(self, type: int) -> None:
        self.__type = type
    
    def get_theme(self) -> int:
        return self.__theme
    def set_theme(self, theme: int) -> None:
        self.__theme = theme
    
    def get_destroyed(self) -> bool:
        return self.__destroyed
    def set_destroyed(self, destroyed: bool) -> None:
        self.__destroyed = destroyed
    
    def get_civils_list(self) -> list:
        return self.__civils_list
    def set_civils_list(self, list: list) -> None:
        self.__civils_list = list
    
    # Méthodes
    
    def sync_vel(self, velocity: float, left: bool, right: bool) -> None:
        # Bouge de la même manière que la map
        if not left and not right:
            self.rect.x -= velocity
        # Synchrnise également les civils
        for civil in self.__civils_list:
            civil.sync_vel(velocity, left, right)
    
    def add_civil(self) -> None:
        self.__civils_list.append(civil.Civil(self.__civils_group, self.rect.x, self.rect.y - 20, self.__pos, "Female", 1, 1))
    
    def hit(self) -> None:
        if not self.__destroyed:
            self.__destroyed = True
            self.image = pygame.image.load(f"assets/structure/{self.__type}/{self.__theme}-decombres.png")
            self.add_civil()
    
    def handle(self, map_size: int) -> None:
        # Gérer les civils
        for civil in self.__civils_list:
            civil.handle(map_size)
    
    def afficher_civils(self, screen: pygame.Surface) -> None:
        self.__civils_group.draw(screen)