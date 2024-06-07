import pygame
import random
import objects.saver as saver

class Music():
    def __init__(self, main: bool = False):
        self.__save_manager = saver.Saver()
        self.__main_background_layer1 = "assets/son/music/Stream Loops 2024-03-30_01_L01.ogg"
        self.__main_background_layer2 = "assets/son/music/Stream Loops 2024-03-30_01_L02.ogg"
        self.__menu_missions_layer1 = "assets/son/music/Stream_Loops_2024-02-14_L01.ogg"
        self.__menu_missions_layer2 = "assets/son/music/Stream_Loops_2024-02-14_L02.ogg"
        self.__menu_missions_layer3 = "assets/son/music/Stream_Loops_2024-02-14_L03.ogg"
        self.__mission1 = "assets/son/music/Stream Loops 2024-04-24_01.ogg"
        self.__monde1_low = "assets/son/music/Original Level Music (Low Intensity) (FULL).wav"
        self.__monde1_high = "assets/son/music/Original Level Music (High Intensity) (FULL).wav"
        self.__monde2_low = "assets/son/music/Blue Sky Level Music (Low Intensity).wav"
        self.__monde2_high = "assets/son/music/Blue Sky Level Music (High Intensity).wav"
        self.__monde3_low = "assets/son/music/ExpendaBros - Level Music (Low Intensity).wav"
        self.__monde3_high = "assets/son/music/ExpendaBros - Level Music (High Intensity).wav"
        self.__monde4_low = "assets/son/music/Hell Level Music (Low Intensity).wav"
        self.__monde4_high = "assets/son/music/Hell Level Music (High Intensity).wav"
        self.__running = "main_background_layer1"
        if main:
            self.END_EVENT = pygame.USEREVENT + 1
            pygame.mixer.music.set_volume(0)
            pygame.mixer.music.set_endevent(self.END_EVENT)
            pygame.mixer.music.load(self.__main_background_layer1)
            pygame.mixer.music.play(0)
    
    # Geter / Seter
    
    def get_main_background_layer1(self) -> str:
        return self.__main_background_layer1
    def set_main_background_layer1(self, path: str) -> None:
        self.__main_background_layer1 = path
        
    def get_main_background_layer2(self) -> str:
        return self.__main_background_layer2
    def set_main_background_layer2(self, path: str) -> None:
        self.__main_background_layer2 = path
    
    def get_running(self) -> str:
        return self.__running
    def set_running(self, running: str) -> None:
        self.__running = running
    
    # Méthodes
    
    def switch(self, target: str) -> None:
        self.__running = target
        loop = 0
        volume = 0
        if self.__running == "mission1":
            music = self.__mission1
            loop = -1
        elif self.__running == "monde1-low":
            music = self.__monde1_low
            loop = -1
            volume = 0.125
        elif self.__running == "monde1-high":
            music = self.__monde1_high
            loop = -1
        elif self.__running == "monde2-low":
            music = self.__monde2_low
            loop = -1
        elif self.__running == "monde2-high":
            music = self.__monde2_high
            loop = -1
        elif self.__running == "monde3-low":
            music = self.__monde3_low
            loop = -1
        elif self.__running == "monde3-high":
            music = self.__monde3_high
            loop = -1
        elif self.__running == "monde4-low":
            music = self.__monde4_low
            loop = -1
        elif self.__running == "monde4-high":
            music = self.__monde4_high
            loop = -1
        elif self.__running == "main_background_layer1":
            music = self.__main_background_layer1
        elif self.__running == "main_background_layer2":
            music = self.__main_background_layer2
        elif self.__running == "menu_missions_layer1":
            music = self.__menu_missions_layer1
        elif self.__running == "menu_missions_layer2":
            music = self.__menu_missions_layer2
        elif self.__running == "menu_missions_layer3":
            music = self.__menu_missions_layer3
        
        pygame.mixer.music.set_volume(self.__save_manager.load()["music"] - volume)
        pygame.mixer.music.stop()
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(loop)
    
    def loop(self) -> None:
        loop = False
        if self.__running == "main_background_layer1":
            self.__running = "main_background_layer2"
            music = self.__main_background_layer2
            loop = True
        elif self.__running == "main_background_layer2":
            self.__running = "main_background_layer1"
            music = self.__main_background_layer1
            loop = True
        elif self.__running == "menu_missions_layer1":
            self.__running = "menu_missions_layer2"
            music = self.__menu_missions_layer2
            loop = True
        elif self.__running == "menu_missions_layer2":
            self.__running = "menu_missions_layer3"
            music = self.__menu_missions_layer3
            loop = True
        elif self.__running == "menu_missions_layer3":
            self.__running = "menu_missions_layer1"
            music = self.__menu_missions_layer1
            loop = True
        
        if loop:
            pygame.mixer.music.load(music)
            pygame.mixer.music.play(0)
    
    def player_shoot(self) -> None:
        shoot = pygame.mixer.Sound("assets/son/sfx/Thompson2_short.wav")
        shoot.set_volume(self.__save_manager.load()["sfx"])
        shoot.play()
    
    def tank_shoot(self) -> None:
        shoot = pygame.mixer.Sound("assets/son/sfx/Firework03_Short.wav")
        shoot.set_volume(self.__save_manager.load()["sfx"])
        shoot.play()
    
    def terroriste_shoot(self) -> None:
        shoot = pygame.mixer.Sound("assets/son/sfx/Machine_Gun_PGI_Single 3.wav")
        shoot.set_volume(self.__save_manager.load()["sfx"])
        shoot.play()
    
    def bomb_explode(self) -> None:
        explosion = pygame.mixer.Sound("assets/son/sfx/ExplosionMediumBig1_Short.wav")
        explosion.set_volume(self.__save_manager.load()["sfx"])
        explosion.play()
    
    def bullet_explode(self) -> None:
        explosion = pygame.mixer.Sound("assets/son/sfx/Explo_Small_01_Short_Violent.wav")
        explosion.set_volume(self.__save_manager.load()["sfx"])
        explosion.play()

    def avion_tire(self) -> None :
        tire = pygame.mixer.Sound('assets/son/game/avion_tire.mp3')
        tire.set_volume(self.__save_manager.load()["sfx"])
        tire.play()

    def cri_1(self) -> None:
        son = pygame.mixer.Sound('assets/son/game/cri-1.aiff')
        son.set_volume(self.__save_manager.load()["sfx"])
        son.play()

    def cri_2(self) -> None:
        son = pygame.mixer.Sound('assets/son/game/cri-2.wav')
        son.set_volume(self.__save_manager.load()["sfx"])
        son.play()

    def defaite(self) -> None:
        son = pygame.mixer.Sound('assets/son/game/defaite.wav')
        son.set_volume(self.__save_manager.load()["sfx"])
        son.play()

    def get_heli_sound(self) -> None:
        son = pygame.mixer.Sound('assets/son/game/helicopter.wav')
        son.set_volume((self.__save_manager.load()["sfx"] * 0.04))
        return son

    def help_1(self) -> None:
        son = pygame.mixer.Sound('assets/son/game/help-1.wav')
        son.set_volume(self.__save_manager.load()["sfx"])
        son.play()

    def help_2(self) -> None:
        son = pygame.mixer.Sound('assets/son/game/help-2.wav')
        son.set_volume(self.__save_manager.load()["sfx"])
        son.play()

    def help_3(self) -> None:
        son = pygame.mixer.Sound('assets/son/game/help-3.wav')
        son.set_volume(self.__save_manager.load()["sfx"])
        son.play()

    def help_5(self) -> None:
        son = pygame.mixer.Sound('assets/son/game/help-5.ogg')
        son.set_volume(self.__save_manager.load()["sfx"])
        son.play()

    def mort_1(self) -> None:
        son = pygame.mixer.Sound('assets/son/game/mort_1.wav')
        son.set_volume(self.__save_manager.load()["sfx"])
        son.play()

    def mort_2(self) -> None:
        son = pygame.mixer.Sound('assets/son/game/mort_2.wav')
        son.set_volume(self.__save_manager.load()["sfx"])
        son.play()

    def mort_3(self) -> None:
        son = pygame.mixer.Sound('assets/son/game/mort_3.wav')
        son.set_volume(self.__save_manager.load()["sfx"])
        son.play()

    def rire_1(self) -> None:
        son = pygame.mixer.Sound('assets/son/game/rire_1.wav')
        son.set_volume(self.__save_manager.load()["sfx"])
        son.play()

    def rire_2(self) -> None:
        son = pygame.mixer.Sound('assets/son/game/rire_2.wav')
        son.set_volume(self.__save_manager.load()["sfx"])
        son.play()

    def rire_3(self) -> None:
        son = pygame.mixer.Sound('assets/son/game/rire_3.wav')
        son.set_volume(self.__save_manager.load()["sfx"])
        son.play()

    def sifflement(self) -> None:
        son = pygame.mixer.Sound('assets/son/game/sifflement.mp3')
        son.set_volume(self.__save_manager.load()["sfx"])
        son.play()

    def victoire(self) -> None:
        son = pygame.mixer.Sound('assets/son/game/victoire.wav')
        son.set_volume(self.__save_manager.load()["sfx"])
        son.play()

    def terroriste_mort_1(self) -> None:
        son = pygame.mixer.Sound('assets/son/game/terroriste_mort_1.wav')
        son.set_volume(self.__save_manager.load()["sfx"])
        son.play()

    def terroriste_mort_2(self) -> None:
        son = pygame.mixer.Sound('assets/son/game/terroriste_mort_2.wav')
        son.set_volume(self.__save_manager.load()["sfx"])
        son.play()

    def terroriste_mort_3(self) -> None:
        son = pygame.mixer.Sound('assets/son/game/terroriste_mort_3.wav')
        son.set_volume(self.__save_manager.load()["sfx"])
        son.play()
    
    def splash(self) -> None:
        sounds = [
            "Blood_Squirt1.wav",
            "Blood_Squirt2.wav",
            "Blood_Squirt3.wav",
            "Blood_Squirt4.wav",
            "Blood_Squirt5.wav",
            "Blood_Squirt1 #85771.wav",
            "Blood_Squirt2_Short.wav",
        ]
        path = f"assets/son/sfx/{random.choice(sounds)}"
        son = pygame.mixer.Sound(path)
        son.set_volume(self.__save_manager.load()["sfx"] * 1.4)
        son.play()