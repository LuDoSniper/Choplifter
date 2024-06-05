import pygame
import math
import objects.tank as tank
import objects.avion as avion
import objects.player as player
import objects.structure as structure
import objects.civil as civil
import objects.terroriste as terroriste
import objects.music as music

class Bullet(pygame.sprite.Sprite):
    
    SPEED = 5
    
    def __init__(self, group: pygame.sprite.Group, screen: pygame.Surface, origine, dir: int, angle: int, pos: tuple, local_x: int, local_y: int, boost: int = 0, name: str = "missile-joueur", size: int = 1) -> None:
        super().__init__(group)
        self.__music_manager = music.Music()
        
        self.image = pygame.image.load(f"assets/tir/missiles/{name}.png")
        if name == "balle-avion":
            self.image = pygame.transform.scale(self.image, (self.image.get_rect().width * 0.75,
                                                             self.image.get_rect().height * 0.75))
        else:
            self.image = pygame.transform.scale(self.image, (self.image.get_rect().width * size,
                                                             self.image.get_rect().height * size))
        self.size = size
        self.rect = self.image.get_rect()
        self.rect.x = local_x
        self.rect.y = local_y + 10
        self.hitbox = pygame.Rect(
            self.rect.x,
            self.rect.y,
            self.rect.width,
            self.rect.height
        )
        self.__screen = screen
        
        self.__origine = origine
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
        if type(self.__origine) == player.Player:
            if dir != 1:
                self.rect.x += 8 * self.SPEED + self.__boost
                self.hitbox.x += 8 * self.SPEED + self.__boost
            for i in range(0, 8):
                self.move()
    
    # Geter / Seter
    
    def get_screen(self) -> pygame.Surface:
        return self.__screen
    def set_screen(self, screen: pygame.Surface) -> None:
        self.__screen = screen
    
    def get_origine(self):
        return self.__origine
    def set_origine(self, origine) -> None:
        self.__origine = origine
    
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
        self.hitbox.x += (self.SPEED + self.__boost) * math.sin(math.radians(self.get_angle()))
        self.hitbox.y -= (self.SPEED + self.__boost) * math.cos(math.radians(self.get_angle()))
        
        # Explosion
        for target in targets:
            if type(target) != player.Player and self.hitbox.colliderect(target.hitbox): # Collision
                self.set_exploded(True)
                if type(target) in (tank.Tank, avion.Avion, structure.Structure):
                    if target.hit():
                        target.set_exploded(True)
                elif type(target) in (civil.Civil, terroriste.Terroriste):
                    target.hit()
                else:
                    target.set_exploded(True)
                
                if type(self.__origine) != terroriste.Terroriste:
                    self.__music_manager.bullet_explode()
            elif type(target) == player.Player and self.hitbox.colliderect(target.get_heli().hitbox):
                self.set_exploded(True)
                if type(self.__origine) == avion.Avion:
                    damage = 10
                elif type(self.__origine) == tank.Tank:
                    damage = 30
                target.set_health(target.get_health() - damage)
                self.__music_manager.bullet_explode()
        if self.rect.x <= 0 - self.rect.width or self.rect.x >= self.__screen.get_width() + self.rect.width or self.rect.y < -100:
            self.set_exploded(True)
    
    def sync_vel(self, velocity: float, left: bool, right: bool) -> None:
        # Bouge de la même manière que la map
        if not left and not right:
            self.rect.x -= velocity
            self.hitbox.x -= velocity