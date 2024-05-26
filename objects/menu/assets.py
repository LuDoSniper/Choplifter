import pygame

class Assets:
    def __init__(self) -> None:
        self.JAUNE = (152, 120, 2)
        self.BLANC = (255, 255, 255)
        self.BACKGROUND = (239, 204, 172)

        self.GRIS_FONCE = (153, 153, 153)
        self.GRIS_CLAIR = (198, 198, 198)

        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600

        self.THEME = 'Orange'

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption('Choplifter Menu')

        self.custom_font_32 = pygame.font.Font('assets/menu/police.ttf', 32)
        self.custom_font_16 = pygame.font.Font('assets/menu/police.ttf', 14)

        self.bouton = pygame.image.load(f'assets/menu/bouton_{self.THEME}.png').convert_alpha()
        self.background_menu = pygame.image.load(f'assets/menu/background.png').convert()

        self.bouton_jouer = pygame.image.load('assets/menu/bouton_jouer.png').convert_alpha()
        self.background_menu_jouer = pygame.image.load('assets/menu/background_jouer.png').convert()
        self.background_menu_options = pygame.image.load('assets/menu/background_option.png').convert()
        self.background_menu_credits = pygame.image.load('assets/menu/background_credits.png').convert()
        self.background_menu_pause = pygame.image.load('assets/menu/background_pause.png').convert()
        self.bouton_leave = pygame.image.load('assets/menu/leave.png').convert_alpha()
        self.bouton_cancel = pygame.image.load('assets/menu/cancel.png').convert_alpha()
        self.bouton_confirm = pygame.image.load('assets/menu/confirm.png').convert_alpha()
        self.bouton_continue = pygame.image.load('assets/menu/continuer.png').convert_alpha()

        self.new_button_width = int(self.bouton_jouer.get_width() * 1.5)
        self.new_button_height = int(self.bouton_jouer.get_height() * 1.5)

        self.bouton_jouer = pygame.transform.scale(self.bouton_jouer, (self.new_button_width, self.new_button_height))
        self.bouton = pygame.transform.scale(self.bouton, (self.new_button_width, self.new_button_height))
        self.background_menu = pygame.transform.scale(self.background_menu, (int(self.background_menu.get_width() * 0.7), int(self.background_menu.get_height() * 0.7)))
        self.background_menu_jouer = pygame.transform.scale(self.background_menu_jouer, (int(self.background_menu_jouer.get_width() * 0.7), int(self.background_menu_jouer.get_height() * 0.7)))
        self.background_menu_options = pygame.transform.scale(self.background_menu_options, (int(self.background_menu_options.get_width() * 0.9), int(self.background_menu_options.get_height() * 0.9)))
        self.background_menu_credits = pygame.transform.scale(self.background_menu_credits, (int(self.background_menu_credits.get_width() * 0.9), int(self.background_menu_credits.get_height() * 0.9)))
        self.background_menu_pause = pygame.transform.scale(self.background_menu_pause, (int(self.background_menu_pause.get_width() * 0.9), int(self.background_menu_pause.get_height() * 0.9)))

        self.bouton_leave = pygame.transform.scale(self.bouton_leave, (int(self.bouton_leave.get_width() * 0.7), int(self.bouton_leave.get_height() * 0.7)))

        self.click_sound = pygame.mixer.Sound('assets/menu/click_sound.mp3')
        self.background_music = 'assets/menu/background_music.ogg'
        # pygame.mixer.music.load(self.background_music)
        pygame.mixer.music.set_volume(0.5)
        # pygame.mixer.music.play(-1)

    def get_jaune(self):
        return self.JAUNE

    def get_blanc(self):
        return self.BLANC

    def get_background(self):
        return self.BACKGROUND

    def get_gris_fonce(self):
        return self.GRIS_FONCE

    def get_gris_clair(self):
        return self.GRIS_CLAIR

    def get_screen_width(self):
        return self.SCREEN_WIDTH

    def get_screen_height(self):
        return self.SCREEN_HEIGHT

    def get_theme(self):
        return self.THEME

    def get_screen(self):
        return self.screen

    def get_custom_font_32(self):
        return self.custom_font_32

    def get_custom_font_16(self):
        return self.custom_font_16

    def get_bouton(self):
        return self.bouton

    def get_background_menu(self):
        return self.background_menu

    def get_bouton_jouer(self):
        return self.bouton_jouer

    def get_background_menu_jouer(self):
        return self.background_menu_jouer

    def get_background_menu_options(self):
        return self.background_menu_options

    def get_background_menu_credits(self):
        return self.background_menu_credits

    def get_background_menu_pause(self):
        return self.background_menu_pause

    def get_bouton_leave(self):
        return self.bouton_leave

    def get_bouton_cancel(self):
        return self.bouton_cancel

    def get_bouton_confirm(self):
        return self.bouton_confirm

    def get_bouton_continue(self):
        return self.bouton_continue

    def get_new_button_width(self):
        return self.new_button_width

    def get_new_button_height(self):
        return self.new_button_height

    def get_click_sound(self):
        return self.click_sound

    def get_background_music(self):
        return self.background_music
