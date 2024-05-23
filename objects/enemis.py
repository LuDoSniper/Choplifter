import pygame
import objects.tank as tank
import objects.avion as avion
import objects.explosion as explosion
import objects.player as player

class Enemis:
    def __init__(self, screen: pygame.Surface) -> None:
        self.__group = pygame.sprite.Group()
        self.__explosions = []
        self.__tanks = []
        self.__avions = []
        self.__list = []
        
        self.__screen = screen
    
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
        
    def get_avions(self) -> list:
        return self.__avions
    def set_avions(self, avions: list) -> None:
        self.__avions = avions
    
    def get_list(self) -> list:
        return self.__list
    def set_list(self, list: list) -> None:
        self.__list = list
        
    def get_screen(self) -> pygame.Surface:
        return self.__screen
    def set_screen(self, screen: pygame.Surface) -> None:
        self.__screen = screen

    # Methodes
    # Tanks
    def add_tank(self, screen: pygame.Surface, map_size: int, pos: tuple = (0, 40), type: int = 1) -> None:
        self.__tanks.append(tank.Tank(self.get_group(), screen, map_size, pos, type))
    
    def handle_tanks(self, player: player.Player) -> None:
        for tank in self.get_tanks():
            tank.scan(player)
            tank.sync_side()
            
            # Gestion des morts
            if tank.get_exploded():
                self.explode(tank.rect.x, tank.rect.y, tank.get_pos(), 2)
                self.__group.remove(tank)
                self.__tanks.pop(self.__tanks.index(tank))
            
            # Gestion des bullets
            if tank.get_bullet() is not None:
                tank.get_bullet().move([player.get_heli()])
                if tank.get_bullet().get_exploded():
                    self.explode(tank.get_bullet().rect.x, tank.get_bullet().rect.y, tank.get_bullet().get_pos())
                    tank.get_bullet_group().remove(tank.get_bullet())
                    tank.set_bullet(None)
    
    def sync_vel_tanks(self, velocity: float, left: bool, right: bool) -> None:
        for tank in self.get_tanks():
            tank.sync_vel(velocity, left, right)
    
    def display_tanks_bullet(self, screen: pygame.Surface) -> None:
        for tank in self.get_tanks():
            tank.get_bullet_group().draw(screen)
    
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
    
    #Avion
    def add_avion(self, screen: pygame.Surface, map_size: int, pos: tuple = (0, 40), type: int = 1, dir = 1) -> None:
        self.__avions.append(avion.Avion(self.get_group(), screen, map_size, pos, type, dir))
    
    def handle_avions(self) -> None:
        for avion in self.get_avions():
            avion.move()
            
            # Gestion des morts
            if avion.get_exploded():
                self.explode(avion.rect.x, avion.rect.y, avion.get_pos(), 2)
                self.__group.remove(avion)
                self.__avions.pop(self.__avions.index(avion))
            
            # Gestion des bullets
            for bullet in avion.get_bullets_list():
                if bullet.get_exploded():
                    avion.get_bullets_group().remove(bullet)
                    avion.get_bullets_list().pop(avion.get_bullets_list().index(bullet))
                    self.explode(bullet.rect.x, bullet.rect.y, bullet.get_pos(), 0.5)
    
    def sync_vel_avions(self, velocity: float, left: bool, right: bool) -> None:
        for avion in self.get_avions():
            avion.sync_vel(velocity, left, right)
    
    def display_avions_bullets(self, screen: pygame.Surface) -> None:
        for avion in self.get_avions():
            avion.get_bullets_group().draw(screen)
    
    def move_avions_bullets(self, targets: list = []) -> None:
        for avion in self.get_avions():
            for bullet in avion.get_bullets_list():
                bullet.move(targets)
    
    # Affichage de touts le group
    def afficher(self, screen: pygame.Surface) -> None:
        self.get_group().draw(screen)