import pygame
import random
import objects.bullets as bullets

import pygame.locals

class Avion(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group, screen: pygame.Surface, map_size: int, pos: tuple = (0, 10), type: int = 1, dir: int = 1) -> None:
        super().__init__(group)
        # Image et Rect doivent être publiques pour Sprite
        if type == 1:
            tmp = 1
        else:
            tmp = 3
        self.image = pygame.image.load(f"assets/avion/avion-{type}-{tmp}.png")
        # Car l'image est dans le mauvais sens -_-
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        if dir == 1:
            self.__pos = (0 - self.rect.width, pos[1])
        elif dir == -1:
            self.__pos = (screen.get_width() + self.rect.width, pos[1])
        self.rect.x, self.rect.y = self.__pos
        
        self.__group = group
        
        self.__type = type
        self.__health = tmp
        self.__max_speed = 4
        self.__velocity = 0
        self.__dir = dir # -1 gauche 1 droite
        
        # Acces a screen plus simple
        self.__screen = screen
        
        self.__map_size = map_size
        
        self.__exploded = False
        self.__moving = False
        
        self.__timer = 0
        self.__start = random.randint(60, 120)
        
        self.__target = 100
        self.__done = 0
        self.__rotated = 0 # -1 bas 0 milieu 1 haut
        
        self.__shooting = False
        self.__max_shoot = 5
        self.__shooted = 0
        self.__max_delay = 10
        self.__delay = 0
        self.__bullets_list = []
        self.__bullets_group = pygame.sprite.Group()
    
    # Geter / Seter
    def get_group(self) -> pygame.sprite.Group:
        return self.__group
    def set_group(self, group: pygame.sprite.Group) -> None:
        self.__group = group
    
    def get_type(self) -> int:
        return self.__type
    def set_type(self, type: int) -> None:
        self.__type = type
    
    def get_health(self) -> int:
        return self.__health
    def set_health(self, health: int) -> None:
        self.__health = health
    
    def get_max_speed(self) -> float:
        return self.__max_speed
    def set_max_speed(self, max_speed: float) -> None:
        self.__max_speed = max_speed
    
    def get_velocity(self) -> float:
        return self.__velocity
    def set_velocity(self, velocity: float) -> None:
        self.__velocity = velocity
    
    def get_dir(self) -> int:
        return self.__dir
    def set_dir(self, dir: int) -> None:
        self.__dir = dir
    
    def get_screen(self) -> pygame.Surface:
        return self.__screen
    def set_screen(self, screen: pygame.Surface) -> None:
        self.__screen = screen
    
    def get_map_size(self) -> int:
        return self.__map_size
    def set_map_size(self, map_size: int) -> None:
        self.__map_size = map_size
    
    def get_pos(self) -> tuple:
        return self.__pos
    def set_pos(self, pos: tuple) -> None:
        self.__pos = pos
    
    def get_exploded(self) -> bool:
        return self.__exploded
    def set_exploded(self, exploded: bool) -> None:
        self.__exploded = exploded
        
    def get_moving(self) -> bool:
        return self.__moving
    def set_moving(self, moving: bool) -> None:
        self.__moving = moving
        
    def get_timer(self) -> int:
        return self.__timer
    def set_timer(self, timer: int) -> None:
        self.__timer = timer
    
    def get_start(self) -> int:
        return self.__start
    def set_start(self, start: int) -> None:
        self.__start = start
    
    def get_bullets_list(self) -> list:
        return self.__bullets_list
    def set_bullets_list(self, list: list) -> None:
        self.__bullets_list = list
    
    def get_bullets_group(self) -> pygame.sprite.Group:
        return self.__bullets_group
    def set_bullets_group(self, group: pygame.sprite.Group) -> None:
        self.__bullets_group = group
        
    # Méthodes
    
    def move(self) -> None:
        if not self.__moving:
            self.__timer += 1
            
        if self.__timer >= self.__start or self.__moving:
            if not self.__moving:
                self.image = pygame.image.load(f"assets/avion/avion-{self.__type}-{self.__health}.png")
                if self.__dir == 1:
                    self.image = pygame.transform.flip(self.image, True, False)
                self.__moving = True
                self.__timer = 0
                self.__start = random.randint(120, 240)
                
                if self.__dir > 0:
                    self.rect.x = 0 - (self.image.get_rect().width + 20)
                elif self.__dir < 0:
                    self.rect.x = self.__screen.get_width() + self.image.get_rect().width + 20
                    
                self.rect.y = random.randint(0, 30)
            
            if (self.__target > 0 and self.__done >= self.__target) or (self.__target < 0 and self.__done <= self.__target):
                self.__target = 100
                self.__done = 0
            if random.randint(1, 50) == 1 and self.__target == 100:
                self.__target = random.uniform(-10.0, 10.0)
            if self.__target < 0 and self.__target != 100:
                dir_tmp = -1
            elif self.__target > 0 and self.__target != 100:
                dir_tmp = 1
            else:
                dir_tmp = 0
            
            self.__velocity = self.__max_speed * self.get_dir()
            self.rect.y += 1 * dir_tmp
            self.__done += 1 * dir_tmp
            
            if self.__rotated == 0 and dir_tmp == 1: # Monter
                self.image = pygame.transform.rotate(self.image, -5)
                self.__rotated = 1
            elif self.__rotated == 0 and dir_tmp == -1: # Descendre
                self.image = pygame.transform.rotate(self.image, 5)
                self.__rotated = -1
            elif self.__rotated == 1 and dir_tmp == 0: # Stabilisation du haut vers milieu
                #self.image = pygame.transform.rotate(self.image, 5) <-- Obsolete car perte de qualité
                self.image = pygame.image.load(f"assets/avion/avion-{self.__type}-{self.__health}.png")
                if self.__rotated and self.__dir == 1:
                    self.image = pygame.transform.flip(self.image, True, False)
                self.__rotated = 0
            elif self.__rotated == -1 and dir_tmp == 0: # Stabilisation du bas vers milieu
                #self.image = pygame.transform.rotate(self.image, -5) <-- Obsolete car perte de qualité
                self.image = pygame.image.load(f"assets/avion/avion-{self.__type}-{self.__health}.png")
                if self.__rotated and self.__dir == 1:
                    self.image = pygame.transform.flip(self.image, True, False)
                self.__rotated = 0
            
            # Appliquer la velocité sur le rect
            self.rect.x += self.get_velocity()
            self.set_pos((self.get_pos()[0] + self.get_velocity(), self.get_pos()[1] + self.__done))
            
            if self.__dir < 0 and self.rect.x < 0 - self.image.get_rect().width:
                self.__moving = False
                self.__dir = 1
                self.image = pygame.transform.flip(self.image, True, False)
            elif self.__dir > 0 and self.rect.x > self.__screen.get_width() + self.image.get_rect().width:
                self.__moving = False
                self.__dir = -1
                self.image = pygame.transform.flip(self.image, True, False)

            # Tirer
            if not self.__shooting and random.randint(1, 50) == 1:
                self.shoot()
            
        else:
            # Garder l'avion en dehors de l'écran
            if self.__dir > 0:
                self.rect.x = 0 - (self.image.get_rect().width + 20)
            elif self.__dir < 0:
                self.rect.x = self.__screen.get_width() + self.image.get_rect().width + 20

    def shoot(self):
        self.__delay += 1
        if self.__delay >= self.__max_delay or not self.__shooting:
            self.__shooting = True
            self.__delay = 0
            self.__shooted = 5
            self.__bullets_list.append(bullets.Bullet(self.__bullets_group, self.__screen, self, self.__dir, 90 * self.__dir, self.__pos, self.rect.x, self.rect.y, 2, "balle-avion"))
        if self.__shooted >= self.__max_shoot:
            self.__shooting = False

    def hit(self, damage: int = 1) -> bool:
        self.__health -= damage
        if self.__health <= 0:
            return True
        self.image = pygame.image.load(f"assets/avion/avion-{self.__type}-{self.__health}.png")
        if self.__dir == 1:
            self.image = pygame.transform.flip(self.image, True, False)
        return False

    def sync_vel(self, velocity: float, left: bool, right: bool) -> None:
        # Bouge de la même manière que la map
        if not left and not right:
            self.rect.x -= velocity