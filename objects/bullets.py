import pygame
import math

class Bullet(pygame.sprite.Sprite):
    
    SPEED = 5
    
    def __init__(self, group: pygame.sprite.Group, dir: int, angle: int, pos: tuple, local_x: int, local_y: int) -> None:
        super().__init__(group)
        self.image = pygame.image.load("assets/imgs/Bullet_tmp_4x4.png")
        self.rect = self.image.get_rect()
        self.rect.x = local_x
        self.rect.y = local_y
        
        self.__dir = dir
        self.__angle = angle
        self.__pos = pos
        self.__local_x = local_x
    
    # Geter / Seter
    def get_dir(self) -> int:
        return self.__dir
    def ste_dir(self, dir: int) -> None:
        self.__dir = dir
    
    def get_angle(self) -> int:
        return self.__angle
    def set_angle(self, angle: int) -> None:
        self.__angle = angle
    
    def get_pos(self) -> tuple:
        return self.__pos
    def set_pos(self, pos: tuple) -> None:
        self.__pos = pos
    
    def get_local_x(self) -> int:
        return self.__local_x
    def set_local_x(self, local_x: int) -> None:
        self.__local_x = local_x

    # Méthodes
    def move(self) -> None:
        self.set_pos((self.get_pos()[0] + self.SPEED * self.get_dir(), self.get_pos()[1]))
        # tmp = 1
        # if self.get_angle() < 0:
        #     tmp = -1
        # angle = (abs(self.get_angle()) - 90) * tmp
        self.rect.x += self.SPEED * math.sin(math.radians(self.get_angle()))
        self.rect.y -= self.SPEED * math.cos(math.radians(self.get_angle()))
    
    def sync_vel(self, velocity: float, left: bool, right: bool) -> None:
        # Bouge de la même manière que la map
        if not left and not right:
            self.rect.x -= velocity