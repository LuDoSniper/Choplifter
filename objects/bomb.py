import pygame
import objects.tank as tank
import objects.structure as structure
import objects.civil as civil
import objects.terroriste as terroriste
import objects.music as music

class Bomb(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group, pos: tuple, local_pos: tuple, screen: pygame.Surface, min_height: int) -> None:
        super().__init__(group)
        self.__music_manager = music.Music()
        
        self.image = pygame.image.load("assets/imgs/Bomb_tmp_7x20.png")
        self.rect = self.image.get_rect()
        self.rect.x = local_pos[0]
        self.rect.y = local_pos[1]
        self.hitbox = pygame.Rect(
            self.rect.x,
            self.rect.y,
            self.rect.width,
            self.rect.height
        )
        
        self.__screen = screen
        
        self.__speed = 2
        self.__pos = pos
        self.__min_height = min_height - self.rect.height * 1.5
        
        self.__expolded = False
    
    # Geter / Seter
    def get_screen(self) -> pygame.Surface:
        return self.__screen
    def set_screen(self, screen: pygame.Surface) -> None:
        self.__screen = screen
    
    def get_speed(self) -> float:
        return self.__speed
    def set_speed(self, speed: float) -> None:
        self.__speed = speed
    
    def get_min_height(self) -> int:
        return self.__min_height
    def set_min_height(self, min_height: int) -> None:
        self.__min_height = min_height
    
    def get_pos(self) -> tuple:
        return self.__pos
    def set_pos(self, pos: tuple) -> None:
        self.__pos = pos
    
    def get_exploded(self) -> bool:
        return self.__expolded
    def set_exploded(self, exploded: bool) -> None:
        self.__expolded = exploded
    
    # Méthodes
    def fall(self, targets: list) -> None:
        self.rect.y += self.get_speed()
        self.hitbox.y += self.get_speed()
        
        # Explosion
        if self.rect.y > self.__min_height: # Touche le sol
            self.set_exploded(True)
            self.__music_manager.bomb_explode()
        
        for target in targets:
            if self.hitbox.colliderect(target.hitbox): # Collision
                if type(target) == tank.Tank and target.hit(3):
                    target.set_exploded(True)
                elif type(target) in (civil.Civil, terroriste.Terroriste):
                    target.hit()
                elif type(target) == structure.Structure:
                    target.hit(True)
                self.set_exploded(True)
                self.__music_manager.bomb_explode()
    
    def sync_vel(self, velocity: float, left: bool, right: bool) -> None:
        # Bouge de la même manière que la map
        if not left and not right:
            self.rect.x -= velocity
            self.hitbox.x -= velocity