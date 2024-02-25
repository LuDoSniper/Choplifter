import pygame

class Tank(pygame.sprite.Sprite):
    
    RANGE = 100
    
    def __init__(self, group: pygame.sprite.Group, pos: tuple = (0, 40)) -> None:
        super().__init__(group)
        # Image et Rect doivent être publiques pour Sprite
        self.image = pygame.image.load("assets/imgs/Tank_tmp_56x24.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        
        self.__group = group
        
        self.__resistance = 0.9
        self.__acceleration = 0.5
        self.__max_speed = 2
        self.__velocity = 0
        self.__dir = 0 # -1 gauche 0 rien 1 droite
    
    # Geter / Seter
    def get_group(self) -> pygame.sprite.Group:
        return self.__group
    def set_group(self, group: pygame.sprite.Group) -> None:
        self.__group = group
    
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
    def set_dir(self, dir: int) -> None:
        self.__dir = dir
    
    # Méthodes
    def scan(self, heli_pos: int) -> None:
        # Agis si l'helico se trouve à portée (Se base uniquement sur l'abscisse)
        heli_pos = round(heli_pos)
        if abs(abs(self.rect.x) - abs(heli_pos)) <= self.RANGE:
            # Helico à portée
            if self.rect.x > heli_pos:
                self.set_dir(-1)
            elif self.rect.x < heli_pos:
                self.set_dir(1)
            else:
                self.set_dir(0)
            self.move()
        else:
            # Stoper le mouvement
            self.set_dir(0)
    
    def move(self) -> None:
        self.set_velocity(self.get_velocity() + (self.get_acceleration() * self.get_dir()))
        
        # Application de la resistance
        self.set_velocity(self.get_velocity() * self.get_resistance())
        if abs(self.get_velocity()) < 0.2:
            self.set_velocity(0)
        
        # Brider la velocité
        if abs(self.get_velocity()) > self.get_max_speed():
            self.set_velocity(self.get_max_speed() * self.get_dir())
        
        # Appliquer la velocité sur le rect
        self.rect.x += self.get_velocity()
    
    def sync_vel(self, velocity: float, left: bool, right: bool) -> None:
        # Bouge de la même manière que la map
        if not left and not right:
            self.rect.x -= velocity