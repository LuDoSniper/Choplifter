import pygame
import objects.tank as tank
import objects.avion as avion
import objects.explosion as explosion
import objects.player as player
import objects.terroriste as terroriste

class Enemis:
    def __init__(self, screen: pygame.Surface, game) -> None:
        self.__game = game
        self.__group = pygame.sprite.Group()
        self.__explosions = []
        self.__tanks = []
        self.__avions = []
        self.__terroristes = []
        self.__list = []
        
        self.__screen = screen
    
    # Geter / Seter
    def get_group(self) -> pygame.sprite.Group:
        return self.__group
    def set_group(self, group: pygame.sprite.Group) -> None:
        self.__group = group
        for tank in self.__tanks:
            tank.set_group(group)
        for avion in self.__avions:
            avion.set_group(group)
        for terroriste in self.__terroristes:
            terroriste.set_group(group)
    
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
    
    def get_terroristes(self) -> list:
        return self.__terroristes
    def set_terroristes(self, list: list) -> None:
        self.__terroristes = list
    
    def get_terroristes_playable(self) -> list:
        list = []
        for terroriste in self.__terroristes:
            if terroriste.get_state() not in ("death", "blood"):
                list.append(terroriste)
        return list
    
    def get_list(self) -> list:
        return self.__list
    def set_list(self, list: list) -> None:
        self.__list = list
        
    def get_screen(self) -> pygame.Surface:
        return self.__screen
    def set_screen(self, screen: pygame.Surface) -> None:
        self.__screen = screen

    # Methodes
    
    def remove_terroriste(self, terroriste) -> None:
        self.__terroristes.pop(self.__terroristes.index(terroriste))
        self.__group.remove(terroriste)
    
    # Tanks
    def add_tank(self, screen: pygame.Surface, map_size: int, pos: tuple = (0, 40), type: int = 1) -> None:
        self.__tanks.append(tank.Tank(self.get_group(), screen, map_size, self.__game, pos, type))
    
    def handle_tanks(self, player: player.Player, civils: list, structures: list) -> None:
        for tank in self.get_tanks():
            if not(tank.rect.x + tank.rect.width < 0 or tank.rect.x > self.__screen.get_width()):
                tank.scan(player)
                tank.scan_civils(civils)
                tank.sync_side()
                
                # Gestion des morts
                if tank.get_exploded():
                    self.explode(tank.rect.x, tank.rect.y, tank.get_pos(), 2)
                    self.__group.remove(tank)
                    self.__tanks.pop(self.__tanks.index(tank))
                
                # Gestion des bullets
                if tank.get_bullet() is not None:
                    tank.get_bullet().move([player] + structures)
                    if tank.get_bullet().get_exploded():
                        self.explode(tank.get_bullet().rect.x, tank.get_bullet().rect.y, tank.get_bullet().get_pos())
                        tank.get_bullet_group().remove(tank.get_bullet())
                        tank.set_bullet(None)
    
    def sync_vel_tanks(self, velocity: float, left: bool, right: bool) -> None:
        for tank in self.get_tanks():
            tank.sync_vel(velocity, left, right)
    
    def display_tanks_bullet(self, screen: pygame.Surface) -> None:
        for tank in self.get_tanks():
            if not(tank.rect.x + tank.rect.width < 0 or tank.rect.x > screen.get_width()):
                tank.get_bullet_group().draw(screen)
    
    # Explosion
    def explode(self, local_x: int, local_y: int, pos: tuple, size: float = 1) -> None:
        self.__explosions.append(explosion.Explosion(self.get_group(), local_x, local_y, pos, size))
        
    def handle_explosions(self) -> None:
        for explosion in self.get_explosions():
            if not(explosion.rect.x + explosion.rect.width < 0 or explosion.rect.x > self.__screen.get_width()):
                if explosion.explode():
                    self.__group.remove(explosion)
                    self.__explosions.pop(self.__explosions.index(explosion))
                
    def sync_vel_explosions(self, velocity: float, left: bool, right: bool) -> None:
        for explosion in self.get_explosions():
            explosion.sync_vel(velocity, left, right)
    
    #Avion
    def add_avion(self, screen: pygame.Surface, map_size: int, pos: tuple = (0, 40), type: int = 1, dir = 1) -> None:
        self.__avions.append(avion.Avion(self.get_group(), screen, map_size, self.__game, pos, type, dir))
    
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
            if not(avion.rect.x + avion.rect.width < 0 or avion.rect.x > screen.get_width()):
                avion.get_bullets_group().draw(screen)
    
    def move_avions_bullets(self, targets: list = []) -> None:
        for avion in self.get_avions():
            for bullet in avion.get_bullets_list():
                bullet.move(targets)
    
    # Terroristes
    def add_terroriste(self, local_x: int, local_y: int, pos: tuple = (0, 40), type: str = "classique") -> None:
        self.__terroristes.append(terroriste.Terroriste(self.get_group(), local_x, local_y, pos, type, self.__game)) # Remplir
    
    def handle_terroristes(self, map_size: int, screen: pygame.Surface, civils: list, player_var) -> None:
        for terroriste in self.__terroristes:
            terroriste.despawn()
            if terroriste.get_despawn():
                self.remove_terroriste(terroriste)
            if not(terroriste.rect.x + terroriste.rect.width < 0 or terroriste.rect.x > self.__screen.get_width()):
                terroriste.handle(map_size, screen, civils, player_var)
                
                # Gestion des bullets
                for bullet in terroriste.get_bullets_list():
                    if bullet.get_exploded():
                        terroriste.get_bullets_group().remove(bullet)
                        terroriste.get_bullets_list().pop(terroriste.get_bullets_list().index(bullet))
                        self.explode(bullet.rect.x, bullet.rect.y, bullet.get_pos(), 0.5)
    
    def sync_vel_terroristes(self, velocity: float, left: bool, right: bool) -> None:
        for terroriste in self.__terroristes:
            terroriste.sync_vel(velocity, left, right)
    
    def display_terroristes_bullets(self, screen: pygame.Surface) -> None:
        for terroriste in self.__terroristes:
            if not(terroriste.rect.x + terroriste.rect.width < 0 or terroriste.rect.x > screen.get_width()):
                terroriste.get_bullets_group().draw(screen)
    
    def move_terroristes_bullets(self, targets: list = []) -> None:
        for terroriste in self.__terroristes:
            terroriste.bullets_handle(targets)
    
    def afficher_gun(self, screen: pygame.Surface) -> None:
        for terroriste in self.__terroristes:
            terroriste.afficher_gun(screen)

    def afficher_terroristes_explosion(self, screen: pygame.Surface) -> None:
        for terroriste in self.__terroristes:
            terroriste.afficher_explosion(screen)
    
    # Affichage de touts le group
    def afficher(self, screen: pygame.Surface) -> None:
        out_of_screen = []
        enemis = self.__tanks + self.__avions + self.__terroristes + self.__explosions
        for enemi in enemis:
            if enemi.rect.x + enemi.rect.width < 0 or enemi.rect.x > screen.get_width():
                out_of_screen.append(enemi)
                self.__group.remove(enemi)
        self.get_group().draw(screen)
        for enemi in out_of_screen:
            self.__group.add(enemi)