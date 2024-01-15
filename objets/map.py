import pygame
import math
from pytmx.util_pygame import load_pygame
from objets.tile import Tile

class Map():
    def __init__(self, screen):
        self.tiles = pygame.sprite.Group()
        self.data = load_pygame("assets/tilesets/map_test.tmx")
        self.origine_x = (screen.get_width() / 2) - ((self.data.width * 32) / 2)
        self.origine_y = (screen.get_height() / 2) - ((self.data.height * 32) / 2)
        self.rect = pygame.Rect(
            (self.origine_x,
             self.origine_y),
            (self.data.width * 32,
             self.data.height * 32)
        )
        print(f"init : {self.rect.x}")
        self.load_tiles()
    
    def load_tiles(self):
        for layer in self.data.layers:
            if layer.name == "Background":
                for x, y, image in layer.tiles():
                    pos = ((x * 32) + self.origine_x, (y * 32) + self.origine_y)
                    Tile(pos, image, self.tiles, (x, y))
    
    def bouger(self, velocity, width):
        if self.rect.x - velocity < 0 and (self.rect.x + self.rect.width) - velocity > width:
            self.rect.x -= velocity
        else:
            if math.copysign(1, velocity) < 0:
                self.rect.x = 0
            else:
                self.rect.x = -(self.rect.width -  width)
        
        for tile in self.tiles:
            tile.rect.x = self.rect.x + (tile.x * 32)
    
    def afficher(self, screen):
        self.tiles.draw(screen)