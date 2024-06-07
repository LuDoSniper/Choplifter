import pygame
import os
import json
import random
import objects.structure as structure_
import objects.civil as civil_
import objects.tank as tank_
import objects.avion as avion_
import objects.terroriste as terroriste_

class Reloader():
    def __init__(self, path: str = "tmp.json") -> None:
        self.__path = path
    
    def load(self) -> dict:
        if os.path.exists(self.__path):
            with open(self.__path, "r") as fichier:
                data = json.load(fichier)
        else:
            data = None
        return data

    def save(self, data: dict) -> None:
        with open(self.__path, "w") as fichier:
            json.dump(data, fichier, indent=4)
        
    def serialize(self, list: list) -> None:
        data_serialized = []
        for element in list:
            data = {}
            if type(element) == structure_.Structure:
                data["pos"] = element.get_pos()
                data["health"] = element.get_state()
                data["theme"] = element.get_theme()
                data["type"] = element.get_type()
                data["nb_civils"] = element.get_civils_number()
                civils = []
                for civil in element.get_civils_list():
                    civil_data = {}
                    civil_data["pos"] = civil.get_pos()
                    civil_data["state"] = civil.get_state()
                    if civil.get_base():
                        civil.set_saved(True)
                    elif civil.get_aboard():
                        civil.set_saved(False)
                    civil_data["saved"] = civil.get_saved()
                    civil_data["gender"] = civil.get_gender()
                    civil_data["type"] = civil.get_type()
                    civil_data["clothes"] = civil.get_clothes()
                    civils.append(civil_data)
                data["civils"] = civils
            elif type(element) == tank_.Tank:
                data["pos"] = element.get_pos()
                data["health"] = element.get_health()
                data["type"] = element.get_type()
            elif type(element) == avion_.Avion:
                data["type"] = element.get_type()
            elif type(element) == terroriste_.Terroriste and element.get_state not in ("death", "scream"):
                data["pos"] = element.get_pos()
                data["type"] = element.get_type()
            data_serialized.append(data)
        return data_serialized
    
    def deserialize(self, game, screen: pygame.Surface, map_size: int) -> dict:
        data_serialized = self.load()
        data_deserialized = {}
        # Structures
        structures = []
        struct_group = pygame.sprite.Group()
        for structure in data_serialized["structures"]:
            civils = []
            group = pygame.sprite.Group()
            for civil in structure["civils"]:
                civils.append(civil_.Civil(group, None, civil["pos"][0], civil["pos"][1], civil["pos"], civil["gender"], civil["type"], civil["clothes"], game))
            structures.append(structure_.Structure(struct_group, structure["pos"][0], structure["pos"][1], structure["pos"], structure["type"], structure["theme"], game))
            structures[-1].set_civils_list(civils)
            structures[-1].set_state(structure["health"])
            structures[-1].update_image()
            structures[-1].set_civils_group(group)
            structures[-1].set_civils_number(structure["nb_civils"])
            if structure["health"] <= 0:
                structures[-1].set_destroyed(True)
        data_deserialized["structures"] = {}
        data_deserialized["structures"]["list"] = structures
        data_deserialized["structures"]["group"] = struct_group
        # Enemis
        enemis_group = pygame.sprite.Group()
        data_deserialized["enemis_group"] = enemis_group
        # Tanks
        tanks = []
        for tank in data_serialized["tanks"]:
            tanks.append(tank_.Tank(enemis_group, screen, map_size, game, tank["pos"], tank["type"]))
        data_deserialized["tanks"] = tanks
        # Avions
        avions = []
        for avion in data_serialized["avions"]:
            avions.append(avion_.Avion(enemis_group, screen, map_size, game, type=avion["type"], dir=random.choice([-1, 1])))
        data_deserialized["avions"] = avions
        # Terroristes
        terroristes = []
        for terroriste in data_serialized["terroristes"]:
            terroristes.append(terroriste_.Terroriste(enemis_group, terroriste["pos"][0], terroriste["pos"][1], terroriste["pos"], terroriste["type"], game))
        data_deserialized["terroristes"] = terroristes
        return data_deserialized