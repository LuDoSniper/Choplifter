import pygame
import random
import objects.player as player

class Civil(pygame.sprite.Sprite):
    
    RANGE = 200
    
    def __init__(self, group: pygame.sprite.Group, local_x: int, local_y: int, pos: tuple, gender: str, type: int, clothes: int) -> None:
        super().__init__(group)
        self.image = pygame.image.load(f"assets/civils/Exported_PNGs/{gender}/Character {type}/Clothes {clothes}/Character{type}{gender[0]}_{clothes}_idle_0.png")
        # self.image = pygame.image.load(f"assets/Update/otages/Female/character-1/clothes-1/Character1F_1_idle_0.png")
        self.rect = self.image.get_rect()
        self.rect.x = local_x
        self.rect.y = local_y
        
        self.__aboard = False
        self.__saved = False
        
        self.__pos = pos
        self.__gender = gender
        self.__type = type
        self.__clothes = clothes
        
        self.__state = "idle"
        self.__frame = 0
        self.__animation_timer = 0
        self.__animation_timer_speed = 5
        self.__switch_animation_timer = 0
        self.__switch_animation_timer_target = random.randint(150, 250)
        
        self.__speed = 1
        self.__dir = 0
        self.__reversed = False
        
    # Geter / Seter
    
    def get_aboard(self) -> bool:
        return self.__aboard
    def set_aboard(self, aboard: bool) -> None:
        self.__aboard = aboard
    
    def get_saved(self) -> bool:
        return self.__saved
    def set_saved(self, saved: bool) -> None:
        self.__saved = saved
    
    def get_pos(self) -> tuple:
        return self.__pos
    def set_pos(self, pos: tuple) -> None:
        self.__pos = pos
        
    # Méthodes
    
    def handle(self, map_size: int, player) -> None:
        self.animate()
        self.sync_side()
        
        if self.__state not in ("death", "damage"):
            if self.rect.colliderect(player.get_heli().get_rect()) and player.get_storage() < player.get_max_storage() and not self.__aboard and player.get_landed():
                player.set_storage(player.get_storage() + 1)
                self.__aboard = True
            
            if self.rect.x - self.RANGE <= player.get_heli().get_rect().x <= self.rect.x + self.RANGE and player.get_landed():
                self.__state = "run"
                self.__speed = 2
                if self.rect.x > player.get_heli().get_rect().x:
                    self.__dir = -1
                else:
                    self.__dir = 1
            elif self.rect.x - self.RANGE <= player.get_heli().get_rect().x <= self.rect.x + self.RANGE:
                self.__state = "talk"
            elif self.__state == "talk":
                self.__state = "idle"
            else:
                self.__switch_animation_timer += 1
                if self.__switch_animation_timer >= self.__switch_animation_timer_target and self.__state not in ("death", "damage"):
                    self.__switch_animation_timer = 0
                    self.__switch_animation_timer_target = random.randint(150, 250)
                    self.__state = random.choice(["idle", "walk", "wait"])
                    
                    if self.__state == "walk":
                        self.__speed = 1
                        self.__dir = random.choice([-1, 1])
                    elif self.__state in ("idle", "wait"):
                        self.__dir = 0
        
        if self.__state in ("walk", "run"):
            self.move(map_size)
    
    def animate(self) -> None:
        self.__animation_timer += 1
        if self.__animation_timer >= self.__animation_timer_speed:
            self.__frame += 1
            self.__animation_timer = 0
        
        if self.__state == "idle":
            if self.__frame > 7:
                self.__frame = 0
            self.image = pygame.image.load(f"assets/civils/Exported_PNGs/{self.__gender}/Character {self.__type}/Clothes {self.__clothes}/Character{self.__type}{self.__gender[0]}_{self.__clothes}_{self.__state}_{self.__frame}.png")
            # self.image = pygame.image.load(f"assets/Update/otages/Female/character-1/clothes-1/Character1F_1_{self.__state}_{self.__frame}.png")
        elif self.__state == "walk":
            if self.__frame > 7:
                self.__frame = 0
            self.image = pygame.image.load(f"assets/civils/Exported_PNGs/{self.__gender}/Character {self.__type}/Clothes {self.__clothes}/Character{self.__type}{self.__gender[0]}_{self.__clothes}_{self.__state}_{self.__frame}.png")
            # self.image = pygame.image.load(f"assets/Update/otages/Female/character-1/clothes-1/Character1F_1_{self.__state}_{self.__frame}.png")
        elif self.__state == "wait":
            if self.__frame > 5:
                self.__frame = 0
            self.image = pygame.image.load(f"assets/civils/Exported_PNGs/{self.__gender}/Character {self.__type}/Clothes {self.__clothes}/Character{self.__type}{self.__gender[0]}_{self.__clothes}_{self.__state}_{self.__frame}.png")
            # self.image = pygame.image.load(f"assets/Update/otages/Female/character-1/clothes-1/Character1F_1_{self.__state}_{self.__frame}.png")
        elif self.__state == "run":
            if self.__frame > 7:
                self.__frame = 0
            self.image = pygame.image.load(f"assets/civils/Exported_PNGs/{self.__gender}/Character {self.__type}/Clothes {self.__clothes}/Character{self.__type}{self.__gender[0]}_{self.__clothes}_{self.__state}_{self.__frame}.png")
            # self.image = pygame.image.load(f"assets/Update/otages/Female/character-1/clothes-1/Character1F_1_{self.__state}_{self.__frame}.png")
        elif self.__state == "talk":
            if self.__frame > 6:
                self.__frame = 0
            self.image = pygame.image.load(f"assets/civils/Exported_PNGs/{self.__gender}/Character {self.__type}/Clothes {self.__clothes}/Character{self.__type}{self.__gender[0]}_{self.__clothes}_{self.__state}_{self.__frame}.png")
            # self.image = pygame.image.load(f"assets/Update/otages/Female/character-1/clothes-1/Character1F_1_{self.__state}_{self.__frame}.png")
        elif self.__state == "death":
            if self.__frame > 7:
                self.__frame = 7
            self.image = pygame.image.load(f"assets/civils/Exported_PNGs/{self.__gender}/Character {self.__type}/Clothes {self.__clothes}/Character{self.__type}{self.__gender[0]}_{self.__clothes}_{self.__state}_{self.__frame}.png")
            # self.image = pygame.image.load(f"assets/Update/otages/Female/character-1/clothes-1/Character1F_1_{self.__state}_{self.__frame}.png")
        elif self.__state == "damage":
            if self.__frame > 0:
                self.__frame = 1
            self.image = pygame.image.load(f"assets/civils/Exported_PNGs/{self.__gender}/Character {self.__type}/Clothes {self.__clothes}/Character{self.__type}{self.__gender[0]}_{self.__clothes}_{self.__state}_{self.__frame}.png")
            # self.image = pygame.image.load(f"assets/Update/otages/Female/character-1/clothes-1/Character1F_1_{self.__state}_{self.__frame}.png")
            self.__state = "death"
        
        if self.__reversed:
            self.image = pygame.transform.flip(self.image, True, False)
    
    def move(self, map_size: int) -> None:
        self.rect.x += self.__speed * self.__dir
        self.__pos = (self.__pos[0] + (self.__speed * self.__dir), self.__pos[1])
        
        # Empecher de sortir de la map
        if self.__pos[0] < 0:
            tmp = self.__pos[0]
            self.__pos = (0, self.__pos[1])
            self.rect.x -= tmp
        elif self.__pos[0] > map_size:
            tmp = self.__pos[0]
            self.__pos = (map_size - self.rect.width, self.__pos[1])
            self.rect.x -= map_size - tmp - self.rect.width
    
    def hit(self) -> None:
        if self.__state != "death":
            self.__state = "damage"
    
    def sync_side(self) -> None:
        if (self.__dir == -1 and not self.__reversed) or (self.__dir == 1 and self.__reversed):
            self.image = pygame.transform.flip(self.image, True, False)
            self.__reversed = not self.__reversed
    
    def sync_vel(self, velocity: float, left: bool, right: bool) -> None:
        # Bouge de la même manière que la map
        if not left and not right:
            self.rect.x -= velocity