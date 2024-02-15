import pygame
import sys
import random
import math
### CLASSES ###

class Player(pygame.sprite.Sprite):
    def __init__(self,color):
        super(Player,self).__init__()
        self.x = 500
        self.y = 500
        self.image = pygame.Surface((25,50), pygame.SRCALPHA, 32)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(self.x,self.y))
        self.jump_count = 0

    def move(self,deltax,deltay):
        self.rect.centerx += deltax
        self.rect.centery += deltay

    def gravity(self):
        self.y += 5
        self.rect.centery = self.y
        if self.rect.centery > 600:
            self.kill()
            print("Death")
    
    def jump(self):
        if self.jump_count < 20:
            self.y -= 10
            self.rect.centery = self.y
        self.jump_count += 1
    
    def on_ground(self,group):
        for item in group:
            if (item.rect.top < (self.rect.bottom + 10)) and (item.rect.top > (self.rect.bottom - 10)) and (item.rect.left < self.rect.right) and (item.rect.right > self.rect.left):
                return True


class Wall(pygame.sprite.Sprite):
    def __init__(self,x,y,width,length):
        super(Wall,self).__init__()
        self.x = x
        self.y = y
        self.image = pygame.Surface((width,length), pygame.SRCALPHA, 32 )
        self.image.fill(BLACK)
        self.rect = self.image.get_rect(center=(self.x,self.y))








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
PURPLE = (146,79,171)
PINK = (255,0,221)
LIGHT_BLUE = (0,255,255)
FOREST_GREEN = (28,122,78)

# Create clock to later control frame rate
clock = pygame.time.Clock()

# SPRITE GROUPS #
player1 = Player(FOREST_GREEN)
player2 = Player(PURPLE)
players = pygame.sprite.Group()
players.add(player1)
players.add(player2)

walls = pygame.sprite.Group()
floor = Wall(500,580,3000,50)
walls.add(floor)

#making more walls
wallx = 50
wally = 500
for i in range(3):
    walls.add(Wall(wallx,wally,60,10))
    wally -= 90
    wallx += 140
    walls.add(Wall(wallx,wally,60,10))
    wally -= 90
    wallx -= 140



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
    walls.draw(screen)

    keys = pygame.key.get_pressed()

    # PLAYER 1 CONTROLS #
    if keys[pygame.K_UP]:
        player1.jump()

    if keys[pygame.K_LEFT]:
        player1.move(-8,0)
        
    if keys[pygame.K_RIGHT]:
        player1.move(8,0)

    # PLAYER 2 CONTROLS #
    if keys[pygame.K_w]:
        player2.jump()

    if keys[pygame.K_a]:
        player2.move(-8,0)
        
    if keys[pygame.K_d]:
        player2.move(8,0)

    for player in players:
        # on_ground = pygame.sprite.spritecollide(player,walls,False) #spritecollide function idea taken from https://stackoverflow.com/questions/43474849/pygame-sprite-collision-with-sprite-group
         
        if not player.on_ground(walls):
            player.gravity()
        if player.on_ground(walls):
            player.jump_count = 0
    # Update the display
    pygame.display.flip()

    # Set a frame rate to 60 frames per second
    clock.tick(60)

# Quit Pygame properly
pygame.quit()
sys.exit()