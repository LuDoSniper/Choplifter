import pygame
import objects.map as map
import objects.player as player

class Game:
    def __init__(self) -> None:
        self.__screen = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("Choplifter")
        
        # Clock pour les itérations max
        # Pas besoin de geter / seter
        self.__clock = pygame.time.Clock()
        
        # La map pourrais changer de game en game
        self.__map = map.Map(20, 4, 32)
        
        # Il faudra rajouter un autre player pour le mode multi
        self.__player = player.Player()
    
    # Geter / Seter
    def get_screen(self) -> pygame.Surface:
        return self.__screen
    def set_screen(self, screen: pygame.Surface) -> None:
        self.__screen = screen
    
    def get_map(self) -> map.Map:
        return self.__map
    def set_map(self, map: map.Map) -> None:
        self.__map = map
    
    def get_player(self) -> player.Player:
        return self.__player
    def set_player(self, player: player.Player) -> None:
        self.__player = player
    
    # Méthodes
    def handle(self):
        running = True
        while running:
            
            # Affichage
            self.get_map().afficher(self.get_screen())
            self.get_player().afficher(self.get_screen())
            
            # Events uniques
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Touches pressées
            pressed = pygame.key.get_pressed()
            
            # Mouvements du player
            self.get_player().set_dir(pressed[pygame.K_RIGHT] - pressed[pygame.K_LEFT])
            self.get_player().move()
            print(self.get_player().get_velocity())
            
            # Syncronisation des mouvements
            self.get_map().sync_vel(self.get_player().get_velocity())
            
            # Rafraichissement de la fenêtre
            pygame.display.flip()
            self.__clock.tick(60)
        
        self.quit()
    
    def quit(self):
        # Sauvegarde surement mais a voir (juste au cas où)
        pass