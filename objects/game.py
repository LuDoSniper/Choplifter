import pygame
import screeninfo
import objects.mission as mission
import objects.map as map
import objects.player as player
import objects.enemis as enemis
import objects.structure as structure
import objects.hud as hud
import objects.base as base
import objects.menu.assets as assets
import objects.menu.link as link
import objects.music as music
import objects.saver as saver
import objects.requester as requester
import objects.reloader as reloader

class Game:
    def __init__(self, screen: pygame.Surface, assets: assets.Assets, music_manager: music.Music, mode: str, steps: int = None, mission_id: int = None, monde_id: int = None, fullscreen: bool = False) -> None:
        self.__music_manager = music_manager
        self.__save_manager = saver.Saver()
        self.__reload_manager = reloader.Reloader()
        self.__mode = mode
        self.__steps = steps
        self.__mission_id = mission_id
        self.__monde_id = monde_id
        self.__assets = assets
        self.play_song = None
        self.__link = link.Link(self.__assets)
        if mode != "menu":
            self.__link.current_menu = "pause"
        self.__current_menu = self.__link.current_menu
        # fullscreen_int = 0
        # width = self.__assets.get_screen_width()
        # height = self.__assets.get_screen_height()
        # if fullscreen:
        #     fullscreen_int = pygame.FULLSCREEN
        #     monitor = screeninfo.get_monitors()[0]
        #     width = monitor.width
        #     height = monitor.height
        #     print(f"test {fullscreen}")
        self.__screen = screen
        
        # Clock pour les itérations max
        # Pas besoin de geter / seter
        self.__clock = pygame.time.Clock()
        
        # Affichage du chargement
        background = pygame.image.load("assets/imgs/Background.png")
        background = pygame.transform.scale(background, (self.__assets.SCREEN_WIDTH, self.__assets.SCREEN_HEIGHT))
        chargement = pygame.image.load("assets/imgs/chargement.png")
        chargement_rect = chargement.get_rect()
        chargement_rect.x = self.__assets.SCREEN_WIDTH / 2 - chargement_rect.width / 2
        chargement_rect.y = self.__assets.SCREEN_HEIGHT / 2 - chargement_rect.height / 2
        self.__screen.blit(background, background.get_rect())
        self.__screen.blit(chargement, chargement_rect)
        pygame.display.flip()
        
        # Gestionnaire de mission
        nb_try = None
        if self.__mode[:-1] == "new_try_survie":
            nb_try = int(self.__mode[-1])
            self.__mode = "survie"
        if self.__mode == "survie":
            palier = self.__save_manager.load()["survival"]["palier"]
            if palier is not None and mission_id < 3:
                if palier == 8:
                    mission_id = 2
                elif palier == 16:
                    mission_id = 3
            id = f"survie/{self.__monde_id}-{self.__mission_id}"
            print("steps :", steps)
        elif self.__mission_id is not None and self.__monde_id is not None:
            id = f"{self.__monde_id}-{self.__mission_id}"
        elif self.__mode == "sandbox":
            id = "sandbox"
        else:
            id = "map_test"
        self.__mission_manager = mission.Mission(id, self.__screen, self, nb_try)
        
        # La map pourrais changer de game en game
        # self.__map = map.Map(20, 4, 64, self.__screen)
        self.__map = self.__mission_manager.get_map()
        
        # Il faudra rajouter un autre player pour le mode multi
        # self.__player = player.Player(self.__screen, (self.__screen.get_width() / 2 - 13 / 2, 0), self.__map.get_map_size())
        self.__player = self.__mission_manager.get_player()

        # Class contenant tout les enemis
        # self.__enemis = enemis.Enemis(self.__screen)
        # self.get_enemis().add_tank(self.get_screen(), self.__map.get_map_size(), type=1)
        # self.get_enemis().add_tank(self.get_screen(), self.__map.get_map_size(), (50, 100), 2)
        # self.get_enemis().add_avion(self.get_screen(), self.__map.get_map_size(), type=2)
        # self.get_enemis().add_terroriste(10, 75, (10, 75), "classique")
        # self.get_enemis().add_terroriste(30, 75, (30, 75), "kamikaze")
        self.__enemis = self.__mission_manager.get_enemis()
        
        # Structures
        # self.__structures_group = pygame.sprite.Group()
        # self.__structures_list = []
        # self.__structures_list.append(structure.Structure(self.__structures_group, 200, 72, (200, 72), "batiment", "brick"))
        self.__structures_group = self.__mission_manager.get_structures_group()
        self.__structures_list = self.__mission_manager.get_structures_list()
    
        # HUD
        self.__hud = hud.HUD(self.__screen, self.__assets.THEME, self.__player.get_try(), self.__mode == "survie")
    
        # Base
        # self.__base_group = pygame.sprite.Group()
        # self.__base = base.Base(self.__base_group, 700, 30, (700, 30))
        self.__base_group = self.__mission_manager.get_base_group()
        self.__base = self.__mission_manager.get_base()
    
        # Easter egg
        self.__egg = []
        self.__egged = False
        
        # Environnement
        self.__paused = False
        self.__response = None
        self.__running = True
        self.__tmp = None
        self.__civil_numbers = self.get_civils_number()
        self.__civil_dead = 0
        self.__civil_saved = 0
        self.__loading = True
        self.__score = 0
        self.__palier = 0
        data = self.__save_manager.load()
        if data["survival"]["running"]:
            self.__score = data["survival"]["score"]
            self.__palier = data["survival"]["palier"]
    
    # Geter / Seter
    def get_steps(self) -> int:
        return self.__steps
    def set_steps(self, steps: int) -> None:
        self.__steps = steps
    
    def get_score(self) -> int:
        return self.__score
    def set_score(self, score: int) -> None:
        self.__score = score
    def add_score(self, add: int) -> None:
        self.__score += add
    
    def get_monde_id(self) -> int:
        return self.__monde_id
    
    def get_mission_id(self) -> int:
        return self.__mission_id
    
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
    
    def get_response(self) -> str:
        return self.__response
    def set_response(self, response: str) -> None:
        self.__response = response
    
    # Méthodes
    def handle(self):
        while self.__running:
            # Affichage
            if self.__loading:
                background = pygame.image.load("assets/imgs/Background.png")
                background = pygame.transform.scale(background, (self.__assets.SCREEN_WIDTH, self.__assets.SCREEN_HEIGHT))
                chargement = pygame.image.load("assets/imgs/chargement.png")
                chargement_rect = chargement.get_rect()
                chargement_rect.x = self.__assets.SCREEN_WIDTH / 2 - chargement_rect.width / 2
                chargement_rect.y = self.__assets.SCREEN_HEIGHT / 2 - chargement_rect.height / 2
                self.__screen.blit(background, background.get_rect())
                self.__screen.blit(chargement, chargement_rect)
                self.__loading = False
            if self.__mode == "menu":
                self.__screen.fill((239, 204, 172))
                self.__link.draw()
            else:
                self.get_map().afficher(self.get_screen())
                if not(self.__base.rect.x + self.__base.rect.width < 0 or self.__base.rect.x > self.__screen.get_width()):
                    self.__base_group.draw(self.__screen)
                self.afficher_structures(self.__egged)
                self.get_player().afficher(self.get_screen())
                self.get_player().afficher_bombs(self.get_screen())
                self.get_player().afficher_bullets(self.get_screen())
                self.get_player().afficher_explosions(self.get_screen())
                self.get_enemis().afficher(self.get_screen())
                self.get_enemis().afficher_gun(self.get_screen())
                self.get_enemis().afficher_terroristes_explosion(self.get_screen())
                self.get_enemis().display_avions_bullets(self.get_screen())
                self.get_enemis().display_tanks_bullet(self.get_screen())
                self.get_enemis().display_terroristes_bullets(self.__screen)
            
            if not self.__paused and self.__mode != "menu":
                self.get_player().get_heli().sync_frame()
                self.get_player().get_heli().sync_side(self.get_player().get_dir())
            
            if self.__mode != "menu":
                self.__hud.afficher(self.get_player().get_health(), self.get_player().get_fuel(), self.__player.get_storage(), self.__player.get_max_storage(), self.__civil_saved, self.__civil_numbers, self.__civil_dead, self.__score)
            
            # Events uniques
            if self.__mode == "menu":
                if self.__link.stop:
                    self.__response = "exit"
                    self.quit()
                elif self.__link.restart:
                    self.__response = "restart"
                    self.quit()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__response = "exit"
                    self.quit()
                
                if event.type == self.__music_manager.END_EVENT:
                    self.__music_manager.loop()
                
                if self.__mode == "menu" and self.__response != "exit":
                    if self.__link.current_menu == "mission" and self.__current_menu != "mission":
                        self.__music_manager.switch("menu_missions_layer1")
                        self.__current_menu = self.__link.current_menu
                    elif self.__link.current_menu != "mission" and self.__current_menu == "mission":
                        self.__music_manager.switch("main_background_layer1")
                        self.__current_menu = self.__link.current_menu
                    self.__response = self.__link.handle_event(event)
                    if self.__response in ("solo", "sandbox", "new_try", "survie", "survie_next", "survie_retry") or (self.__response is not None and '-' in self.__response):
                        self.quit()
                    elif self.__response == "continue":
                        self.__mode = self.__tmp
                        self.__paused = False
                else:
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
                        
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if self.__link.current_menu == "pause":
                        self.__paused = not self.__paused
                        
                        if self.__paused:
                            self.__tmp = self.__mode
                            self.__link.current_menu = "pause"
                            self.__mode = "menu"
                        else:
                            self.__mode = self.__tmp
            
            if not self.__paused and self.__mode != "menu":
                # Etat des touches
                pressed = pygame.key.get_pressed()
                
                # Lancement d'une bombe
                if pressed[pygame.K_b]:
                    self.get_player().bomber()
                
                # Lancement d'un tir
                if pressed[pygame.K_SPACE]:
                    self.get_player().shoot()
                
                # Mouvements du player
                if self.get_player().get_heli().get_rect().y < self.__player.get_min_height() - (self.__player.get_heli().get_rect().height * 0.5):
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
                    self.get_enemis().sync_vel_terroristes(self.get_player().get_velocity(), self.get_map().get_left_border(), self.get_map().get_right_border())
                    self.get_enemis().sync_vel_explosions(self.get_player().get_velocity(), self.get_map().get_left_border(), self.get_map().get_right_border())
                    self.get_player().sync_vel_bombs(self.get_player().get_velocity(), self.get_map().get_left_border(), self.get_map().get_right_border())
                    self.get_player().sync_vel_bullets(self.get_player().get_velocity(), self.get_map().get_left_border(), self.get_map().get_right_border())
                    self.get_player().sync_vel_explosions(self.get_player().get_velocity(), self.get_map().get_left_border(), self.get_map().get_right_border())
                    self.sync_vel_structures(self.get_player().get_velocity(), self.get_map().get_left_border(), self.get_map().get_right_border())
                    self.__base.sync_vel(self.get_player().get_velocity(), self.get_map().get_left_border(), self.get_map().get_right_border())
                self.get_player().get_heli().sync_vel(self.get_player().get_velocity(), self.get_player().get_vertical_velocity(), self.get_map().get_left_border(), self.get_map().get_right_border(), self.get_player().get_max_height(), self.get_player().get_min_height())
                
                # Gestion du player
                if self.__player.get_health() <= 0:
                    if self.__mode == "solo":
                        self.reload()
                    elif self.__mode == "sandbox":
                        self.__player.set_health(100)
                    elif self.__mode == "survie":
                        self.__player.set_try(self.__player.get_try() - 1)
                        if self.__player.get_try() <= 0:
                            self.__mode = "menu"
                            self.__current_menu = "lose_step"
                            self.__link.current_menu = "lose_step"
                            requests_manager = requester.Requester()
                            requests = {
                                "upload":{
                                    "username": self.__save_manager.load()["username"],
                                    "score": self.__score
                                }
                            }
                            requests_manager.upload(requests)
                            data = self.__save_manager.load()
                            data["survival"] = {
                                    "running" : False,
                                    "score" : None,
                                    "palier": None,
                                    "pb_score" : self.__score,
                                    "pb_palier": self.__palier
                                }
                            self.__save_manager.save(data)
                        else:
                            self.__response = "new_try_survie"
                            self.quit()
                
                # Gestion des bombes
                if self.get_player().get_bombs_list() != []:
                    self.get_player().bombs_handle(self.get_enemis().get_tanks() + self.get_intacts_structures() + self.get_civils_playable() + self.get_enemis().get_terroristes_playable())
                
                # Gestion des bullets
                if self.get_player().get_bullets_list() != []:
                    self.get_player().bullets_handle(self.get_enemis().get_tanks() + self.get_enemis().get_avions() + self.get_intacts_structures() + self.get_civils_playable() + self.get_enemis().get_terroristes_playable())
                self.get_enemis().move_avions_bullets([self.get_player()])
                self.get_enemis().move_terroristes_bullets(self.get_civils_playable())
                
                # Mouvements des tanks
                self.get_enemis().handle_tanks(self.get_player(), self.get_civils_playable(), self.__structures_list)
                
                # Mouvement des avions
                self.get_enemis().handle_avions()
                
                # Gestion des terroristes
                self.get_enemis().handle_terroristes(self.__map.get_map_size(), self.__screen, self.get_civils_playable(), self.__player)
                
                # Gestion des explosions
                self.get_player().explosions_handle(self.get_enemis().get_tanks() + self.get_intacts_structures() + self.get_civils_playable() + self.get_enemis().get_terroristes_playable())
                self.get_enemis().handle_explosions()
                
                # Gestion des structures
                self.handle_structures(self.__map.get_map_size(), self.__base.porte)
                
                # Gestion du despawn des civils
                self.despawn_civils()
                
                # Gestion de la base
                self.__base.handle(self.__player, self.__structures_list)
                
                # Check de la win
                if self.check_end_game():
                    self.__mission_manager.win()
                
                # Easter egg
                if self.__egg == ['e', 'g', 'g']:
                    self.__egged = True
                else:
                    self.__egged = False
            
            # Rafraichissement de la fenêtre
            pygame.display.flip()
            self.__clock.tick(60)
        
        self.quit()
    
    def check_end_game(self) -> bool:
        dead = self.__civil_dead
        saved = self.__civil_saved
        if dead + saved >= self.__civil_numbers:
            if self.__mode != "survie":
                if saved >= self.__civil_numbers / 2:
                    self.win()
                else:
                    self.game_over()
            else:
                self.step_end()
    
    def win(self) -> None:
        self.__current_menu = "win"
        self.__link.current_menu = "win"
        if self.play_song is None: 
            self.__music_manager.victoire()
            self.play_song = True
        self.__mode = "menu"
        data = self.get_data()
        id_mission = self.__mission_id + 1
        id_monde = self.__monde_id
        if id_mission > 4:
            id_mission = 1
            id_monde = self.__monde_id + 1
        if id_monde == 1:
            monde = "Ile Alloca"
        elif id_monde == 2:
            monde = "Foret Alloca"
        elif id_monde == 3:
            monde = "Desert Alloca"
        elif id_monde == 4:
            monde = "Montagne Alloca"
        data["missions"][monde][id_mission - 1] = True
        self.__save_manager.save(data)
        self.__link.set_missions(data["missions"])
        print("win")
    
    def game_over(self) -> None:
        print("game over")
        self.__current_menu = "lose"
        self.__link.current_menu = "lose"
        self.__mode = "menu"
        if self.play_song is None: 
            self.__music_manager.defaite()
            self.play_song = True
    
    def step_end(self) -> None:
        print("Fin de l'étape courante")
        self.__current_menu = "win_step"
        self.__link.current_menu = "win_step"
        if self.play_song is None: 
            self.__music_manager.victoire()
            self.play_song = True
        self.__mode = "menu"
        quotient = (self.__civil_numbers / 250) * self.__civil_saved
        self.__score += quotient * 250
        data = self.__save_manager.load()
        data["survival"]["running"] = True
        data["survival"]["score"] = self.__score
        data["survival"]["palier"] = self.__palier
        self.__save_manager.save(data)
    
    def reload(self) -> None:
        data = {}
        data["structures"] = self.__reload_manager.serialize(self.__structures_list)
        data["tanks"] = self.__reload_manager.serialize(self.__enemis.get_tanks())
        data["avions"] = self.__reload_manager.serialize(self.__enemis.get_avions())
        data["terroristes"] = self.__reload_manager.serialize(self.__enemis.get_terroristes())
        self.__reload_manager.save(data)
        if self.__mission_id is not None and self.__monde_id is not None:
            id = f"{self.__monde_id}-{self.__mission_id}"
        elif self.__mode == "sandbox":
            id = "sandbox"
        else:
            id = "map_test"
        self.__mission_manager = mission.Mission(id, self.__screen, self, self.__player.get_try() - 1, reload=True)
        # origine
        # Mise à jour de game
        self.__map = self.__mission_manager.get_map()
        self.__player = self.__mission_manager.get_player()
        self.__structures_list = self.__mission_manager.get_structures_list()
        self.__structures_group = self.__mission_manager.get_structures_group()
        self.__enemis = self.__mission_manager.get_enemis()
        self.__base = self.__mission_manager.get_base()
        self.__base_group = self.__mission_manager.get_base_group()
        # Mise à jour du HUD
        self.__hud.update_try(self.__player.get_try())
    
    def despawn_civils(self) -> None:
        for structure in self.__structures_list:
            for civil in structure.get_civils_list():
                civil.despawn()
                if civil.get_despawn():
                    structure.remove_civil(civil)
    
    def handle_structures(self, map_size: int, base_porte: pygame.Rect) -> None:
        for structure in self.__structures_list:
            structure.despawn()
            if structure.get_despawn():
                self.__structures_list.pop(self.__structures_list.index(structure))
                self.__structures_group.remove(structure)
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
    
    def add_dead(self) -> None:
        self.__civil_dead += 1
    def add_saved(self) -> None:
        self.__civil_saved += 1
    
    def get_civils_dead(self) -> list:
        # list = []
        # for civil in self.get_civils():
        #     if civil.get_state() in ("death", "damage"):
        #         list.append(civil)
        # return list
        s = 0
        for structure in self.__structures_list:
            s += structure.get_civils_dead()
        return s
    
    def get_civils_saved(self) -> int:
        # list = []
        # for civil in self.get_civils():
        #     if civil.get_saved():
        #         list.append(civil)
        # return list
        s = 0
        for structure in self.__structures_list:
            s += structure.get_civils_saved()
        return s
    
    def get_civils_playable(self) -> list:
        list = []
        for structure in self.__structures_list:
            list += structure.get_civils_playable()
        return list
        
    def afficher_structures(self, egged: bool = False) -> None:
        out_of_screen = []
        for structure in self.__structures_list:
            if structure.rect.x + structure.rect.width < 0 or structure.rect.x > self.__screen.get_width():
                out_of_screen.append(structure)
                self.__structures_group.remove(structure)
        self.__structures_group.draw(self.__screen)
        for structure in self.__structures_list:
            structure.afficher_civils(self.__screen, egged)
        for structure in out_of_screen:
            self.__structures_group.add(structure)
        
    def sync_vel_structures(self, velocity: float, left: bool, right: bool) -> None:
        for structure in self.__structures_list:
            structure.sync_vel(velocity, left, right)
    
    def get_data(self) -> dict:
        data_origine = self.__save_manager.load()
        data = self.__link.get_data()
        data["survival"] = data_origine["survival"]
        data["username"] = data_origine["username"]
        if "ID" in data_origine:
            data["ID"] = data_origine["ID"]
        return data
    
    def set_data(self, data: dict) -> None:
        self.__link.set_volume(data)
        pygame.mixer.music.set_volume(data["music"])
        self.__assets.set_sfx_sound(data["sfx"])
        self.__assets.sfx_volume = data["sfx"]
        self.__assets.music_volume = data["music"]
        self.__assets.THEME = data["theme"]
        self.update_hud()
        self.__link.update_theme(data["theme"])
        self.__link.set_missions(data["missions"])
        self.__link.update_resolution(data["resolution"])
    
    def update_hud(self) -> None:
        self.__hud.update(self.__assets.THEME)
    
    def get_current_menu(self) -> str:
        return self.__link.current_menu
    
    def change_menu(self, target: str) -> None:
        self.__link.change_menu(target)
    
    def quit(self) -> None:
        self.__running = False