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
    print(player.velocity)
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
    
    # Mouvement de l'helico
    dir = pressed[pygame.K_RIGHT] - pressed[pygame.K_LEFT]
    player.changer_velocity(dir)
    
    # Mouvement du player
    if dir == 0:
        player.inertie()
        if -0.2 < player.velocity < 0 or 0 < player.velocity < 0.2:
            player.velocity = 0
    player.deplacer()
        
        
    pygame.display.flip()
    clock.tick(frames)

pygame.quit()