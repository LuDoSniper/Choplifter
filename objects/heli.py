import pygame

class Heli:
    
    LIMIT = 20
    
    def __init__(self, screen: pygame.Surface) -> None:
        self.__image = pygame.image.load("assets/helico/main/helicopter-1.png")
        self.__image = pygame.transform.scale(self.__image, (
            self.__image.get_rect().width * 1.5,
            self.__image.get_rect().height * 1.5
        ))
        self.__image_tmp = self.__image
        self.__rect = self.__image.get_rect()
        self.__rect.x = screen.get_width() / 2 - self.__rect.width / 2
        self.__rect.y = 5
        self.__center = self.__image.get_rect().center
        
        # Pour la gestion du changement d'image
        self.__frame = 1
        self.__frame_speed = 3
        self.__frame_tmp = 0
        
        # Dire si la map doit bouger ou non
        self.__limited = False
        
        # Suivre l'orientation de l'image
        # False -> droite
        # True  -> gauche
        self.__sens = False
        
        # Pour récuperer la aille d'ecran plus facilement
        self.__screen = screen
    
    # Geter / Seter
    def get_image(self) -> pygame.Surface:
        return self.__image
    def set_image(self, image: pygame.Surface) -> None:
        self.__image = image
    
    def get_image_tmp(self) -> pygame.Surface:
        return self.__image_tmp
    def set_image_tmp(self, image_tmp: pygame.Surface) -> None:
        self.__image_tmp = image_tmp
    
    def get_rect(self, center:bool = False) -> pygame.Rect:
        # if center:
        #     return self.get_image().get_rect(center=self.get_center())
        return self.__rect
    def set_rect(self, rect: pygame.Rect) -> None:
        self.__rect = rect
    
    def get_center(self) -> int:
        return self.__center
    def set_center(self, center: int) -> None:
        self.__center = center
    
    def get_frame(self) -> int:
        return self.__frame
    def set_frame(self, frame: int) -> None:
        self.__frame = frame
        
    def get_frame_speed(self) -> float:
        return self.__frame_speed
    def set_frame_speed(self, frame_speed: float) -> None:
        self.__frame_speed = frame_speed
        
    def get_frame_tmp(self) -> float:
        return self.__frame_tmp
    def set_frame_tmp(self, frame_tmp: float) -> None:
        self.__frame_tmp = frame_tmp
    
    def get_limited(self) -> bool:
        return self.__limited
    def set_limited(self, limited: bool) -> None:
        self.__limited = limited
    
    def get_sens(self) -> bool:
        return self.__sens
    def set_sens(self, sens: bool) -> None:
        self.__sens = sens
    
    def get_screen(self) -> pygame.Surface:
        return self.__screen
    def set_screen(self, screen: pygame.Surface) -> None:
        self.__screen = screen
    
    # Méthodes
    def sync_vel(self, velocity: float, vertical_velocity: float, left_border: bool, right_border: bool, top_limit: int, bottom_limit: int) -> None:
        self.__rect.x += velocity
        self.__rect.y -= vertical_velocity
        
        # Bride le mouvement de l'helico
        if left_border:
            limit_left = 0
        else:
            limit_left = (self.get_screen().get_width() / 2 - self.get_rect().width / 2) - self.LIMIT
        if right_border:
            limit_right = self.get_screen().get_width() - self.get_rect().width
        else:
            limit_right = (self.get_screen().get_width() / 2 - self.get_rect().width / 2) + self.LIMIT
        
        if self.__rect.x < limit_left:
            self.__rect.x = limit_left
            self.set_limited(True)
        elif self.__rect.x > limit_right:
            self.__rect.x = limit_right
            self.set_limited(True)
        else:
            self.set_limited(False)
    
        if self.__rect.y < top_limit:
            self.__rect.y = top_limit
        elif self.__rect.y > bottom_limit:
            self.__rect.y = bottom_limit
    
    # Fait tourner l'image de l'helico
    def sync_side(self, dir: int) -> None:
        if dir < 0 and not self.get_sens() or dir > 0 and self.get_sens():
            self.set_image(pygame.transform.flip(self.get_image(), True, False))
            self.set_sens(not(self.get_sens()))
    
    # Fait changer d'image
    def sync_frame(self):
        self.set_image(pygame.image.load(f"assets/helico/main/helicopter-{self.get_frame()}.png"))
        self.__image = pygame.transform.scale(self.__image, (
            self.__image.get_rect().width * 1.5,
            self.__image.get_rect().height * 1.5
        ))
        if self.__sens:
            self.set_image(pygame.transform.flip(self.get_image(), True, False))
        
        # Incrémenter frame
        if self.__frame_tmp < self.__frame_speed:
            self.__frame_tmp += 1
        elif self.__frame_tmp == self.__frame_speed:
            self.__frame_tmp = 0
            
            self.__frame += 1
            if self.__frame >= 5:
                self.__frame = 1
    
    # Fait rotate l'image de l'helico
    def rotate(self, angle: int) -> None:
        tmp = 1
        if angle < 0:
            tmp = -1
        angle -= tmp * 90
        self.set_image_tmp(pygame.transform.rotate(self.get_image(), -angle))
        # self.set_rect(self.get_image().get_rect(center=self.get_image_tmp().get_rect().center))