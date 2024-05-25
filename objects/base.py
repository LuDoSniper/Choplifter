import pygame

class Base(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Sprite, local_x: int ,local_y: int, pos: tuple) -> None:
        super().__init__(group)
        self.image = pygame.image.load("assets/structure/base/base-1-0-2.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_rect().width * 2, self.image.get_rect().height * 2))
        self.rect = self.image.get_rect()
        self.rect.x = local_x
        self.rect.y = local_y
        
        self.__pos = pos
        
        self.__animation_timer = 0
        self.__animation_timer_delay = 10
        self.__frame = 0
        
        self.__refuel_speed = 3
        self.__fuel_timer = 0
        self.__fuel_timer_delay = 10
    
    # Geter / Seter
    
    def get_pos(self) -> tuple:
        return self.__pos
    def set_pos(self, pos: tuple) -> None:
        self.__pos = pos
    
    # Méthodes
    
    def handle(self, player) -> None:
        self.animate()
        
        if self.rect.colliderect(player.get_heli().get_rect()) and player.get_landed():
            player.set_refueling(True)
            self.__fuel_timer += 1
            if self.__fuel_timer >= self.__fuel_timer_delay:
                self.__fuel_timer = 0
                player.set_fuel(player.get_fuel() + self.__refuel_speed)
                if player.get_fuel() > 100:
                    player.set_fuel(100)
        else:
            player.set_refueling(False)
    
    def animate(self) -> None:
        self.__animation_timer += 1
        if self.__animation_timer >= self.__animation_timer_delay:
            self.__animation_timer = 0
            self.__frame += 1
            if self.__frame > 4:
                self.__frame = 0
        self.image = pygame.image.load(f"assets/structure/base/base-1-{self.__frame}-2.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_rect().width * 2, self.image.get_rect().height * 2))

    def sync_vel(self, velocity: float, left: bool, right: bool) -> None:
        # Bouge de la même manière que la map
        if not left and not right:
            self.rect.x -= velocity