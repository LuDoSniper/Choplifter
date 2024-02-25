import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group, dir: int, pos: tuple) -> None:
        super().__init__(group)
        self.__dir = dir
        self.__pos = pos