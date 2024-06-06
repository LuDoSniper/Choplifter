import pygame
import random
import objects.bullets as bullets
import objects.explosion as explosion
import objects.music as music

class Terroriste(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group, local_x: int, local_y: int, pos: tuple, type: str):
        super().__init__(group)
        self.__music_manager = music.Music()
        self.__type = type
        
        self.group = group
        self.image = pygame.image.load(f"assets/terroriste/{type}/idle 1/0.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_rect().width * 1.75, self.image.get_rect().height * 1.75))
        self.rect = self.image.get_rect()
        self.rect.x = local_x
        self.rect.y = local_y
        self.hitbox = pygame.Rect(
            self.rect.x + 10 * 1.75,
            self.rect.y + 13 * 1.75,
            12 * 1.75,
            18 * 1.75
        )
        if type == "classique":
            self.gun_image = pygame.image.load(f"assets/terroriste/{type}/gun/idle/0.png")
            self.gun_image = pygame.transform.scale(self.gun_image, (self.gun_image.get_rect().width * 1.75, self.gun_image.get_rect().height * 1.75))
            self.gun_rect = self.gun_image.get_rect()
            self.gun_rect.x = self.rect.x
            self.gun_rect.y = self.rect.y
        
        self.__despawn = False
        self.__speed = 1
        self.__range = 150
        self.__shooting = False
        self.__exploding = False
        self.__explosion = None
        self.__explosion_group = pygame.sprite.Group()
        
        self.__pos = pos
        self.__bullets = []
        self.__bullets_group = pygame.sprite.Group()
        
        self.__reversed = False
        self.__dir = 0
        self.__state = "idle"
        self.__death_variation = random.randint(1, 2)
        self.__gun_state = "idle"
        self.__idle_variation = random.randint(1, 3)
        self.__frame = 0
        self.__animation_timer = 0
        self.__animation_timer_delay = 5
        self.__gun_frame = 0
        self.__animation_gun_timer = 0
        self.__animation_gun_timer_delay = 10
        self.__state_timer_delay = random.randint(150, 250)
        self.__state_timer = self.__state_timer_delay
        self.__shooting_delay = 60
        self.__shooting_timer = self.__shooting_delay
        self.__exploding_timer = 0
        self.__exploding_delay = 60
        self.__despawn_timer = 0
        self.__despawn_timer_delay = 300
        
    # Geter / Seter
    
    def get_group(self) -> pygame.sprite.Group:
        return self.group
    def set_group(self, group: pygame.sprite.Group) -> None:
        self.group = group
        super().__init__(group)
    
    def get_despawn(self) -> bool:
        return self.__despawn
    def set_despawn(self, despawn: bool) -> None:
        self.__despawn = despawn
    
    def get_pos(self) -> tuple:
        return self.__pos
    def set_pos(self, pos: tuple) -> None:
        self.__pos = pos
    
    def get_bullets_list(self) -> list:
        return self.__bullets
    def set_bullets_list(self, bullets: list) -> None:
        self.__bullets = bullets
        
    def get_bullets_group(self) -> pygame.sprite.Group:
        return self.__bullets_group
    def set_bullets_group(self, group: list) -> None:
        self.__bullets_group = group
    
    def get_state(self) -> str:
        return self.__state
    
    # Méthodes
    
    def despawn(self) -> None:
        if self.__state in ("blood", "death"):
            self.__despawn_timer += 1
            if self.__despawn_timer >= self.__despawn_timer_delay:
                self.__despawn = True
    
    def handle(self, map_size: int, screen: pygame.Surface, civils: list, player) -> None:
        self.animate()
        self.sync_side()
        if self.__state not in ("death", "blood"):
            self.scan(screen, civils)
            
            self.__shooting_timer += 1
            self.__state_timer += 1
            if self.__state_timer >= self.__state_timer_delay and self.__state != "death":
                self.__state_timer = 0
                self.__state_timer_delay = random.randint(150, 250)
                
                if random.randint(1, 2) == 1:
                    self.__state = "idle"
                    self.__idle_variation = random.randint(1, 3)
                    self.__dir = 0
                else:
                    self.__state = "run"
                    self.__dir = random.choice([-1, 1])
            
            if self.__state in ("run", "scream"):
                self.move(map_size)
            
            if self.__type == "classique":
                self.gun_rect = self.rect
            
        if self.__exploding:
            self.explode_civils(civils)
            self.__exploding_timer += 1
            if self.__exploding_timer >= self.__exploding_delay and self.__state != "blood":
                self.__state = "blood"
                self.__frame = random.randint(0, 3)
                self.explode()
            if self.__explosion != None and self.__explosion.explode():
                self.__explosion = None
        
        if self.hitbox.colliderect(player.get_heli().hitbox):
            self.hit()
    
    def explode(self) -> None:
        self.__explosion = explosion.Explosion(self.__explosion_group, self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2, (self.__pos[0] + self.rect.width / 2, self.__pos[1] + self.rect.height / 2))
    
    def move(self, map_size: int) -> None:
        self.rect.x += self.__speed * self.__dir
        self.hitbox.x += self.__speed * self.__dir
        self.__pos = (self.__pos[0] + self.__speed * self.__dir, self.__pos[1])
        
        if self.__state == "scream":
            self.__speed = 2
        else:
            self.__speed = 1
        
        # Empecher de sortir de la map
        if self.__pos[0] < 0:
            tmp = self.__pos[0]
            self.__pos = (0, self.__pos[1])
            self.rect.x -= tmp
            self.hitbox.x -= tmp
        elif self.__pos[0] > map_size:
            tmp = self.__pos[0]
            self.__pos = (map_size - self.rect.width, self.__pos[1])
            self.rect.x -= map_size - tmp - self.rect.width
            self.hitbox.x -= map_size - tmp - self.rect.width
    
    def animate(self) -> None:
        if self.__state != "blood":
            self.__animation_timer += 1
            if self.__animation_timer >= self.__animation_timer_delay:
                self.__animation_timer = 0
                self.__frame += 1
                
            self.__animation_gun_timer +=1
            if self.__animation_gun_timer >= self.__animation_gun_timer_delay:
                self.__animation_gun_timer = 0
                self.__gun_frame += 1
        
        
        state = self.__state
        if self.__state == "idle":
            if self.__idle_variation == 1:
                max = 7
            elif self.__idle_variation == 2:
                max = 4
            elif self.__idle_variation == 3:
                max = 11
            
            if self.__frame > max:
                self.__idle_variation = random.randint(1, 3)
                self.__frame = 0
        elif self.__state == "run":
            if self.__frame > 7:
                self.__frame = 0
        
        elif self.__state == "shoot":
            state = "idle"
            self.__idle_variation = 3
            self.__frame = 2
        
        elif self.__state == "death" and self.__frame >= 15:
            self.__frame = 15
        
        elif self.__state == "scream" and self.__frame > 7:
            self.__frame = 0
        
        if self.__gun_state == "idle" and self.__gun_frame > 23: # 31
            self.__gun_frame = 0
        elif self.__gun_state == "shoot" and self.__gun_frame > 3:
            self.__shooting = False
            self.__gun_state = "idle"
            self.__gun_frame = 0
            self.__state = "idle"
            state = "idle"
            self.__frame = 0
            self.__idle_variation = random.randint(1, 3)
            self.__animation_gun_timer_delay = 10
        elif self.__gun_state == "drop" and self.__gun_frame >= 5:
            self.__gun_frame = 5
        
        variation = ""
        if self.__state == "idle":
            variation = " " + str(self.__idle_variation)
        elif self.__state == "death" and self.__type == "classique":
            variation = " " + str(self.__death_variation)
        self.image = pygame.image.load(f"assets/terroriste/{self.__type}/{state}{variation}/{self.__frame}.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_rect().width * 1.75, self.image.get_rect().height * 1.75))
        if self.__type == "classique":
            self.gun_image = pygame.image.load(f"assets/terroriste/{self.__type}/gun/{self.__gun_state}/{self.__gun_frame}.png")
            self.gun_image = pygame.transform.scale(self.gun_image, (self.gun_image.get_rect().width * 1.75, self.gun_image.get_rect().height * 1.75))
    
        if self.__reversed:
            self.image = pygame.transform.flip(self.image, True, False)
            if self.__type == "classique":
                self.gun_image = pygame.transform.flip(self.gun_image, True, False)
    
    def scan(self, screen: pygame.Surface, civils: list) -> None:
        for civil in civils:
            if civil.rect.x - self.__range <= self.rect.x <= civil.rect.x + self.__range and not self.__shooting and self.__shooting_timer >= self.__shooting_delay:
                if self.rect.x < civil.rect.x:
                    self.__dir = 1
                elif self.rect.x > civil.rect.x:
                    self.__dir = -1

                if self.__type == "classique":
                    self.__state = "shoot"
                    self.__gun_state = "shoot"
                    self.__gun_frame = 0
                    self.__shooting_timer = 0
                    self.__animation_gun_timer_delay = 5
                    self.__shooting = True
                    self.shoot(screen)
                elif self.__type == "kamikaze":
                    self.__state = "scream"
                    self.__exploding = True
    
    def explode_civils(self, civils: list) -> None:
        for civil in civils:
            if self.__explosion != None and self.__explosion.hitbox.colliderect(civil.hitbox):
                civil.hit()
    
    def shoot(self, screen: pygame.Surface) -> None:
        # x
        offset = 0
        if self.__dir > 0:
            offset = self.rect.width
        x = self.rect.x + offset
        # y
        y = self.rect.y + self.rect.height / 2
        # pos
        pos = (
            self.__pos[0] + x,
            self.__pos[1] + y
        )
        
        self.__bullets.append(bullets.Bullet(self.__bullets_group, screen, self, self.__dir, self.__dir * 90, pos, x, y, size=0.5))
        self.__music_manager.terroriste_shoot()
    
    def bullets_handle(self, target: list) -> None:
        for bullet in self.__bullets:
            bullet.move(target)
    
    def hit(self) -> None:
        if self.__state != "death":
            self.__state = "death"
            self.__gun_state = "drop"
            self.__frame = 0
            self.__gun_frame = 0
    
    def sync_side(self) -> None:
        if (self.__dir == -1 and not self.__reversed) or (self.__dir == 1 and self.__reversed):
            self.image = pygame.transform.flip(self.image, True, False)
            if self.__type == "classique":
                self.gun_image = pygame.transform.flip(self.gun_image, True, False)
            self.__reversed = not self.__reversed
    
    def sync_vel(self, velocity: float, left: bool, right: bool) -> None:
        # Bouge de la même manière que la map
        if not left and not right:
            self.rect.x -= velocity
            self.hitbox.x -= velocity
            self.gun_rect = self.rect
        # Pour les balles
        for bullet in self.__bullets:
            bullet.sync_vel(velocity, left, right)
        # Pour l'explosion
        if self.__explosion is not None:
            self.__explosion.sync_vel(velocity, left, right)
    
    def afficher_gun(self, screen: pygame.Surface) -> None:
        if self.__type == "classique" and not(self.gun_rect.x + self.gun_rect.width < 0 or self.gun_rect.x > screen.get_width()):
            screen.blit(self.gun_image, self.gun_rect)
    
    def afficher_explosion(self, screen: pygame.Surface) -> None:
        if self.__explosion is not None and not(self.__explosion.rect.x + self.__explosion.rect.width < 0 or self.__explosion.rect.x > screen.get_width()):
            if self.__explosion is not None:
                self.__explosion_group.draw(screen)
    
    def get_data(self) -> dict:
        data = {
            "alive": self.__state not in ("death", "scream"),
            "pos": self.__pos
        }
        return data
    def set_data(self, data: dict) -> None:
        if not data["alive"]:
            self.hit()
        self.__pos = data["pos"]