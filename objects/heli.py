import pygame
import math

class Heli:
    
    LIMIT = 20
    
    def __init__(self, screen: pygame.Surface) -> None:
        self.__image = pygame.image.load("assets/imgs/Helicopter_tmp_32x13.png")
        self.__rect = self.__image.get_rect()
        self.__rect.x = screen.get_width() / 2 - self.__rect.width / 2
        
        # Pour récuperer la aille d'ecran plus facilement
        self.__screen = screen
    
    # Geter / Seter
    def get_image(self) -> pygame.Surface:
        return self.__image
    def set_image(self, image: pygame.Surface) -> None:
        self.__image = image
    
    def get_rect(self) -> pygame.Rect:
        return self.__rect
    def set_rect(self, rect: pygame.Rect) -> None:
        self.__rect = rect
    
    def get_screen(self) -> pygame.Surface:
        return self.__screen
    def set_screen(self, screen: pygame.Surface) -> None:
        self.__screen = screen
    
    # Méthodes
    def sync_vel(self, velocity: float, dir: int) -> None:
        self.__rect.x += velocity
        
        limit_left = (self.get_screen().get_width() / 2 - self.get_rect().width / 2) - self.LIMIT
        limit_right = (self.get_screen().get_width() / 2 - self.get_rect().width / 2) + self.LIMIT
        if self.__rect.x < limit_left:
            self.__rect.x = limit_left
        elif self.__rect.x > limit_right:
            self.__rect.x = limit_right