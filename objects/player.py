import pygame
import objects.heli as heli

class Player:
    def __init__(self):
        self.__heli = heli.Heli()
    
    # Geter / Seter
    def get_heli(self) -> heli.Heli:
        return self.__heli
    def set_heli(self, heli: heli.Heli) -> None:
        self.__heli = heli
    
    # Méthodes
    def afficher(self, screen: pygame.Surface) -> None:
        screen.blit(self.get_heli().get_image(), self.get_heli().get_rect())