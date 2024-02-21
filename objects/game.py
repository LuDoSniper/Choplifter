import pygame
import objects.map as map

class Game:
    def __init__(self) -> None:
        self.__screen = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("Choplifter")
    
    def get_screen(self) -> pygame.Surface:
        return self.__screen
    def set_screen(self, screen: pygame.Surface) -> None:
        self.__screen = screen
    
    def handle(self):
        mamap = map.Map()
        
        running = True
        while running:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            pygame.display.flip()
            mamap.afficher(self.get_screen())
        
        self.quit()
    
    def quit(self):
        # Sauvegarde surement mais a voir (juste au cas où)
        pass