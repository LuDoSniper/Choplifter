import pygame
import os
import json
import objects.structure as structure_
import objects.civil as civil_

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
            if type(element) == structure_.Structure:
                data = {}
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
            data_serialized.append(data)
        return data_serialized
    
    def deserialize(self, game) -> dict:
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
        return data_deserialized