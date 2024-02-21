import pygame
import objects.heli as heli

class Player:
    def __init__(self):
        self.__heli = heli.Heli()
        
        self.__resistance = 0.9
        self.__acceleration = 0.5
        self.__max_speed = 3
        self.__velocity = 0
        self.__dir = 0
    
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
    
    def get_dir(self) -> int:
        return self.__dir
    def set_dir(self, dir: int):
        self.__dir = dir
    
    # Méthodes
    def afficher(self, screen: pygame.Surface) -> None:
        screen.blit(self.get_heli().get_image(), self.get_heli().get_rect())
    
    def move(self) -> None:
        self.set_velocity(self.get_velocity() + (self.get_acceleration() * self.get_dir()))
        
        # Application de la resistance
        self.set_velocity(self.get_velocity() * self.get_resistance())
        if abs(self.get_velocity()) < 0.2:
            self.set_velocity(0)
        
        # Brider la velocité
        if abs(self.get_velocity()) > self.get_max_speed():
            self.set_velocity(self.get_max_speed() * self.get_dir())