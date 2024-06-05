import os
import json

class Saver():
    def __init__(self, path: str = 'save.json') -> None:
        self.__path = path
    
    # Geter / Seter
    
    def get_path(self) -> str:
        return self.__path
    def set_path(self, path: str) -> None:
        self.__path = path
    
    # Méthodes
    
    def save(self, data: dict) -> None:
        with open('save.json', 'w') as file:
            json.dump(data, file, indent=4)
        
    def load(self) -> dict:
        if os.path.exists('save.json'):
            with open('save.json') as file:
                return json.load(file)
        else:
            return {
                "music" : 0.5,
                "sfx" : 0.5,
                "theme" : "Gris",
                "missions" : {
                    "Ile Alloca": [True, False, False, False],
                    "Foret Alloca": [False, False, False, False],
                    "Desert Alloca": [False, False, False, False],
                    "Montagne Alloca": [False, False, False, False]
                }
            }