import pygame

class Tank(pygame.sprite.Sprite):
    
    RANGE = 250
    
    def __init__(self, group: pygame.sprite.Group, screen: pygame.Surface, map_size: int, pos: tuple = (0, 40)) -> None:
        super().__init__(group)
        # Image et Rect doivent être publiques pour Sprite
        self.image = pygame.image.load("assets/imgs/Tank_tmp_56x24.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        
        self.__group = group
        
        self.__resistance = 0.9
        self.__acceleration = 0.5
        self.__max_speed = 1
        self.__velocity = 0
        self.__dir = 0 # -1 gauche 0 rien 1 droite
        
        # Acces a screen plus simple
        self.__screen = screen
        
        self.__map_size = map_size
        self.__pos = pos
        
        self.__side = True # False gauche - True droite
        
        self.__exploded = False
    
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
    
    def get_side(self) -> bool:
        return self.__side
    def set_side(self, side: bool) -> None:
        self.__side = side
    
    def get_exploded(self) -> bool:
        return self.__exploded
    def set_exploded(self, exploded: bool) -> None:
        self.__exploded = exploded
    
    # Méthodes
    def scan(self, heli_pos: int) -> None:
        # Agis si l'helico se trouve à portée (Se base uniquement sur l'abscisse)
        marge = 10
        heli_pos = round(heli_pos)
        if abs(abs(self.get_pos()[0]) - abs(heli_pos)) <= self.RANGE:
            # Helico à portée
            if self.get_pos()[0] > heli_pos + marge:
                self.set_dir(-1)
            elif self.get_pos()[0] < heli_pos - marge:
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
        
        # Réduire le décalage de la pos - /!\ BUG /!\
        # if self.rect.x < 0:
        #     self.rect.x = 0
        #     self.set_pos((0, self.get_pos()[1]))
        # elif self.rect.x + self.rect.width > self.get_screen().get_width():
        #     self.rect.x = self.get_screen().get_width() - self.rect.width
        #     self.set_pos((self.get_map_size() - self.rect.width, self.get_pos()[1]))
        # else:
        #     self.set_pos((self.get_pos()[0] + self.get_velocity(), self.get_pos()[1]))
        self.set_pos((self.get_pos()[0] + self.get_velocity(), self.get_pos()[1]))

    def sync_side(self):
        if self.get_dir() == 1 and not self.get_side() or self.get_dir() == -1 and self.get_side():
            self.image = pygame.transform.flip(self.image, True, False)
            self.set_side(not(self.get_side()))

    def sync_vel(self, velocity: float, left: bool, right: bool) -> None:
        # Bouge de la même manière que la map
        if not left and not right:
            self.rect.x -= velocity