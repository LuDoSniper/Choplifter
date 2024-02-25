import pygame
import objects.tank as tank

class Enemis:
    def __init__(self) -> None:
        self.__group = pygame.sprite.Group()
        self.__tanks = []
        self.__list = []
    
    # Geter / Seter
    def get_group(self) -> pygame.sprite.Group:
        return self.__group
    def set_group(self, group: pygame.sprite.Group) -> None:
        self.__group = group
    
    def get_tanks(self) -> list:
        return self.__tanks
    def set_tanks(self, tanks: list) -> None:
        self.__tanks = tanks
    
    def get_list(self) -> list:
        return self.__list
    def set_list(self, list: list) -> None:
        self.__list = list

    # Methodes
    # Tanks
    def add_tank(self) -> None:
        self.__tanks.append(tank.Tank(self.get_group()))
    
    def handle_tanks(self, heli_pos: int) -> None:
        for tank in self.get_tanks():
            tank.scan(heli_pos)
    
    def sync_vel_tanks(self, velocity: float, left: bool, right: bool) -> None:
        for tank in self.get_tanks():
            tank.sync_vel(velocity, left, right)
    
    def afficher(self, screen: pygame.Surface) -> None:
        self.get_group().draw(screen)