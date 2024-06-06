import pygame
import random
import time
import objects.civil as civil

class Structure(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group, local_x: int, local_y: int, pos: tuple, type: str, theme: str, game) -> None:
        super().__init__(group)
        self.__pos = pos
        self.__type = type
        self.__theme = theme

        self.__game = game

        if self.__type == "batiment":
            self.__civils_number = random.randint(3, 5)
        elif self.__type == "garage":
            self.__civils_number = random.randint(1, 3)

        self.__state = 2
        self.__despawn = False
        self.__destroyed = False
        self.__unloading = False
        self.__civils_group = pygame.sprite.Group()
        self.__civils_list = []

        self.__despawn_timer = 0
        self.__despawn_timer_delay = 300

        self.image = pygame.image.load(f"assets/structure/{self.__type}/{self.__theme}.png")
        self.image = pygame.transform.scale(self.image, (
            self.image.get_rect().width * 2,
            self.image.get_rect().height * 2
        ))
        self.rect = self.image.get_rect()
        self.rect.x = local_x
        self.rect.y = local_y
        self.hitbox = pygame.Rect(
            self.rect.x,
            self.rect.y,
            self.rect.width,
            self.rect.height
        )

        self.__pos_tmp = []

        self.__egged = False
        self.__civils_saved = 0
        self.__civils_dead = 0
        self.__time_of_destruction = None  # Ajouter cet attribut pour la gestion de la réapparition

    # Getters / Setters
    
    def get_despawn(self) -> bool:
        return self.__despawn
    def set_despawn(self, despawn: bool) -> None:
        self.__despawn = despawn
    
    def get_pos(self) -> tuple:
        return self.__pos
    def set_pos(self, pos: tuple) -> None:
        self.__pos = pos
    
    def get_type(self) -> int:
        return self.__type
    def set_type(self, type: int) -> None:
        self.__type = type
    
    def get_theme(self) -> int:
        return self.__theme
    def set_theme(self, theme: int) -> None:
        self.__theme = theme
    
    def get_civils_number(self) -> int:
        return self.__civils_number
    def set_civils_number(self, n: int) -> None:
        self.__civils_number = n
    
    def get_destroyed(self) -> bool:
        return self.__destroyed
    def set_destroyed(self, destroyed: bool) -> None:
        self.__destroyed = destroyed

    def get_unloading(self) -> bool:
        return self.__unloading
    def set_unloading(self, unloading: bool) -> None:
        self.__unloading = unloading
    
    def get_civils_list(self) -> list:
        return self.__civils_list
    def set_civils_list(self, list: list) -> None:
        self.__civils_list = list
    
    def get_civils_group(self) -> pygame.sprite.Group:
        return self.__civils_group
    def set_civils_group(self, group: pygame.sprite.Group) -> None:
        self.__civils_group = group
        for civil in self.__civils_list:
            civil.set_group(self.__civils_group)
    
    def get_civils_saved(self) -> int:
        return self.__civils_saved
    def set_civils_saved(self, saved: int) -> None:
        self.__civils_saved = saved
    def add_civils_saved(self) -> None:
        self.__game.add_saved()
    
    def get_civils_dead(self) -> int:
        return self.__civils_dead
    def set_civils_dead(self, dead: int) -> None:
        self.__civils_dead = dead
    def add_civils_dead(self) -> None:
        self.__game.add_dead()
    
    def get_civils_playable(self) -> list:
        list = []
        for civil in self.__civils_list:
            if not civil.get_aboard() and not civil.get_saved() and civil.get_state() not in ("death", "damage"):
                list.append(civil)
        return list
    
    # Méthodes
    
    def despawn(self) -> None:
        if self.__destroyed and self.__civils_list == []:
            self.__despawn_timer += 1
            if self.__despawn_timer >= self.__despawn_timer_delay:
                self.__despawn = True
    
    def sync_vel(self, velocity: float, left: bool, right: bool) -> None:
        # Bouge de la même manière que la map
        if not left and not right:
            self.rect.x -= velocity
            self.hitbox.x -= velocity
        # Synchrnise également les civils
        for civil in self.__civils_list:
            civil.sync_vel(velocity, left, right)
    
    def add_civils(self) -> None:
        for i in range(self.__civils_number):
            if random.randint(1, 2) == 1:
                gender = "Male"
            else:
                gender = "Female"
            type = random.randint(1, 3)
            clothes = random.randint(1, 3)
            x = random.randint(self.rect.x - 20, self.rect.x + self.rect.width)
            check = False
            while not check and self.__pos_tmp != []:
                for pos in self.__pos_tmp:
                    if not(pos - 10 <= x <= pos + 10):
                        check = True
                        break
                if not check:
                    x = random.randint(self.rect.x, self.rect.x + self.rect.width)
            self.__pos_tmp.append(x)
            y_offset = 10
            self.__civils_list.append(civil.Civil(self.__civils_group, self, x, self.rect.y + y_offset, (x, self.rect.y + y_offset), gender, type, clothes, self.__egged))
    
    def remove_civil(self, civil) -> None:
        self.__civils_group.remove(civil)
        self.__civils_list.pop(self.__civils_list.index(civil))
    
    def hit(self, bomb: bool = False) -> None:
        if bomb:
            damage = 2
        else:
            damage = 1
        self.__state -= damage
        if self.__state == 1:
            self.update_image()
        if not self.__destroyed and self.__state <= 0:
            self.__destroyed = True
            self.update_image()
            self.add_civils()
            self.__time_of_destruction = time.time()  # Enregistrer le temps de destruction
            # Tuer entre 2 et 3 civils
            if bomb:
                kill = random.randint(2, 3)
                for civil in self.__civils_list:
                    if kill > 0:
                        civil.hit()
                        kill -= 1

    def handle(self, map_size: int, player, base_porte: pygame.Rect) -> None:
        # Gérer les civils
        for civil in self.__civils_list:
            civil.handle(map_size, player, base_porte)
        
        # Gérer le déchargement
        if self.__unloading:
            for civil in self.__civils_list:
                if civil.get_aboard():
                    civil.rect.x = player.get_heli().get_rect().x
                    civil.hitbox.x = civil.rect.x + 24
                    civil.set_aboard(False)
                    self.__civils_group.add(civil)
                    civil.set_base(True)
                    civil.rect.x = random.randint(civil.rect.x - 10, civil.rect.x + 10)
                    civil.hitbox.x = random.randint(civil.hitbox.x - 10, civil.hitbox.x + 10)
                    player.set_storage(player.get_storage() - 1)
        
        # Ne plus gérer les civils sauvés
        for civil in self.__civils_list:
            if civil.get_saved():
                self.__civils_group.remove(civil)
                self.__civils_list.pop(self.__civils_list.index(civil))
                self.__civils_saved += 1
                self.add_civils_saved()
        
        # Vérifier si la structure doit réapparaître
        if self.__destroyed and self.__time_of_destruction is not None:
            if time.time() - self.__time_of_destruction >= 5:  # Réapparaît après 5 secondes
                if self.__game == "sandbox":
                    self.reapparaitre()

    def reapparaitre(self):
        self.__destroyed = False
        self.__state = 2
        self.__time_of_destruction = None
        self.update_image()
    
    def update_image(self) -> None:
        state = ""
        if self.__state == 1:
            state = "-fissure"
        elif self.__state == 0:
            state = "-decombres"
        self.image = pygame.image.load(f"assets/structure/{self.__type}/{self.__theme}{state}.png")
        self.image = pygame.transform.scale(self.image, (
            self.image.get_rect().width * 2,
            self.image.get_rect().height * 2
        ))

    def afficher_civils(self, screen: pygame.Surface, egged: bool = False) -> None:
        self.easter_egg(egged)
        out_of_screen = []
        for civil in self.__civils_list:
            if civil.get_aboard() or civil.get_saved():
                self.__civils_group.remove(civil)
            if civil.rect.x + civil.rect.width < 0 or civil.rect.x > screen.get_width():
                out_of_screen.append(civil)
                self.__civils_group.remove(civil)
        self.__civils_group.draw(screen)
        for civil in out_of_screen:
            self.__civils_group.add(civil)
    
    def easter_egg(self, egged: bool) -> None:
        for civil in self.get_civils_list():
            civil.set_egged(egged)
    
    def get_data(self) -> dict:
        data = {
            "destroyed": self.__destroyed,
            "state": self.__state,
            "pos": self.__pos
        }
        return data

    def set_data(self, data: dict) -> None:
        self.__destroyed = data["destroyed"]
        self.__state = data["state"]
        self.__pos = data["pos"]
        self.update_image()
