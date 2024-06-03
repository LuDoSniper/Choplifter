import pygame
import player as player
import tank as tank
import avion as avion
import terroriste as terroriste
import structure as structure

class Mission():
    def __init__(self, id: int) -> None:
        self.__id = id
    
    # Geter / Seter
    
    def get_id(self) -> int:
        return self.__id
    def set_id(self, id: int) -> None:
        self.__id = id