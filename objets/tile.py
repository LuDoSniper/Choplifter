import pygame
from pytmx.util_pygame import load_pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surface, group, pos_map):
        super().__init__(group)
        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.x, self.y = pos_map[0], pos_map[1]