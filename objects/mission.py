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
    
    def load(self, id: str, reload: bool = False) -> None:
        if reload:
            civils = []
            for structure_tmp in self.__structures:
                tmp = structure_tmp.get_civils_list()
                for civil in tmp:
                    civils.append(civil)
            
            terroristes = self.__enemis.get_terroristes()
            tanks = self.__enemis.get_tanks()
            avions = self.__enemis.get_avions()
            
            # Get data
            civils_data = []
            for civil in civils:
                civils_data.append(civil.get_data())
                civil.origine = self.__structures.index(civil.origine)
            
            terroristes_data = []
            for terroriste in terroristes:
                terroristes_data.append(terroriste.get_data())
            
            tanks_data = []
            for tank in tanks:
                tanks_data.append(tank.get_data())
            
            avions_data = []
            for avion in avions:
                avions_data.append(avion.get_data())
            
            structures_data = []
            for structure_tmp in self.__structures:
                structures_data.append(structure_tmp.get_data())
        
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
            self.__base = base.Base(self.__base_group, 4 * tile_size, 30, (4 * tile_size, 30 + 4 * tile_size))
            self.__structures.append(structure.Structure(self.__structures_group, 2 * tile_size, 72 + 4 * tile_size, (2 * tile_size, 72 + 4 * tile_size), "batiment", "ville"))
            self.__structures.append(structure.Structure(self.__structures_group, 10 * tile_size, 72 + 4 * tile_size, (2 * tile_size, 72 + 4 * tile_size), "garage", "ville"))
            self.__structures.append(structure.Structure(self.__structures_group, 15 * tile_size, 72 + 4 * tile_size, (2 * tile_size, 72 + 4 * tile_size), "batiment", "ville"))
            if not reload:
                self.__enemis.add_tank(self.__screen, self.__map.get_map_size(), (5 * tile_size, 100 + 4 * tile_size))
                self.__enemis.add_tank(self.__screen, self.__map.get_map_size(), (12 * tile_size, 100 + 4 * tile_size))
        else:
            if int(id[0]) == 1:
                if int(id[-1]) == 1:
                    width = 20
                    if int(id[0]) == 1:
                        id = f"Island/{id}"
                    height = 10
                    self.__map = map.Map(f"assets/tilesets/{id}.tmx", width, height, tile_size, self.__screen)
                    self.__player = player.Player(self.__screen, (self.__screen.get_width() / 2 - 13 / 2, 0), self.__map.get_map_size()) # pas fini
                    self.__base = base.Base(self.__base_group, 4 * tile_size, 30 + (4 * tile_size), (4 * tile_size, 30 + (4 * tile_size)))
                    self.__structures.append(structure.Structure(self.__structures_group, 2 * tile_size, 72 + (4 * tile_size), (2 * tile_size, 72 + (4 * tile_size)), "batiment", "ville"))
                    self.__structures.append(structure.Structure(self.__structures_group, 10 * tile_size, 72 + (4 * tile_size), (2 * tile_size, 72 + (4 * tile_size)), "garage", "ville"))
                    self.__structures.append(structure.Structure(self.__structures_group, 15 * tile_size, 72 + (4 * tile_size), (2 * tile_size, 72 + (4 * tile_size)), "batiment", "ville"))
                    if not reload:
                        self.__enemis.add_tank(self.__screen, self.__map.get_map_size(), (5 * tile_size, 100 + (4 * tile_size)))
                        self.__enemis.add_tank(self.__screen, self.__map.get_map_size(), (12 * tile_size, 100 + (4 * tile_size)))
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
        
        if reload:
            # Set data
            i = 0
            for terroriste in terroristes:
                terroriste.set_data(terroristes_data[i])
                i += 1
            
            i = 0
            for tank in tanks:
                tank.set_data(tanks_data[i])
                tank.set_group(self.__enemis.get_group())
                tmp = self.__enemis.get_tanks()
                tmp.append(tank)
                self.__enemis.set_list(tmp)
                i += 1
            
            i = 0
            for avion in avions:
                avion.set_data(avions_data[i])
                i += 1
            
            i = 0
            for structure_tmp in self.__structures:
                structure_tmp.set_data(structures_data[i])
                i += 1
    
            i = 0
            for civil in civils:
                civil.set_data(civils_data[i])
                civil.set_group(self.__structures[civil.origine].get_civils_group())
                tmp = self.__structures[civil.origine].get_civils_list()
                tmp.append(civil)
                self.__structures[civil.origine].set_civils_list(tmp)
                civil.origine = self.__structures[civil.origine]
                i += 1
            
    def reload(self, id: str) -> None:
        player_try = self.__player.get_try() - 1
        if player_try <= 0:
            self.game_over()
            return # Arreter la fonction
        self.load(id, True)
        self.__player.set_try(player_try)
    
    def game_over(self) -> None:
        print("Game Over")