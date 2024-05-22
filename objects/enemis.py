import pygame
import objects.tank as tank
import objects.explosion as explosion

class Enemis:
    def __init__(self) -> None:
        self.__group = pygame.sprite.Group()
        self.__explosions = []
        self.__tanks = []
        self.__list = []
    
    # Geter / Seter
    def get_group(self) -> pygame.sprite.Group:
        return self.__group
    def set_group(self, group: pygame.sprite.Group) -> None:
        self.__group = group
    
    def get_explosions(self) -> list:
        return self.__explosions
    def set_explosions(self, explosions: list) -> None:
        self.__explosions = explosions
        
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
    def add_tank(self, screen: pygame.Surface, map_size: int, pos: tuple = (0, 40), type: int = 1) -> None:
        self.__tanks.append(tank.Tank(self.get_group(), screen, map_size, pos, type))
    
    def handle_tanks(self, heli_pos: int) -> None:
        for tank in self.get_tanks():
            tank.scan(heli_pos)
            tank.sync_side()
            
            # Gestion des morts
            if tank.get_exploded():
                self.explode(tank.rect.x, tank.rect.y, tank.get_pos(), 2)
                self.__group.remove(tank)
                self.__tanks.pop(self.__tanks.index(tank))
    
    def sync_vel_tanks(self, velocity: float, left: bool, right: bool) -> None:
        for tank in self.get_tanks():
            tank.sync_vel(velocity, left, right)
    
    # Explosion
    def explode(self, local_x: int, local_y: int, pos: tuple, size: float = 1) -> None:
        self.__explosions.append(explosion.Explosion(self.get_group(), local_x, local_y, pos, size))
        
    def handle_explosions(self) -> None:
        for explosion in self.get_explosions():
            if explosion.explode():
                self.__group.remove(explosion)
                self.__explosions.pop(self.__explosions.index(explosion))
                
    def sync_vel_explosions(self, velocity: float, left: bool, right: bool) -> None:
        for explosion in self.get_explosions():
            explosion.sync_vel(velocity, left, right)
    
    # Affichage de touts le group
    def afficher(self, screen: pygame.Surface) -> None:
        self.get_group().draw(screen)