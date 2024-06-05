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
    def __init__(self, id: str, screen: pygame.Surface, game) -> None:
        self.__id = id
        self.__screen = screen
        self.__game = game
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
        elif id == "sandbox":
            width = 100
            self.__map = map.Map(f"assets/tilesets/sandbox/sandbox.tmx", width, height, tile_size, self.__screen)
            self.__player = player.Player(self.__screen, (self.__screen.get_width() / 2 - 13 / 2, 0), self.__map.get_map_size()) # pas fini
                    
            # Positions
            base_pos = (14 * tile_size, 4 * tile_size + 30)
            structure1_pos = (3 * tile_size, 4 * tile_size + 72)
            structure2_pos = (10 * tile_size, 4 * tile_size + 72)
            structure3_pos = (25 * tile_size, 4 * tile_size + 72)
            tank1_pos = (5 * tile_size, 4 * tile_size + 100)
            tank2_pos = (20 * tile_size, 4 * tile_size + 100)
            
            self.__base = base.Base(self.__base_group, base_pos[0], base_pos[1], (base_pos[0], base_pos[1]))
            self.__structures.append(structure.Structure(self.__structures_group, structure1_pos[0], structure1_pos[1], (structure1_pos[0], structure1_pos[1]), "batiment", "ville"))
            self.__structures.append(structure.Structure(self.__structures_group, structure2_pos[0], structure2_pos[1], (structure2_pos[0], structure2_pos[1]), "garage", "ville"))
            self.__structures.append(structure.Structure(self.__structures_group, structure3_pos[0], structure3_pos[1], (structure3_pos[0], structure3_pos[1]), "batiment", "ville"))
            if not reload:
                self.__enemis.add_tank(self.__screen, self.__map.get_map_size(), (tank1_pos[0], tank1_pos[1]))
                self.__enemis.add_tank(self.__screen, self.__map.get_map_size(), (tank2_pos[0], tank2_pos[1]))
        else:
            if int(id[0]) == 1:
                if int(id[-1]) == 1:
                    width = 30
                    if int(id[0]) == 1:
                        id = f"Island/{id}"
                    height = 10
                    self.__map = map.Map(f"assets/tilesets/{id}.tmx", width, height, tile_size, self.__screen)
                    self.__player = player.Player(self.__screen, (self.__screen.get_width() / 2 - 13 / 2, 0), self.__map.get_map_size()) # pas fini
                    
                    # Positions
                    base_pos = (14 * tile_size, 4 * tile_size + 30)
                    structure1_pos = (3 * tile_size, 4 * tile_size + 72)
                    structure2_pos = (10 * tile_size, 4 * tile_size + 72)
                    structure3_pos = (25 * tile_size, 4 * tile_size + 72)
                    tank1_pos = (5 * tile_size, 4 * tile_size + 100)
                    tank2_pos = (20 * tile_size, 4 * tile_size + 100)
                    
                    self.__base = base.Base(self.__base_group, base_pos[0], base_pos[1], (base_pos[0], base_pos[1]))
                    self.__structures.append(structure.Structure(self.__structures_group, structure1_pos[0], structure1_pos[1], (structure1_pos[0], structure1_pos[1]), "batiment", "ville"))
                    self.__structures.append(structure.Structure(self.__structures_group, structure2_pos[0], structure2_pos[1], (structure2_pos[0], structure2_pos[1]), "garage", "ville"))
                    self.__structures.append(structure.Structure(self.__structures_group, structure3_pos[0], structure3_pos[1], (structure3_pos[0], structure3_pos[1]), "batiment", "ville"))
                    if not reload:
                        self.__enemis.add_tank(self.__screen, self.__map.get_map_size(), (tank1_pos[0], tank1_pos[1]))
                        self.__enemis.add_tank(self.__screen, self.__map.get_map_size(), (tank2_pos[0], tank2_pos[1]))
                elif int(id[-1]) == 2:
                    width = 40
                    if int(id[0]) == 1:
                        id = f"Island/{id}"
                    height = 10
                    self.__map = map.Map(f"assets/tilesets/{id}.tmx", width, height, tile_size, self.__screen)
                    self.__player = player.Player(self.__screen, (self.__screen.get_width() / 2 - 13 / 2, 0), self.__map.get_map_size()) # pas fini
                    
                    # Positions
                    base_pos = (14 * tile_size, 4 * tile_size + 30)
                    structure1_pos = (3 * tile_size, 4 * tile_size + 72)
                    structure2_pos = (10 * tile_size, 4 * tile_size + 72)
                    structure3_pos = (25 * tile_size, 4 * tile_size + 72)
                    structure4_pos = (30 * tile_size, 4 * tile_size + 72)
                    structure5_pos = (35 * tile_size, 4 * tile_size + 72)
                    tank1_pos = (5 * tile_size, 4 * tile_size + 100)
                    tank2_pos = (24 * tile_size, 4 * tile_size + 100)
                    tank3_pos = (31 * tile_size, 4 * tile_size + 100)
                    terroriste1_pos = (9 * tile_size, 4 * tile_size + 75)
                    terroriste2_pos = (34 * tile_size, 4 * tile_size + 75)
                    
                    self.__base = base.Base(self.__base_group, base_pos[0], base_pos[1], (base_pos[0], base_pos[1]))
                    self.__structures.append(structure.Structure(self.__structures_group, structure1_pos[0], structure1_pos[1], (structure1_pos[0], structure1_pos[1]), "batiment", "ville"))
                    self.__structures.append(structure.Structure(self.__structures_group, structure2_pos[0], structure2_pos[1], (structure2_pos[0], structure2_pos[1]), "garage", "ville"))
                    self.__structures.append(structure.Structure(self.__structures_group, structure3_pos[0], structure3_pos[1], (structure3_pos[0], structure3_pos[1]), "batiment", "ville"))
                    self.__structures.append(structure.Structure(self.__structures_group, structure4_pos[0], structure4_pos[1], (structure4_pos[0], structure4_pos[1]), "garage", "ville"))
                    self.__structures.append(structure.Structure(self.__structures_group, structure5_pos[0], structure5_pos[1], (structure5_pos[0], structure5_pos[1]), "batiment", "ville"))
                    if not reload:
                        self.__enemis.add_tank(self.__screen, self.__map.get_map_size(), (tank1_pos[0], tank1_pos[1]))
                        self.__enemis.add_tank(self.__screen, self.__map.get_map_size(), (tank2_pos[0], tank2_pos[1]))
                        self.__enemis.add_tank(self.__screen, self.__map.get_map_size(), (tank3_pos[0], tank3_pos[1]))
                        self.__enemis.add_terroriste(terroriste1_pos[0], terroriste1_pos[1], (terroriste1_pos[0], terroriste1_pos[1]), "classique")
                        self.__enemis.add_terroriste(terroriste2_pos[0], terroriste2_pos[1], (terroriste2_pos[0], terroriste2_pos[1]), "classique")
                elif int(id[-1]) == 3:
                    width = 50
                    if int(id[0]) == 1:
                        id = f"Island/{id}"
                    height = 10
                    self.__map = map.Map(f"assets/tilesets/{id}.tmx", width, height, tile_size, self.__screen)
                    self.__player = player.Player(self.__screen, (self.__screen.get_width() / 2 - 13 / 2, 0), self.__map.get_map_size()) # pas fini
                    
                    # Positions
                    base_pos = (25 * tile_size, 4 * tile_size + 30)
                    structure1_pos = (4 * tile_size, 4 * tile_size + 72)
                    structure2_pos = (11 * tile_size, 4 * tile_size + 72)
                    structure3_pos = (20 * tile_size, 4 * tile_size + 72)
                    structure4_pos = (30 * tile_size, 4 * tile_size + 72)
                    structure5_pos = (35 * tile_size, 4 * tile_size + 72)
                    structure6_pos = (39 * tile_size, 4 * tile_size + 72)
                    structure7_pos = (47 * tile_size, 4 * tile_size + 72)
                    tank1_pos = (5 * tile_size, 4 * tile_size + 100)
                    tank2_pos = (24 * tile_size, 4 * tile_size + 100)
                    tank3_pos = (31 * tile_size, 4 * tile_size + 100)
                    tank4_pos = (40 * tile_size, 4 * tile_size + 100)
                    tank5_pos = (46 * tile_size, 4 * tile_size + 100)
                    terroriste1_pos = (6 * tile_size, 4 * tile_size + 75)
                    terroriste2_pos = (21 * tile_size, 4 * tile_size + 75)
                    terroriste3_pos = (38 * tile_size, 4 * tile_size + 75)
                    
                    self.__base = base.Base(self.__base_group, base_pos[0], base_pos[1], (base_pos[0], base_pos[1]))
                    self.__structures.append(structure.Structure(self.__structures_group, structure1_pos[0], structure1_pos[1], (structure1_pos[0], structure1_pos[1]), "batiment", "ville"))
                    self.__structures.append(structure.Structure(self.__structures_group, structure2_pos[0], structure2_pos[1], (structure2_pos[0], structure2_pos[1]), "garage", "ville"))
                    self.__structures.append(structure.Structure(self.__structures_group, structure3_pos[0], structure3_pos[1], (structure3_pos[0], structure3_pos[1]), "garage", "ville"))
                    self.__structures.append(structure.Structure(self.__structures_group, structure4_pos[0], structure4_pos[1], (structure4_pos[0], structure4_pos[1]), "batiment", "ville"))
                    self.__structures.append(structure.Structure(self.__structures_group, structure5_pos[0], structure5_pos[1], (structure5_pos[0], structure5_pos[1]), "batiment", "ville"))
                    self.__structures.append(structure.Structure(self.__structures_group, structure6_pos[0], structure6_pos[1], (structure6_pos[0], structure6_pos[1]), "garage", "ville"))
                    self.__structures.append(structure.Structure(self.__structures_group, structure7_pos[0], structure7_pos[1], (structure7_pos[0], structure7_pos[1]), "batiment", "ville"))
                    if not reload:
                        self.__enemis.add_tank(self.__screen, self.__map.get_map_size(), (tank1_pos[0], tank1_pos[1]))
                        self.__enemis.add_tank(self.__screen, self.__map.get_map_size(), (tank2_pos[0], tank2_pos[1]))
                        self.__enemis.add_tank(self.__screen, self.__map.get_map_size(), (tank3_pos[0], tank3_pos[1]))
                        self.__enemis.add_tank(self.__screen, self.__map.get_map_size(), (tank4_pos[0], tank4_pos[1]))
                        self.__enemis.add_tank(self.__screen, self.__map.get_map_size(), (tank5_pos[0], tank5_pos[1]))
                        self.__enemis.add_terroriste(terroriste1_pos[0], terroriste1_pos[1], (terroriste1_pos[0], terroriste1_pos[1]), "classique")
                        self.__enemis.add_terroriste(terroriste2_pos[0], terroriste2_pos[1], (terroriste2_pos[0], terroriste2_pos[1]), "classique")
                        self.__enemis.add_terroriste(terroriste3_pos[0], terroriste3_pos[1], (terroriste3_pos[0], terroriste3_pos[1]), "classique")
                elif int(id[-1]) == 4:
                    width = 60
                    if int(id[0]) == 1:
                        id = f"Island/{id}"
                    height = 10
                    self.__map = map.Map(f"assets/tilesets/{id}.tmx", width, height, tile_size, self.__screen)
                    self.__player = player.Player(self.__screen, (self.__screen.get_width() / 2 - 13 / 2, 0), self.__map.get_map_size()) # pas fini
                    
                    # Positions
                    base_pos = (30 * tile_size, 4 * tile_size + 30)
                    structure1_pos = (4 * tile_size, 4 * tile_size + 72)
                    structure2_pos = (11 * tile_size, 4 * tile_size + 72)
                    structure3_pos = (20 * tile_size, 4 * tile_size + 72)
                    structure4_pos = (33 * tile_size, 4 * tile_size + 72)
                    structure5_pos = (35 * tile_size, 4 * tile_size + 72)
                    structure6_pos = (39 * tile_size, 4 * tile_size + 72)
                    structure7_pos = (47 * tile_size, 4 * tile_size + 72)
                    structure8_pos = (49 * tile_size, 4 * tile_size + 72)
                    structure9_pos = (55 * tile_size, 4 * tile_size + 72)
                    structure10_pos = (58 * tile_size, 4 * tile_size + 72)
                    tank1_pos = (5 * tile_size, 4 * tile_size + 100)
                    tank2_pos = (24 * tile_size, 4 * tile_size + 100)
                    tank3_pos = (31 * tile_size, 4 * tile_size + 100)
                    tank4_pos = (40 * tile_size, 4 * tile_size + 100)
                    tank5_pos = (46 * tile_size, 4 * tile_size + 100)
                    tank6_pos = (56 * tile_size, 4 * tile_size + 100)
                    tank7_pos = (57 * tile_size, 4 * tile_size + 100)
                    terroriste1_pos = (5 * tile_size, 4 * tile_size + 75)
                    terroriste2_pos = (21 * tile_size, 4 * tile_size + 75)
                    terroriste3_pos = (38 * tile_size, 4 * tile_size + 75)
                    terroriste4_pos = (50 * tile_size, 4 * tile_size + 75)
                    terroriste5_pos = (48 * tile_size, 4 * tile_size + 75)
                    
                    self.__base = base.Base(self.__base_group, base_pos[0], base_pos[1], (base_pos[0], base_pos[1]))
                    self.__structures.append(structure.Structure(self.__structures_group, structure1_pos[0], structure1_pos[1], (structure1_pos[0], structure1_pos[1]), "batiment", "ville"))
                    self.__structures.append(structure.Structure(self.__structures_group, structure2_pos[0], structure2_pos[1], (structure2_pos[0], structure2_pos[1]), "garage", "ville"))
                    self.__structures.append(structure.Structure(self.__structures_group, structure3_pos[0], structure3_pos[1], (structure3_pos[0], structure3_pos[1]), "garage", "ville"))
                    self.__structures.append(structure.Structure(self.__structures_group, structure4_pos[0], structure4_pos[1], (structure4_pos[0], structure4_pos[1]), "batiment", "ville"))
                    self.__structures.append(structure.Structure(self.__structures_group, structure5_pos[0], structure5_pos[1], (structure5_pos[0], structure5_pos[1]), "batiment", "ville"))
                    self.__structures.append(structure.Structure(self.__structures_group, structure6_pos[0], structure6_pos[1], (structure6_pos[0], structure6_pos[1]), "garage", "ville"))
                    self.__structures.append(structure.Structure(self.__structures_group, structure7_pos[0], structure7_pos[1], (structure7_pos[0], structure7_pos[1]), "batiment", "ville"))
                    self.__structures.append(structure.Structure(self.__structures_group, structure8_pos[0], structure8_pos[1], (structure8_pos[0], structure8_pos[1]), "batiment", "ville"))
                    self.__structures.append(structure.Structure(self.__structures_group, structure9_pos[0], structure9_pos[1], (structure9_pos[0], structure9_pos[1]), "batiment", "ville"))
                    self.__structures.append(structure.Structure(self.__structures_group, structure10_pos[0], structure10_pos[1], (structure10_pos[0], structure10_pos[1]), "batiment", "ville"))
                    if not reload:
                        self.__enemis.add_tank(self.__screen, self.__map.get_map_size(), (tank1_pos[0], tank1_pos[1]))
                        self.__enemis.add_tank(self.__screen, self.__map.get_map_size(), (tank2_pos[0], tank2_pos[1]))
                        self.__enemis.add_tank(self.__screen, self.__map.get_map_size(), (tank3_pos[0], tank3_pos[1]))
                        self.__enemis.add_tank(self.__screen, self.__map.get_map_size(), (tank4_pos[0], tank4_pos[1]))
                        self.__enemis.add_tank(self.__screen, self.__map.get_map_size(), (tank5_pos[0], tank5_pos[1]))
                        self.__enemis.add_tank(self.__screen, self.__map.get_map_size(), (tank6_pos[0], tank6_pos[1]))
                        self.__enemis.add_tank(self.__screen, self.__map.get_map_size(), (tank7_pos[0], tank7_pos[1]))
                        self.__enemis.add_terroriste(terroriste1_pos[0], terroriste1_pos[1], (terroriste1_pos[0], terroriste1_pos[1]), "classique")
                        self.__enemis.add_terroriste(terroriste2_pos[0], terroriste2_pos[1], (terroriste2_pos[0], terroriste2_pos[1]), "classique")
                        self.__enemis.add_terroriste(terroriste3_pos[0], terroriste3_pos[1], (terroriste3_pos[0], terroriste3_pos[1]), "classique")
                        self.__enemis.add_terroriste(terroriste4_pos[0], terroriste4_pos[1], (terroriste4_pos[0], terroriste4_pos[1]), "classique")
                        self.__enemis.add_terroriste(terroriste5_pos[0], terroriste5_pos[1], (terroriste5_pos[0], terroriste5_pos[1]), "classique")
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
            self.__game.game_over()
            return # Arreter la fonction
        self.load(id, True)
        self.__player.set_try(player_try)