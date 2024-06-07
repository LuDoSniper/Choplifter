import pygame
import objects.bullets as bullets
import objects.player as player
import objects.music as music

class Tank(pygame.sprite.Sprite):
    
    RANGE = 250
    
    def __init__(self, group: pygame.sprite.Group, screen: pygame.Surface, map_size: int, game, pos: tuple = (0, 40), type: int = 1) -> None:
        super().__init__(group)
        self.__music_manager = music.Music()
        self.__game = game
        
        # Image et Rect doivent être publiques pour Sprite
        if type == 1:
            tmp = 3
        else:
            tmp = 5
        self.image = pygame.image.load(f"assets/tanks/tank-{type}-{tmp}.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.hitbox = pygame.Rect(
            self.rect.x,
            self.rect.y,
            self.rect.width,
            self.rect.height
        )
        
        self.__group = group
        
        self.__type = type
        self.__health = tmp
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
        self.__bullet = None
        self.__bullet_group = pygame.sprite.Group()
        self.__delay = 60
        self.__timer = 0
    
    # Geter / Seter
    
    def get_group(self) -> pygame.sprite.Group:
        return self.__group
    def set_group(self, group: pygame.sprite.Group) -> None:
        self.__group = group
        super().__init__(group)
    
    def get_type(self) -> int:
        return self.__type
    def set_type(self, type: int) -> None:
        self.__type = type
    
    def get_health(self) -> int:
        return self.__health
    def set_health(self, health: int) -> None:
        self.__health = health
    
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
        
    def get_bullet(self) -> bullets.Bullet:
        return self.__bullet
    def set_bullet(self, bullet: bullets.Bullet) -> None:
        self.__bullet = bullet
        
    def get_bullet_group(self) -> pygame.sprite.Group:
        return self.__bullet_group
    def set_bullet_group(self, group: pygame.sprite.Group) -> None:
        self.__bullet_group = group
    
    # Méthodes
    def scan(self, player) -> None:
        # Agis si l'helico se trouve à portée (Se base uniquement sur l'abscisse)
        marge = 10
        heli_pos = round(player.get_heli().get_rect().x)
        if abs(abs(self.rect.x) - abs(heli_pos)) <= self.RANGE:
            # Helico à portée
            if self.rect.x > heli_pos + marge:
                self.set_dir(-1)
            elif self.rect.x < heli_pos - marge:
                self.set_dir(1)
            else:
                self.set_dir(0)
            self.move()
            # Tirer
            self.__timer += 1
            if (self.__bullet == None and self.__dir != 0) and self.__timer >= self.__delay:
                self.__timer = 0
                self.shoot()
        else:
            # Stoper le mouvement
            self.set_dir(0)
    
    def shoot(self) -> None:
        if self.__dir == 1:
            bullet_pos = (
                self.rect.x + 37,
                self.rect.y - 15
            )
        else:
            bullet_pos = (
                self.rect.x - 15,
                self.rect.y - 15
            )
        # self.rect.x + (18 * self.__dir), self.rect.y - 5
        self.__bullet = bullets.Bullet(self.__bullet_group, self.__screen, self, self.__dir, 65 * self.__dir, self.__pos, bullet_pos[0], bullet_pos[1], boost=-3)
        self.__music_manager.tank_shoot()
    
    def scan_civils(self, civils: list) -> None:
        for civil in civils:
            if self.hitbox.colliderect(civil.hitbox):
                civil.hit()
                self.__music_manager.splash()
    
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
        self.hitbox.x += self.get_velocity()
        
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

    def hit(self, damage: int = 1) -> bool:
        self.__health -= damage
        if self.__health <= 0:
            if self.__type == 1:
                score = 10
            elif self.__type == 2:
                score = 15
            self.__game.add_score(score)
            return True
        self.image = pygame.image.load(f"assets/tanks/tank-{self.__type}-{self.__health}.png")
        if self.__dir == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        return False

    def sync_side(self):
        if self.get_dir() == 1 and not self.get_side() or self.get_dir() == -1 and self.get_side():
            self.image = pygame.transform.flip(self.image, True, False)
            self.set_side(not(self.get_side()))

    def sync_vel(self, velocity: float, left: bool, right: bool) -> None:
        # Bouge de la même manière que la map
        if not left and not right:
            self.rect.x -= velocity
            self.hitbox.x -= velocity
        # Syncroniser la velocité de la bullet
        if self.__bullet is not None:
            self.__bullet.sync_vel(velocity, left, right)
    
    def get_data(self) -> dict:
        data = {
            "health": self.__health,
            "pos": self.__pos
        }
        return data
    def set_data(self, data: dict) -> None:
        self.__health = data["health"]
        self.__pos = data["pos"]