import pygame
from objets.helicopter import Helicopter

pygame.init()

# Couleurs
NOIR = (0, 0, 0)

screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Choplifter")

# Initialisation des objects de démarrage
player = Helicopter(screen)
clock = pygame.time.Clock()

# Initialisation des variables de jeu
frames = 60
running = True

while running:
    
    # Affichage
    
    screen.fill(NOIR)
    
    player.afficher(screen)
    
    # Gestion des events instantanés
    
    for event in pygame.event.get():
        
        # Quit
        if event.type == pygame.QUIT:
            running = False
        
    # Gestion des events perpetuels
    pressed = pygame.key.get_pressed()
    
    # Flèche de gauche
    if pressed[pygame.K_LEFT] != 0:
        player.changer_velocity(-1)
    
    # Flèche de droite
    if pressed[pygame.K_RIGHT] != 0:
        player.changer_velocity(1)
    
    # Mouvement du player
    if player.velocity != 0:
        player.inertie()
        player.deplacer()
        if -0.2 < player.velocity < 0 or 0 < player.velocity < 0.2:
            player.velocity = 0
        
    pygame.display.flip()
    clock.tick(frames)

pygame.quit()