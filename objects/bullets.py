import pygame
import math
import objects.tank as tank
import objects.avion as avion
import objects.heli as heli

class Bullet(pygame.sprite.Sprite):
    
    SPEED = 5
    
    def __init__(self, group: pygame.sprite.Group, screen: pygame.Surface, dir: int, angle: int, pos: tuple, local_x: int, local_y: int, boost: int = 0, name: str = "missile-joueur") -> None:
        super().__init__(group)
        self.image = pygame.image.load(f"assets/tir/missiles/{name}.png")
        if name == "balle-avion":
            self.image = pygame.transform.scale(self.image, (self.image.get_rect().width * 0.75,
                                                             self.image.get_rect().height * 0.75))
        self.rect = self.image.get_rect()
        self.rect.x = local_x
        self.rect.y = local_y + 10
        self.__screen = screen
        
        self.__boost = boost
        
        self.__dir = dir
        self.__angle = angle
        self.__pos = pos
        self.__local_x = local_x
        
        self.__exploded = False
        
        # Mettre dans le bon sens l'image (mirroir)
        if dir == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        
        # Faire rotate l'image
        if angle < 0:
            signe = -1
        else:
            signe = 1
        self.image = pygame.transform.rotate(self.image, -(angle - 90 * signe))
        
        # Faire partir le tir du nez de l'helico
        if dir != 1:
            self.rect.x += 8 * self.SPEED + self.__boost
        for i in range(0, 8):
            self.move()
    
    # Geter / Seter
    
    def get_screen(self) -> pygame.Surface:
        return self.__screen
    def set_screen(self, screen: pygame.Surface) -> None:
        self.__screen = screen
    
    def get_boost(self) -> int:
        return self.__boost
    def set_boost(self, boost: int) -> None:
        self.__boost = boost
    
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

    def get_exploded(self) -> bool:
        return self.__exploded
    def set_exploded(self, exploded: bool) -> None:
        self.__exploded = exploded

    # Méthodes
    def move(self, targets: list = []) -> None:
        self.set_pos((self.get_pos()[0] + (self.SPEED + self.__boost) * self.get_dir(), self.get_pos()[1]))
        # tmp = 1
        # if self.get_angle() < 0:
        #     tmp = -1
        # angle = (abs(self.get_angle()) - 90) * tmp
        self.rect.x += (self.SPEED + self.__boost) * math.sin(math.radians(self.get_angle()))
        self.rect.y -= (self.SPEED + self.__boost) * math.cos(math.radians(self.get_angle()))
        
        # Explosion
        for target in targets:
            if type(target) != heli.Heli and self.rect.colliderect(target.rect): # Collision
                self.set_exploded(True)
                if type(target) == tank.Tank or type(target) == avion.Avion:
                    if target.hit():
                        target.set_exploded(True)
                else:
                    target.set_exploded(True)
            elif type(target) == heli.Heli and self.rect.colliderect(target.get_rect()):
                self.set_exploded(True)
        if self.rect.x <= 0 - self.rect.width or self.rect.x >= self.__screen.get_width() + self.rect.width or self.rect.y < -100:
            self.set_exploded(True)
    
    def sync_vel(self, velocity: float, left: bool, right: bool) -> None:
        # Bouge de la même manière que la map
        if not left and not right:
            self.rect.x -= velocity