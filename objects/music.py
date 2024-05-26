import pygame

class Music():
    def __init__(self):
        self.__main_background_layer1 = "assets/menu/Stream Loops 2024-03-30_01_L01.ogg"
        self.__main_background_layer2 = "assets/menu/Stream Loops 2024-03-30_01_L02.ogg"
        self.__mission1 = "assets/son/music/Stream Loops 2024-04-24_01.ogg"
        self.__running = "main_background_layer1"
        self.END_EVENT = pygame.USEREVENT + 1
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
        if self.__running == "mission1":
            music = self.__mission1
            loop = -1
        elif self.__running == "main_background_layer1":
            music = self.__main_background_layer1
        elif self.__running == "main_background_layer2":
            music = self.__main_background_layer2
        
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
        
        if loop:
            pygame.mixer.music.load(music)
            pygame.mixer.music.play(0)