import pygame
import objects.map as map
import objects.player as player
import objects.enemis as enemis

class Game:
    def __init__(self) -> None:
        self.__screen = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("Choplifter")
        
        # Clock pour les itérations max
        # Pas besoin de geter / seter
        self.__clock = pygame.time.Clock()
        
        # La map pourrais changer de game en game
        self.__map = map.Map(20, 4, 32, self.__screen)
        
        # Il faudra rajouter un autre player pour le mode multi
        self.__player = player.Player(self.__screen, (self.__screen.get_width() / 2 - 13 / 2, 0), 20 * 32)

        # Class contenant tout les enemis
        self.__enemis = enemis.Enemis()
        self.get_enemis().add_tank(self.get_screen(), 20 * 32)
    
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
    
    def get_enemis(self) -> enemis.Enemis:
        return self.__enemis
    def set_enemis(self, enemis: enemis.Enemis) -> None:
        self.__enemis = enemis
    
    # Méthodes
    def handle(self):
        running = True
        while running:
            
            # Affichage
            self.get_map().afficher(self.get_screen())
            self.get_player().afficher(self.get_screen())
            self.get_player().afficher_bombs(self.get_screen())
            self.get_player().afficher_bullets(self.get_screen())
            self.get_enemis().afficher(self.get_screen())
            
            self.get_player().get_heli().sync_frame()
            self.get_player().get_heli().sync_side(self.get_player().get_dir())
            
            # Events uniques
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Touche pressée
                if event.type == pygame.KEYDOWN:
                    
                    # Lancement d'une bombe
                    if event.key == pygame.K_b:
                        self.get_player().bomber()
                    
                    # Lancement d'un tir
                    if event.key == pygame.K_SPACE:
                        self.get_player().shoot()
            
            # Etat des touches
            pressed = pygame.key.get_pressed()
            
            # Mouvements du player
            self.get_player().set_dir(pressed[pygame.K_RIGHT] - pressed[pygame.K_LEFT])
            self.get_player().set_vertical_dir(pressed[pygame.K_UP] - pressed[pygame.K_DOWN])
            self.get_player().move()
            
            # Syncronisation des mouvements
            if self.get_player().get_heli().get_limited():
                self.get_map().sync_vel(self.get_player().get_velocity())
                self.get_enemis().sync_vel_tanks(self.get_player().get_velocity(), self.get_map().get_left_border(), self.get_map().get_right_border())
                self.get_player().sync_vel_bombs(self.get_player().get_velocity(), self.get_map().get_left_border(), self.get_map().get_right_border())
                self.get_player().sync_vel_bullets(self.get_player().get_velocity(), self.get_map().get_left_border(), self.get_map().get_right_border())
            self.get_player().get_heli().sync_vel(self.get_player().get_velocity(), self.get_player().get_vertical_velocity(), self.get_map().get_left_border(), self.get_map().get_right_border(), self.get_player().get_max_height(), self.get_player().get_min_height())
            
            # Gestion des bombes
            if self.get_player().get_bombs_list() != []:
                self.get_player().bombs_handle(self.get_enemis().get_tanks())
            
            # Gestion des bullets
            if self.get_player().get_bullets_list() != []:
                self.get_player().bullets_handle()
            
            # Mouvements des tanks
            self.get_enemis().handle_tanks(self.get_player().get_pos()[0])
            
            # Rafraichissement de la fenêtre
            pygame.display.flip()
            self.__clock.tick(60)
        
        self.quit()
    
    def quit(self):
        # Sauvegarde surement mais a voir (juste au cas où)
        pass