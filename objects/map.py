import pygame
from pytmx.util_pygame import load_pygame
import objects.PIG as PIG
# Typage
from pytmx import TiledMap

class Tile(pygame.sprite.Sprite):
    def __init__(self, surface: pygame.Surface, pos: tuple, local_pos: tuple, group: pygame.sprite.Group) -> None:
        super().__init__(group)
        self.image = surface
        self.image = pygame.transform.scale(self.image, (self.image.get_rect().width * 2, self.image.get_rect().height * 2))
        self.rect = self.image.get_rect(topleft = pos)
        self.__local_pos = local_pos
    
    # Geter / Seter
    def get_local_pos(self) -> tuple:
        return self.__local_pos

class Map:
    def __init__(self, path: str, width: int, height: int, tile_size: int, screen: pygame.Surface, pig: bool = False) -> None:
        self.__pig = pig
        
        self.__width = width
        self.__height = height
        self.__tile_size = tile_size
        
        # Indique si la map touche le bord droit, gauche ou aucun
        self.__left_border = False
        self.__right_border = False

        # Pour acceder aux dimensions de l'écran plus facilement
        self.__screen = screen
        
        if not pig:
            self.__tmx_data = load_pygame(path) # "assets/tilesets/map_test.tmx"
            self.__tiles = []
            self.__group = pygame.sprite.Group()
            
            self.__load_tiles()
            self.__rect = pygame.Rect((0, 0), (self.__width * self.__tile_size, self.__height * self.__tile_size))
        else:
            path_cut = path[:-4]
            PIG.generate_map_image(path, f"{path_cut}.png")
            self.__image = pygame.image.load(f"{path_cut}.png")
            size = self.__tile_size / 32
            self.__image = pygame.transform.scale(self.__image, (self.__image.get_rect().width * size, self.__image.get_rect().height * size))
            self.__rect = self.__image.get_rect()
    
    # Geter / Seter
    def get_width(self) -> int:
        return self.__width
    def set_width(self, width: int) -> None:
        self.__width = width
    
    def get_height(self) -> int:
        return self.__height
    def set_height(self, height: int) -> None:
        self.__height = height
    
    def get_tile_size(self) -> int:
        return self.__tile_size
    def set_tile_size(self, tile_size: int) -> None:
        self.__tile_size = tile_size
    
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
        super().__init__(group)
    
    def get_rect(self) -> pygame.Rect:
        return self.__rect
    def set_rect(self, rect: pygame.Rect) -> None:
        self.__rect = rect
    
    def get_left_border(self) -> bool:
        return self.__left_border
    def set_left_border(self, left_border: bool) -> None:
        self.__left_border = left_border
    
    def get_right_border(self) -> bool:
        return self.__right_border
    def set_right_border(self, right_border: bool) -> None:
        self.__right_border = right_border
    
    def get_screen(self) -> pygame.Surface:
        return self.__screen
    def set_screen(self, screen: pygame.Surface) -> None:
        self.__screen = screen
    
    # Méthodes
    def __load_tiles(self) -> None:
        tiles = self.__tmx_data.get_layer_by_name("Background").tiles()
        if tiles is not None:
            for tile in tiles:
                self.__tiles.append(Tile(tile[2], (tile[0] * self.get_tile_size(), tile[1] * self.get_tile_size()), (tile[:2]), self.get_group()))
        tiles = self.__tmx_data.get_layer_by_name("Main").tiles()
        for tile in tiles:
            self.__tiles.append(Tile(tile[2], (tile[0] * self.get_tile_size(), tile[1] * self.get_tile_size()), (tile[:2]), self.get_group()))
    
    def afficher(self, screen: pygame.Surface) -> None:
        if not self.__pig:
            out_of_screen = []
            for tile in self.__tiles:
                if tile.rect.x + tile.rect.width < 0 or tile.rect.x > screen.get_width():
                    out_of_screen.append(tile)
                    self.__group.remove(tile)
            self.get_group().draw(screen)
            for tile in out_of_screen:
                self.__group.add(tile)
        else:
            screen.blit(self.__image, self.__rect)
    
    def sync_vel(self, velocity: float) -> None:
        if velocity != 0:
            self.__rect.x -= velocity
            
            # Brider le mouvement vers la droite
            if self.__rect.x >= 0:
                self.__rect.x = 0
                self.set_left_border(True)
            else:
                self.set_left_border(False)
            
            # Brider le mouvement vers la gauche
            limite = self.get_screen().get_width() + -self.get_rect().width
            if self.__rect.x <= limite:
                self.__rect.x = limite
                self.set_right_border(True)
            else:
                self.set_right_border(False)
            
            if not self.__pig:
                # Modifier les tuiles
                for tuile in self.get_tiles():
                    tuile.rect.x = self.__rect.x + tuile.get_local_pos()[0] * self.get_tile_size()
    
    def get_map_size(self) -> int:
        return self.__width * self.__tile_size