import pygame

class Heli:
    def __init__(self) -> None:
        self.__image = pygame.image.load("assets/imgs/Helicopter_tmp_32x13.png")
        self.__rect = self.__image.get_rect()
    
    # Geter / Seter
    def get_image(self) -> pygame.Surface:
        return self.__image
    def set_image(self, image: pygame.Surface) -> None:
        self.__image = image
    
    def get_rect(self) -> pygame.Rect:
        return self.__rect
    def set_rect(self, rect: pygame.Rect) -> None:
        self.__rect = rect
    
    # Méthodes