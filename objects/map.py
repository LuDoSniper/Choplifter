import pygame
from pytmx.util_pygame import load_pygame
# Typage
from pytmx import TiledMap

class Tile(pygame.sprite.Sprite):
    def __init__(self, surface: pygame.Surface, pos: tuple, group: pygame.sprite.Group) -> None:
        super().__init__(group)
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
    
    # Geter / Seter
    # def get_image(self) -> pygame.Surface:
    #     return self.__image
    # def set_image(self, image: pygame.Surface) -> None:
    #     self.__image = image
    
    # def get_rect(self) -> pygame.Rect:
    #     return self.__rect
    # def set_rect(self, rect: pygame.Rect) -> None:
    #     self.__rect = rect

class Map:
    def __init__(self) -> None:
        self.__tmx_data = load_pygame("assets/tilesets/map_test.tmx")
        self.__tiles = []
        self.__group = pygame.sprite.Group()
        
        self.__load_tiles()
    
    # Geter / Seter
    def get_tmx_data(self) -> TiledMap:
        return self.__tmx_data
    def set_tmx_data(self, data: TiledMap) -> None:
        self.__tmx_data = data
    
    def get_tiles(self) -> list:
        return self.__tiles
    def set_tiles(self, tiles: list) -> None:
        self.__tiles = tiles
    
    def get_group(self) -> pygame.sprite.Group:
        return self.__group
    def set_group(self, group: pygame.sprite.Group) -> None:
        self.__group = group
    
    # Méthodes
    def __load_tiles(self) -> None:
        for tile in self.get_tmx_data().get_layer_by_name("Background").tiles():
            self.__tiles.append(Tile(tile[2], (tile[0] * 32, tile[1] * 32), self.get_group()))
    
    def afficher(self, screen: pygame.Surface) -> None:
        self.get_group().draw(screen)