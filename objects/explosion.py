import pygame
import pygame.sprite

class Explosion(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group, local_x: int, local_y: int, pos: tuple, size: float = 1, origine = None) -> None:
        super().__init__(group)
        self.origine = origine
        self.image = pygame.image.load('assets/tir/explosion/explo-1.png')
        self.rect = self.image.get_rect()
        self.rect.x = local_x
        self.rect.y = local_y
        self.hitbox = pygame.Rect(
            self.rect.x,
            self.rect.y,
            self.rect.width,
            self.rect.height
        )
        self.__pos = pos
        
        self.__size = size
        
        self.__frame = 1
        self.__frame_speed = 3
        self.__frame_timer = 0
        
        self.__exploded = False
        self.memory = []
        
    # Geter / Seter
    
    def get_pos(self) -> tuple:
        return self.__pos
    def set_pos(self, pos: tuple) -> None:
        self.__pos = pos
    
    def get_size(self) -> float:
        return self.__size
    def set_size(self, size: float) -> None:
        self.__size = size
    
    def get_frame(self) -> int:
        return self.__frame
    def set_frame(self, frame: int) -> None:
        self.__frame = frame
        
    def get_frame_speed(self) -> int:
        return self.__frame_speed
    def set_frame_speed(self, frame_speed: int) -> None:
        self.__frame_speed = frame_speed
        
    def get_frame_timer(self) -> int:
        return self.__frame_timer
    def set_frame_timer(self, frame_timer: int) -> None:
        self.__frame_timer = frame_timer
    
    def get_exploded(self) -> bool:
        return self.__exploded
    
    # Méthodes
    
    def explode(self) -> bool:
        self.__frame_timer += 1
        if self.__frame_timer == self.__frame_speed:
            self.__frame_timer = 0
            self.__frame += 1
        if self.__frame == 7:
            self.__exploded = True
            return True
        self.image = pygame.image.load(f"assets/tir/explosion/explo-{self.__frame}.png")
        size = (self.image.get_rect().width * self.get_size(),
                self.image.get_rect().height * self.get_size())
        self.image = pygame.transform.scale(self.image, size)
        new_rect = self.image.get_rect()
        new_rect.x = self.rect.x
        new_rect.y = self.rect.y
        self.rect = new_rect
        self.hitbox = pygame.Rect(
            self.rect.x,
            self.rect.y,
            self.rect.width,
            self.rect.height
        )
        return False

    def sync_vel(self, velocity: float, left: bool, right: bool) -> None:
        # Bouge de la même manière que la map
        if not left and not right:
            self.rect.x -= velocity
            self.hitbox.x -= velocity