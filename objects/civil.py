import pygame

class Civil(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group, local_x: int, local_y: int, pos: tuple, gender: str, type: int, clothes: int) -> None:
        super().__init__(group)
        self.image = pygame.image.load(f"assets/civils/Exported_PNGs/{gender}/Character {type}/Clothes {clothes}/Character{type}{gender[0]}_{clothes}_idle_0.png")
        self.rect = self.image.get_rect()
        self.rect.x = local_x
        self.rect.y = local_y
        
        self.__pos = pos
        self.__gender = gender
        self.__type = type
        self.__clothes = clothes
        
        self.__state = "idle"
        self.__frame = 0
        self.__animation_timer = 0
        self.__animation_timer_speed = 5
        
    # Geter / Seter
    
    def get_pos(self) -> tuple:
        return self.__pos
    def ste_pos(self, pos: tuple) -> None:
        self.__pos = pos
        
    # Méthodes
    
    def handle(self) -> None:
        self.animate()
    
    def animate(self) -> None:
        self.__animation_timer += 1
        if self.__animation_timer >= self.__animation_timer_speed:
            self.__frame += 1
            self.__animation_timer = 0
        
        if self.__state == "idle":
            if self.__frame > 7:
                self.__frame = 0
            self.image = pygame.image.load(f"assets/civils/Exported_PNGs/{self.__gender}/Character {self.__type}/Clothes {self.__clothes}/Character{self.__type}{self.__gender[0]}_{self.__clothes}_idle_{self.__frame}.png")
    
    def sync_vel(self, velocity: float, left: bool, right: bool) -> None:
        # Bouge de la même manière que la map
        if not left and not right:
            self.rect.x -= velocity