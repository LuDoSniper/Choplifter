import pygame
import random
import objects.map as map
import objects.player as player
import objects.enemis as enemis
import objects.tank as tank
import objects.avion as avion
import objects.terroriste as terroriste
import objects.structure as structure
import objects.base as base

class Mission():
    def __init__(self, id: str, screen: pygame.Surface) -> None:
        self.__id = id
        self.__screen = screen
        self.load(id)
    
    # Geter / Seter
    
    def get_id(self) -> int:
        return self.__id
    def set_id(self, id: int) -> None:
        self.__id = id
    
    def get_map(self) -> map.Map:
        return self.__map
    def set_map(self, map: map.Map) -> None:
        self.__map = map
    
    def get_player(self) -> player.Player:
        return self.__player
    def set_player(self, player: player.Player) -> None:
        self.__player = player
    
    def get_enemis(self) -> enemis.Enemis:
        return self.__enemis
    def set_enemis(self, enemis: enemis.Enemis) -> None:
        self.__enemis = enemis
    
    def get_structures_list(self) -> list:
        return self.__structures
    def set_structures_list(self, structures: list) -> None:
        self.__structures = structure
    
    def get_structures_group(self) -> pygame.sprite.Group:
        return self.__structures_group
    def set_structures_group(self, group: pygame.sprite.Group) -> None:
        self.__structures_group = group
    
    def get_base(self) -> base.Base:
        return self.__base
    def set_base(self, base: base.Base) -> None:
        self.__base = base
    
    def get_base_group(self) -> pygame.sprite.Group:
        return self.__base_group
    def set_base_group(self, group: pygame.sprite.Group) -> None:
        self.__base_group = group
    
    # Méthodes
    
    def load(self, id: str) -> None:
        height = 4 # temporaire
        tile_size = 64 # temporaire
        
        self.__base_group = pygame.sprite.Group()
        self.__structures = []
        self.__enemis = enemis.Enemis(self.__screen)
        self.__structures_group = pygame.sprite.Group()
        
        if id == "map_test":
            width = 20
            self.__map = map.Map(f"assets/tilesets/{id}.tmx", width, height, tile_size, self.__screen)
            self.__player = player.Player(self.__screen, (self.__screen.get_width() / 2 - 13 / 2, 0), self.__map.get_map_size()) # pas fini
            self.__base = base.Base(self.__base_group, 3 * tile_size, 30, (3 * tile_size, 30))
            self.__structures.append(structure.Structure(self.__structures_group, 2 * tile_size, 72, (2 * tile_size, 72), "batiment", "ville"))
            self.__structures.append(structure.Structure(self.__structures_group, 10 * tile_size, 72, (2 * tile_size, 72), "garage", "ville"))
            self.__structures.append(structure.Structure(self.__structures_group, 15 * tile_size, 72, (2 * tile_size, 72), "batiment", "ville"))
            self.__enemis.add_tank(self.__screen, self.__map.get_map_size(), (5 * tile_size, 100))
            self.__enemis.add_tank(self.__screen, self.__map.get_map_size(), (12 * tile_size, 100))
        else:
            if int(id[0]) == 1:
                if int(id[-1]) == 1:
                    width = 20
                    self.__map = map.Map(f"assets/tilesets/{id}.tmx", width, height, tile_size, self.__screen)
                    self.__player = player.Player(self.__screen, (self.__screen.get_width() / 2 - 13 / 2, 0), self.__map.get_map_size()) # pas fini
                    self.__base = base.Base(self.__base_group, 3 * tile_size, 30, (3 * tile_size, 30))
                    self.__structures.append(structure.Structure(self.__structures_group, 2 * tile_size, 72, (2 * tile_size, 72), "batiment", "ville"))
                    self.__structures.append(structure.Structure(self.__structures_group, 10 * tile_size, 72, (2 * tile_size, 72), "garage", "ville"))
                    self.__structures.append(structure.Structure(self.__structures_group, 15 * tile_size, 72, (2 * tile_size, 72), "batiment", "ville"))
                    self.__enemis.add_tank(self.__screen, self.__map.get_map_size(), (5 * tile_size, 100))
                    self.__enemis.add_tank(self.__screen, self.__map.get_map_size(), (12 * tile_size, 100))
                elif int(id[-1]) == 2:
                    width = 30
                elif int(id[-1]) == 3:
                    width = 40
                elif int(id[-1]) == 4:
                    width = 50
            elif int(id[0]) == 2:
                if int(id[-1]) == 1:
                    width = 20
                elif int(id[-1]) == 2:
                    width = 30
                elif int(id[-1]) == 3:
                    width = 40
                elif int(id[-1]) == 4:
                    width = 50
            elif int(id[0]) == 3:
                if int(id[-1]) == 1:
                    width = 20
                elif int(id[-1]) == 2:
                    width = 30
                elif int(id[-1]) == 3:
                    width = 40
                elif int(id[-1]) == 4:
                    width = 50
            elif int(id[0]) == 4:
                if int(id[-1]) == 1:
                    width = 20
                elif int(id[-1]) == 2:
                    width = 30
                elif int(id[-1]) == 3:
                    width = 40
                elif int(id[-1]) == 4:
                    width = 50