import pygame
import sys
import random
import math
### CLASSES ###

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        self.x = 500
        self.y = 300
        self.image = pygame.Surface((25,50), pygame.SRCALPHA, 32)
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(self.x,self.y))

    def move(self,deltax,deltay):
        self.rect.centerx += deltax
        self.rect.centery += deltay

class Wall(pygame.sprite.Sprite):
    def __init__(self,x,y,width,length):
        super(Wall,self).__init__()
        self.x = x
        self.y = y
        self.image = pygame.surface((width,length), pygame.SRCALPHA, 32)








# Initialize Pygame and give access to all the methods in the package
pygame.init()

# Set up the screen dimensions
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Tutorial")

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255,0,0)
GREEN = (0,255,0)
SKY = (85,156,187)

# Create clock to later control frame rate
clock = pygame.time.Clock()

# SPRITE GROUPS #
player = Player()
players = pygame.sprite.Group()
players.add(player)



# FONT SURFACES #





# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get(): # pygame.event.get()
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color (e.g., white)
    screen.fill(WHITE)

    players.draw(screen)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player.move(0,-8)
        
    if keys[pygame.K_DOWN]:
        player.move(0,8)

    if keys[pygame.K_LEFT]:
        player.move(-8,0)
        
    if keys[pygame.K_RIGHT]:
        player.move(8,0)
    # Update the display
    pygame.display.flip()

    # Set a frame rate to 60 frames per second
    clock.tick(60)

# Quit Pygame properly
pygame.quit()
sys.exit()