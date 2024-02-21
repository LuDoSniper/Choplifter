import pygame

class Game:
    def __init__(self) -> None:
        self.__screen = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("Choplifter")
    
    def get_screen(self) -> pygame.Surface:
        return self.__screen
    def set_screen(self, screen: pygame.Surface) -> None:
        self.__screen = screen
    
    def handle(self):
        running = True
        while running:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        
        self.quit()
    
    def quit(self):
        # Sauvegarde surement mais a voir (juste au cas où)
        pass