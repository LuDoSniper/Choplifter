import pygame

class Heli:
    def __init__(self) -> None:
        self.__image = pygame.image.load("assets/imgs/Helicopter_tmp_32x13.png")
        self.__rect = self.__image.get_rect()

        self.__resistance = 0
        self.__acceleration = 0
        self.__max_speed = 0
        self.__velocity = 0
    
    # Geter / Seter
    def get_image(self) -> pygame.Surface:
        return self.__image
    def set_image(self, image: pygame.Surface) -> None:
        self.__image = image
    
    def get_rect(self) -> pygame.Rect:
        return self.__rect
    def set_rect(self, rect: pygame.Rect) -> None:
        self.__rect = rect
    
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