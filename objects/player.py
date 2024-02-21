import pygame
import objects.heli as heli

class Player:
    def __init__(self):
        self.__heli = heli.Heli()
        
        self.__resistance = 0
        self.__acceleration = 0
        self.__max_speed = 0
        self.__velocity = 0
    
    # Geter / Seter
    def get_heli(self) -> heli.Heli:
        return self.__heli
    def set_heli(self, heli: heli.Heli) -> None:
        self.__heli = heli
    
    def get_resistance(self) -> float:
        return self.__resistance
    def set_resistance(self, resistance: float) -> None:
        self.__resistance = resistance
    
    def get_acceleration(self) -> float:
        return self.__acceleration
    def set_acceleration(self, acceleration: float) -> None:
        self.__acceleration = acceleration
    
    def get_max_speed(self) -> float:
        return self.__max_speed
    def set_max_speed(self, max_speed: float) -> None:
        self.__max_speed = max_speed
    
    def get_velocity(self) -> float:
        return self.__velocity
    def set_velocity(self, velocity: float) -> None:
        self.__velocity = velocity
    
    # Méthodes
    def afficher(self, screen: pygame.Surface) -> None:
        screen.blit(self.get_heli().get_image(), self.get_heli().get_rect())