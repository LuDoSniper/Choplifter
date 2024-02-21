import pygame
from pytmx.util_pygame import load_pygame
# Typage
from pytmx import TiledMap

class Tile(pygame.sprite.Sprite):
    def __init__(self, surface: pygame.Surface, pos: tuple, local_pos: tuple, group: pygame.sprite.Group) -> None:
        super().__init__(group)
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        self.__local_pos = local_pos
    
    # Geter / Seter
    def get_local_pos(self) -> tuple:
        return self.__local_pos

class Map:
    def __init__(self) -> None:
        self.__tmx_data = load_pygame("assets/tilesets/map_test.tmx")
        self.__tiles = []
        self.__group = pygame.sprite.Group()
        
        self.__load_tiles()
        self.__rect = pygame.Rect((0, 0), (20 * 32, 4 * 32))
    
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
            self.__tiles.append(Tile(tile[2], (tile[0] * 32, tile[1] * 32), (tile[:2]), self.get_group()))
    
    def afficher(self, screen: pygame.Surface) -> None:
        self.get_group().draw(screen)
    
    def sync_vel(self, velocity: float) -> None:
        self.__rect.x += velocity
        
        # Modifier les tuiles
        for tuile in self.get_tiles():
            tuile.rect.x = self.__rect.x + tuile.get_local_pos()[0] * 32