import pygame
import random
import objects.civil as civil

class Structure(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group, local_x: int, local_y: int, pos: tuple, type: str, theme: str) -> None:
        super().__init__(group)
        self.__pos = pos
        self.__type = type
        self.__theme = theme
        
        if self.__type == "batiment":
            self.__civils_number = random.randint(3, 5)
        elif self.__type == "garade":
            self.__civils_number = random.randint(1, 3)
        
        self.__state = 2
        self.__destroyed = False
        self.__unloading = False
        self.__civils_group = pygame.sprite.Group()
        self.__civils_list = []
        
        self.image = pygame.image.load(f"assets/structure/{self.__type}/{self.__theme}.png")
        self.image = pygame.transform.scale(self.image, (
            self.image.get_rect().width * 2,
            self.image.get_rect().height * 2
        ))
        self.rect = self.image.get_rect()
        self.rect.x = local_x
        self.rect.y = local_y
        
        self.__pos_tmp = []
        
        self.__egged = False

    # Geter / Seter
    
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
    
    def get_civils_playable(self) -> list:
        list = []
        for civil in self.__civils_list:
            if not civil.get_aboard() and not civil.get_saved() and civil.get_state() not in ("death", "damage"):
                list.append(civil)
        return list
    
    # Méthodes
    
    def sync_vel(self, velocity: float, left: bool, right: bool) -> None:
        # Bouge de la même manière que la map
        if not left and not right:
            self.rect.x -= velocity
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
            self.__civils_list.append(civil.Civil(self.__civils_group, x, self.rect.y + y_offset, (x, self.rect.y + y_offset), gender, type, clothes, self.__egged))
    
    def hit(self, bomb: bool = False) -> None:
        if bomb:
            damage = 2
        else:
            damage = 1
        self.__state -= damage
        if self.__state == 1:
            self.image = pygame.image.load(f"assets/structure/{self.__type}/{self.__theme}-fissure.png")
            self.image = pygame.transform.scale(self.image, (
                self.image.get_rect().width * 2,
                self.image.get_rect().height * 2
            ))
        if not self.__destroyed and self.__state == 0:
            self.__destroyed = True
            self.image = pygame.image.load(f"assets/structure/{self.__type}/{self.__theme}-decombres.png")
            self.image = pygame.transform.scale(self.image, (
                self.image.get_rect().width * 2,
                self.image.get_rect().height * 2
            ))
            self.add_civils()
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
                    civil.set_aboard(False)
                    self.__civils_group.add(civil)
                    civil.set_base(True)
                    civil.rect.x = random.randint(civil.rect.x - 10, civil.rect.x + 10)
                    player.set_storage(player.get_storage() - 1)
        
        # Ne plus gérer les civils sauvés
        for civil in self.__civils_list:
            if civil.get_saved():
                self.__civils_group.remove(civil)
    
    def afficher_civils(self, screen: pygame.Surface, egged: bool = False) -> None:
        self.easter_egg(egged)
        for civil in self.__civils_list:
            if civil.get_aboard() or civil.get_saved():
                self.__civils_group.remove(civil)
        self.__civils_group.draw(screen)
    
    def easter_egg(self, egged: bool) -> None:
        for civil in self.get_civils_list():
            civil.set_egged(egged)