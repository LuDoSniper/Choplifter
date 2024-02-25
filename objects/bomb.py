import pygame

class Bomb(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group, pos: tuple, local_pos: tuple, screen: pygame.Surface) -> None:
        super().__init__(group)
        self.image = pygame.image.load("assets/imgs/Bomb_tmp_7x20.png")
        self.rect = self.image.get_rect()
        self.rect.x = local_pos[0]
        
        self.__speed = 2
        self.__pos = pos
        
        self.__expolded = False
    
    # Geter / Seter
    def get_speed(self) -> float:
        return self.__speed
    def set_speed(self, speed: float) -> None:
        self.__speed = speed
    
    def get_pos(self) -> tuple:
        return self.__pos
    def set_pos(self, pos: tuple) -> None:
        self.__pos = pos
    
    def get_exploded(self) -> bool:
        return self.__expolded
    def set_exploded(self, exploded: bool) -> None:
        self.__expolded = exploded
    
    # Méthodes
    def fall(self) -> None:
        self.rect.y += self.get_speed()
        if self.rect.y >= 4 * 32: # Temporaire
            self.set_exploded(True)
    
    def sync_vel(self, velocity: float, left: bool, right: bool) -> None:
        # Bouge de la même manière que la map
        if not left and not right:
            self.rect.x -= velocity