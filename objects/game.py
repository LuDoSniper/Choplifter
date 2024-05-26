import pygame
import objects.map as map
import objects.player as player
import objects.enemis as enemis
import objects.structure as structure
import objects.hud as hud
import objects.base as base

class Game:
    def __init__(self) -> None:
        self.__screen = pygame.display.set_mode((700, 500))
        pygame.display.set_caption("Choplifter")
        
        # Clock pour les itérations max
        # Pas besoin de geter / seter
        self.__clock = pygame.time.Clock()
        
        # La map pourrais changer de game en game
        self.__map = map.Map(20, 4, 64, self.__screen)
        
        # Il faudra rajouter un autre player pour le mode multi
        self.__player = player.Player(self.__screen, (self.__screen.get_width() / 2 - 13 / 2, 0), self.__map.get_map_size())

        # Class contenant tout les enemis
        self.__enemis = enemis.Enemis(self.__screen)
        # self.get_enemis().add_tank(self.get_screen(), self.__map().get_map_size(), type=1)
        self.get_enemis().add_tank(self.get_screen(), self.__map.get_map_size(), (50, 100), 2)
        self.get_enemis().add_avion(self.get_screen(), self.__map.get_map_size(), type=2)
        
        # Structures
        self.__structures_group = pygame.sprite.Group()
        self.__structures_list = []
        self.__structures_list.append(structure.Structure(self.__structures_group, 200, 72, (200, 72), "batiment", "brick"))
        self.__civil_numbers = self.get_civils_number()
    
        # HUD
        self.__hud = hud.HUD(self.__screen, self.__player.get_try())
    
        # Base
        self.__base_group = pygame.sprite.Group()
        self.__base = base.Base(self.__base_group, 700, 30, (700, 30))
    
        # Easter egg
        self.__egg = []
        self.__egged = False
        
        # Environnement
        self.__paused = False
    
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
    
    def get_hud(self) -> hud.HUD:
        return self.__hud
    def set_hud(self, hud: hud.HUD) -> None:
        self.__hud = hud
    
    # Méthodes
    def handle(self):
        running = True
        while running:
            
            # Affichage
            self.get_map().afficher(self.get_screen())
            self.__base_group.draw(self.__screen)
            self.afficher_structures(self.__egged)
            self.get_player().afficher(self.get_screen())
            self.get_player().afficher_bombs(self.get_screen())
            self.get_player().afficher_bullets(self.get_screen())
            self.get_player().afficher_explosions(self.get_screen())
            self.get_enemis().afficher(self.get_screen())
            self.get_enemis().display_avions_bullets(self.get_screen())
            self.get_enemis().display_tanks_bullet(self.get_screen())
            
            if not self.__paused:
                self.get_player().get_heli().sync_frame()
                self.get_player().get_heli().sync_side(self.get_player().get_dir())
            
            self.__hud.afficher(self.get_player().get_health(), self.get_player().get_fuel(), self.__player.get_storage(), self.__player.get_max_storage(), len(self.get_civils_saved()), self.__civil_numbers, len(self.get_civils_dead()))
            
            # Events uniques
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Touche pressée
                if event.type == pygame.KEYDOWN:
                    
                    if not self.__paused:
                        # Easter egg
                        if event.key == pygame.K_e:
                            if self.__egg == []:
                                self.__egg.append('e')
                            else:
                                self.__egg = []
                        if event.key == pygame.K_g:
                            if self.__egg in (['e'], ['e', 'g']):
                                self.__egg.append('g')
                            else:
                                self.__egg = []
                    
                    if event.key == pygame.K_ESCAPE:
                        self.__paused = not self.__paused
            
            if not self.__paused:
                # Etat des touches
                pressed = pygame.key.get_pressed()
                
                # Lancement d'une bombe
                if pressed[pygame.K_b]:
                    self.get_player().bomber()
                
                # Lancement d'un tir
                if pressed[pygame.K_SPACE]:
                    self.get_player().shoot()
                
                # Mouvements du player
                if self.get_player().get_heli().get_rect().y < 80:
                    dir = pressed[pygame.K_RIGHT] - pressed[pygame.K_LEFT]
                else:
                    dir = 0
                self.get_player().set_dir(dir)
                self.get_player().set_vertical_dir(pressed[pygame.K_UP] - pressed[pygame.K_DOWN])
                self.get_player().move()
                
                # Syncronisation des mouvements
                if self.get_player().get_heli().get_limited():
                    self.get_map().sync_vel(self.get_player().get_velocity())
                    self.get_enemis().sync_vel_tanks(self.get_player().get_velocity(), self.get_map().get_left_border(), self.get_map().get_right_border())
                    self.get_enemis().sync_vel_avions(self.get_player().get_velocity(), self.get_map().get_left_border(), self.get_map().get_right_border())
                    self.get_enemis().sync_vel_explosions(self.get_player().get_velocity(), self.get_map().get_left_border(), self.get_map().get_right_border())
                    self.get_player().sync_vel_bombs(self.get_player().get_velocity(), self.get_map().get_left_border(), self.get_map().get_right_border())
                    self.get_player().sync_vel_bullets(self.get_player().get_velocity(), self.get_map().get_left_border(), self.get_map().get_right_border())
                    self.get_player().sync_vel_explosions(self.get_player().get_velocity(), self.get_map().get_left_border(), self.get_map().get_right_border())
                    self.sync_vel_structures(self.get_player().get_velocity(), self.get_map().get_left_border(), self.get_map().get_right_border())
                    self.__base.sync_vel(self.get_player().get_velocity(), self.get_map().get_left_border(), self.get_map().get_right_border())
                self.get_player().get_heli().sync_vel(self.get_player().get_velocity(), self.get_player().get_vertical_velocity(), self.get_map().get_left_border(), self.get_map().get_right_border(), self.get_player().get_max_height(), self.get_player().get_min_height())
                
                # Gestion des bombes
                if self.get_player().get_bombs_list() != []:
                    self.get_player().bombs_handle(self.get_enemis().get_tanks() + self.get_intacts_structures() + self.get_civils_playable())
                
                # Gestion des bullets
                if self.get_player().get_bullets_list() != []:
                    self.get_player().bullets_handle(self.get_enemis().get_tanks() + self.get_enemis().get_avions() + self.get_intacts_structures() + self.get_civils_playable())
                self.get_enemis().move_avions_bullets([self.get_player()])
                
                # Mouvements des tanks
                self.get_enemis().handle_tanks(self.get_player())
                
                # Mouvement des avions
                self.get_enemis().handle_avions()
                
                # Gestion des explosions
                self.get_player().explosions_handle()
                self.get_enemis().handle_explosions()
                
                # Gestion des structures
                self.handle_structures(self.__map.get_map_size(), self.__base.porte)
                
                # Gestion de la base
                self.__base.handle(self.__player, self.__structures_list)
                
                # Easter egg
                if self.__egg == ['e', 'g', 'g']:
                    self.__egged = True
                else:
                    self.__egged = False
            
            # Rafraichissement de la fenêtre
            pygame.display.flip()
            self.__clock.tick(60)
        
        self.quit()
    
    def handle_structures(self, map_size: int, base_porte: pygame.Rect) -> None:
        for structure in self.__structures_list:
            structure.handle(map_size, self.__player, base_porte)
    
    def get_intacts_structures(self) -> list:
        list = []
        for structure in self.__structures_list:
            if not structure.get_destroyed():
                list.append(structure)
        return list
    
    def get_civils_number(self) -> int:
        n = 0
        for structure in self.__structures_list:
            n += structure.get_civils_number()
        return n
    
    def get_civils(self) -> list:
        list = []
        for structure in self.__structures_list:
            list += structure.get_civils_list()
        return list
    
    def get_civils_dead(self) -> list:
        list = []
        for civil in self.get_civils():
            if civil.get_state() in ("death", "damage"):
                list.append(civil)
        return list
    
    def get_civils_saved(self) -> list:
        list = []
        for civil in self.get_civils():
            if civil.get_saved():
                list.append(civil)
        return list
    
    def get_civils_playable(self) -> list:
        list = []
        for structure in self.__structures_list:
            list += structure.get_civils_playable()
        return list
        
    def afficher_structures(self, egged: bool = False) -> None:
        self.__structures_group.draw(self.__screen)
        for structure in self.__structures_list:
            structure.afficher_civils(self.__screen, egged)
    
    def sync_vel_structures(self, velocity: float, left: bool, right: bool) -> None:
        for structure in self.__structures_list:
            structure.sync_vel(velocity, left, right)
    
    def quit(self) -> None:
        # Sauvegarde surement mais a voir (juste au cas où)
        pass