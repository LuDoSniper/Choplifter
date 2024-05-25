import pygame
import objects.heli as heli
import objects.bomb as bomb
import objects.bullets as bullet
import objects.explosion as explosion

class Player:
    def __init__(self, screen: pygame.Surface, pos: tuple, map_size: int) -> None:
        self.__heli = heli.Heli(screen)
        
        # Accès plus simple a screen
        self.__screen = screen
        
        self.__resistance = 0.9
        self.__acceleration = 0.5
        self.__max_speed = 3
        self.__max_vertical_speed = 1.5
        self.__velocity = 0
        self.__vertical_velocity = 0
        self.__dir = 0
        self.__vertical_dir = 0
        self.__angle = 90
        
        self.__max_storage = 5
        self.__storage = 0
        self.__health = 100
        self.__fuel = 100
        self.__fuel_timer = 0
        self.__fuel_timer_delay = 50
        
        self.__pos = pos
        self.__max_height = 0
        self.__min_height = 100
        self.__map_size = map_size
        
        # Gestion des bombes
        self.__bombs_list = []
        self.__bombs_group = pygame.sprite.Group()
        
        # Gestion des tirs
        self.__bullets_list = []
        self.__bullets_group = pygame.sprite.Group()
        
        # Gestion des explosions
        self.__explosions_list = []
        self.__explosions_group = pygame.sprite.Group()
    
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
        
    def get_max_vertical_speed(self) -> float:
        return self.__max_vertical_speed
    def set_max_vertical_speed(self, max_vertical_speed: float) -> None:
        self.__max_vertical_speed = max_vertical_speed
    
    def get_velocity(self) -> float:
        return self.__velocity
    def set_velocity(self, velocity: float) -> None:
        self.__velocity = velocity
        
    def get_vertical_velocity(self) -> float:
        return self.__vertical_velocity
    def set_vertical_velocity(self, vertical_velocity: float) -> None:
        self.__vertical_velocity = vertical_velocity
    
    def get_dir(self) -> int:
        return self.__dir
    def set_dir(self, dir: int):
        self.__dir = dir
        
    def get_vertical_dir(self) -> int:
        return self.__vertical_dir
    def set_vertical_dir(self, vertical_dir: int):
        self.__vertical_dir = vertical_dir
        
    def get_angle(self) -> int:
        return self.__angle
    def set_angle(self, angle: int):
        self.__angle = angle
    
    def get_max_storage(self) -> int:
        return self.__max_storage
    def set_max_storage(self, max_storage: int) -> None:
        self.__max_storage = max_storage
    
    def get_storage(self) -> int:
        return self.__storage
    def set_storage(self, storage: int) -> None:
        self.__storage = storage
    
    def get_health(self) -> int:
        return self.__health
    def set_health(self, health: int) -> None:
        self.__health = health
    
    def get_fuel(self) -> int:
        return self.__fuel
    def set_fuel(self, fuel: int) -> None:
        self.__fuel = fuel
    
    def get_pos(self) -> tuple:
        return self.__pos
    def set_pos(self, pos: tuple) -> None:
        self.__pos = pos
    
    def get_max_height(self) -> int:
        return self.__max_height
    def set_max_height(self, max_height: int) -> None:
        self.__max_height = max_height
        
    def get_min_height(self) -> int:
        return self.__min_height
    def set_min_height(self, min_height: int) -> None:
        self.__min_height = min_height
        
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
    
    def get_explosions_list(self) -> list:
        return self.__explosions_list
    def set_bullets_list(self, list: list) -> None:
        self.__explosions_list = list
        
    def get_explosions_group(self) -> pygame.sprite.Group:
        return self.__explosions_group
    def set_explosions_group(self, group: pygame.sprite.Group) -> None:
        self.__explosions_group = group
    
    # Méthodes
    def afficher(self, screen: pygame.Surface) -> None:
        image = self.get_heli().get_image()
        rect = self.get_heli().get_rect()
        if self.get_angle() not in (-90, 90):
            image = self.get_heli().get_image_tmp()
            # rect = self.get_heli().get_rect(center=self.get_heli().get_center())
        screen.blit(image, rect)
    
    def move(self) -> None:
        # Consommer du carburant
        self.__fuel_timer += 1
        if self.__fuel_timer >= self.__fuel_timer_delay:
            self.__fuel_timer = 0
            self.__fuel -= 1
        
        # Mouvement
        self.set_velocity(self.get_velocity() + (self.get_acceleration() * self.get_dir()))
        self.set_vertical_velocity(self.get_vertical_velocity() + (self.get_acceleration() * self.get_vertical_dir()))
        
        # Rotation de l'helico
        self.get_heli().sync_side(self.get_dir())
        sens = 1
        if self.get_heli().get_sens():
            sens = -1
        q = abs(self.get_velocity()) / (self.get_max_speed() + 0.5) # jsp pk mais la velocity atteint |3.5|
        self.set_angle((q * 20 + 90) * sens)
        self.get_heli().rotate(self.get_angle())
                
        # Application de la resistance
        self.set_velocity(self.get_velocity() * self.get_resistance())
        if abs(self.get_velocity()) < 0.2:
            self.set_velocity(0)
        self.set_vertical_velocity(self.get_vertical_velocity() * self.get_resistance())
        if abs(self.get_vertical_velocity()) < 0.2:
            self.set_vertical_velocity(0)
        
        # Brider la velocité
        if abs(self.get_velocity()) > self.get_max_speed():
            self.set_velocity(self.get_max_speed() * self.get_dir())
        if abs(self.get_vertical_velocity()) > self.get_max_vertical_speed():
            self.set_vertical_velocity(self.get_max_vertical_speed() * self.get_vertical_dir())
        
        # Mise à jour de pos
        pos_y = self.get_pos()[1] + self.get_vertical_velocity()
        pos_x = self.get_pos()[0] + self.get_velocity()
        if self.get_heli().get_rect().y >= self.get_max_height():
            pos_y = 0
        elif self.get_heli().get_rect().y + self.get_heli().get_rect().height >= self.get_min_height():
            pos_y = self.get_min_height - self.get_heli().get_rect().height
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
        self.__bullets_list.append(bullet.Bullet(self.get_bullets_group(), self.__screen, self, dir, self.get_angle(), self.get_pos(), self.get_heli().get_rect().x, self.get_heli().get_rect().y))
    
    def bullets_handle(self, targets: list = []) -> None:
        for bullet in self.get_bullets_list():
            bullet.move(targets)
            if bullet.rect.x < 0 or bullet.rect.x > self.get_map_size() or bullet.rect.y < 0 or bullet.rect.y > self.get_screen().get_height() or bullet.get_exploded():
                if bullet.get_exploded():
                    self.explode(bullet.rect.x, bullet.rect.y, bullet.get_pos(), 1)
                self.get_bullets_list().pop(self.get_bullets_list().index(bullet))
                self.get_bullets_group().remove(bullet)
    
    def sync_vel_bullets(self, velocity: float, left: bool, right: bool) -> None:
        for bullets in self.get_bullets_list():
            bullets.sync_vel(velocity, left, right)
    
    def afficher_bullets(self, screen: pygame.Surface) -> None:
        self.get_bullets_group().draw(screen)
    
    # Explosions
    def explode(self, local_x: int, local_y: int, pos: tuple, size: float = 1) -> None:
        self.__explosions_list.append(explosion.Explosion(self.get_explosions_group(), local_x, local_y, pos, size))
    
    def explosions_handle(self) -> None:
        for explosion in self.get_explosions_list():
            if explosion.explode():
                self.get_explosions_list().pop(self.get_explosions_list().index(explosion))
                self.get_explosions_group().remove(explosion)
    
    def sync_vel_explosions(self, velocity: float, left: bool, right: bool) -> None:
        for explosion in self.get_explosions_list():
            explosion.sync_vel(velocity, left, right)
    
    def afficher_explosions(self, screen: pygame.Surface) -> None:
        self.get_explosions_group().draw(screen)
    