import pygame
import math
from objets.helicopter import Helicopter
from objets.map import Map

pygame.init()

# Couleurs
NOIR = (0, 0, 0)

screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Choplifter")

# Initialisation des objects de démarrage
player = Helicopter(screen)
map = Map(screen)
clock = pygame.time.Clock()

# Initialisation des variables de jeu
frames = 60
running = True

while running:

    # Affichage
    
    screen.fill(NOIR)
    
    map.afficher(screen)
    player.afficher(screen)
    
    # Gestion des events instantanés
    
    for event in pygame.event.get():
        
        # Quit
        if event.type == pygame.QUIT:
            running = False

    # Gestion des events perpetuels
    pressed = pygame.key.get_pressed()
    
    # Mouvement de l'helico
    dir = pressed[pygame.K_RIGHT] - pressed[pygame.K_LEFT]
    if math.copysign(1, player.velocity) != dir:
        player.moving = False
    player.accelerer(dir)
    
    if dir == 0:
        player.inertie()
        if -0.2 < player.velocity < 0 or 0 < player.velocity < 0.2:
            player.velocity = 0
            player.moving = False
    player.deplacer(screen)
    
    # Mouvement de la map
    if player.moving:
        map.bouger(player)
        
        
    pygame.display.flip()
    clock.tick(frames)

pygame.quit()