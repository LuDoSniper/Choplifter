import pygame
import objects.heli as heli
import objects.bomb as bomb
import objects.bullets as bullet

class Player:
    def __init__(self, screen: pygame.Surface, pos: tuple, map_size: int) -> None:
        self.__heli = heli.Heli(screen)
        
        # Accès plus simple a screen
        self.__screen = screen
        
        self.__resistance = 0.9
        self.__acceleration = 0.5
        self.__max_speed = 3
        self.__velocity = 0
        self.__dir = 0
        
        self.__pos = pos
        self.__map_size = map_size
        
        # Gestion des bombes
        self.__bombs_list = []
        self.__bombs_group = pygame.sprite.Group()
        
        # Gestion des tirs
        self.__bullets_list = []
        self.__bullets_group = pygame.sprite.Group()
    
    # Geter / Seter
    def get_heli(self) -> heli.Heli:
        return self.__heli
    def set_heli(self, heli: heli.Heli) -> None:
        self.__heli = heli
    
    def get_screen(self) -> pygame.Surface:
        return self.__screen
    def set_screen(self, screen: pygame.Surface) -> None:
        self.__screen = screen
    
    def get_resistance(self) -> float:
        return self.__resistance
    def set_resistance(self, resistance: float) -> None:
        self.__resistance = resistance
    
    def get_acceleration(self) -> float:
        return self.__acceleration
    def set_acceleration(self, acceleration: float) -> None:
        self.__acceleration = acceleration
    
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
    def set_dir(self, dir: int):
        self.__dir = dir
    
    def get_pos(self) -> tuple:
        return self.__pos
    def set_pos(self, pos: tuple) -> None:
        self.__pos = pos
    
    def get_map_size(self) -> int:
        return self.__map_size
    def set_map_size(self, map_size: int) -> None:
        self.__map_size = map_size
    
    def get_bombs_list(self) -> list:
        return self.__bombs_list
    def set_bombs_list(self, list: list) -> None:
        self.__bombs_list = list
    
    def get_bombs_group(self) -> pygame.sprite.Group:
        return self.__bombs_group
    def set_bombs_group(self, group: pygame.sprite.Group) -> None:
        self.__bombs_group = group
        
    def get_bullets_list(self) -> list:
        return self.__bullets_list
    def set_bullets_list(self, list: list) -> None:
        self.__bullets_list = list
    
    def get_bullets_group(self) -> pygame.sprite.Group:
        return self.__bullets_group
    def set_bullets_group(self, group: pygame.sprite.Group) -> None:
        self.__bullets_group = group
    
    # Méthodes
    def afficher(self, screen: pygame.Surface) -> None:
        screen.blit(self.get_heli().get_image(), self.get_heli().get_rect())
    
    def move(self) -> None:
        self.set_velocity(self.get_velocity() + (self.get_acceleration() * self.get_dir()))
        
        # Application de la resistance
        self.set_velocity(self.get_velocity() * self.get_resistance())
        if abs(self.get_velocity()) < 0.2:
            self.set_velocity(0)
        
        # Brider la velocité
        if abs(self.get_velocity()) > self.get_max_speed():
            self.set_velocity(self.get_max_speed() * self.get_dir())
        
        # Mise à jour de pos
        pos_y = 0
        pos_x = self.get_pos()[0] + self.get_velocity()
        if self.get_heli().get_rect().x <= 0:
            pos_x = 0
        elif self.get_heli().get_rect().x + self.get_heli().get_rect().width >= self.get_screen().get_width():
            pos_x = self.get_map_size() - self.get_heli().get_rect().width
        
        self.set_pos((pos_x, pos_y))
    
    # Bombes
    def bomber(self) -> None:
        self.__bombs_list.append(bomb.Bomb(self.get_bombs_group(), self.get_pos(), (self.get_heli().get_rect().x, self.get_heli().get_rect().y), self.get_screen()))
    
    def bombs_handle(self, targets: list) -> None:
        for bomb in self.get_bombs_list():
            bomb.fall(targets)
            if bomb.get_exploded():
                self.get_bombs_group().remove(bomb)
                self.__bombs_list.pop(self.__bombs_list.index(bomb))
    
    def sync_vel_bombs(self, velocity: float, left: bool, right: bool) -> None:
        for bomb in self.get_bombs_list():
            bomb.sync_vel(velocity, left, right)
    
    def afficher_bombs(self, screen: pygame.Surface) -> None:
        self.get_bombs_group().draw(screen)
    
    # Bullets
    def shoot(self) -> None:
        sens = self.get_heli().get_sens()
        if sens:
            dir = -1
        else:
            dir = 1
        self.__bullets_list.append(bullet.Bullet(self.get_bullets_group(), dir, self.get_pos(), self.get_heli().get_rect().x))
    
    def bullets_handle(self) -> None:
        for bullet in self.get_bullets_list():
            bullet.move()
            if bullet.rect.x < 0 or bullet.rect.x > self.get_map_size():
                self.get_bullets_list().pop(self.get_bullets_list().index(bullet))
                self.get_bullets_group().remove(bullet)
    
    def sync_vel_bullets(self, velocity: float, left: bool, right: bool) -> None:
        for bullets in self.get_bullets_list():
            bullets.sync_vel(velocity, left, right)
    
    def afficher_bullets(self, screen: pygame.Surface) -> None:
        self.get_bullets_group().draw(screen)