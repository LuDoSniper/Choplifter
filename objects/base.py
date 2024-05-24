import pygame

class Base(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Sprite, local_x: int ,local_y: int, pos: tuple) -> None:
        super().__init__(group)
        self.image = pygame.image.load("assets/structure/base/base-1.png")
        self.rect = self.image.get_rect()
        self.rect.x = local_x
        self.rect.y = local_y
        
        self.__pos = pos
    
    # Geter / Seter
    
    def get_pos(self) -> tuple:
        return self.__pos
    def set_pos(self, pos: tuple) -> None:
        self.__pos = pos