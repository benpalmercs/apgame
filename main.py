import pygame
import sys
import random
import math
### CLASSES ###

class Player(pygame.sprite.Sprite):
    def __init__(self,color):
        super(Player,self).__init__()
        self.x = 0
        self.y = 500
        self.images_standing = [pygame.image.load("kidleft.png").convert_alpha(),pygame.image.load("kidright.png").convert_alpha()]
        self.images_walk_right = [pygame.image.load("kidrightwalk1.png").convert_alpha(), pygame.image.load("kidrightwalk2.png").convert_alpha()]
        self.images_walk_left = [pygame.image.load("kidleftwalk1.png").convert_alpha(), pygame.image.load("kidleftwalk2.png").convert_alpha()]
        self.image = self.images_standing[0]
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect(center=(self.x,self.y))
        self.jump_count = 0
        self.index = 0
        self.heading = "left"
        self.time = 0
        
    # def move(self,deltax,deltay):
    #     if deltax <0:
    #         self.image = self.images[0]
    #     if deltax > 0: 
    #         self.image = self.images[1]
    #     self.image = pygame.transform.scale(self.image, (50,50))
    #     if self.rect.left > 0 and self.rect.right < 1000:
    #         self.rect.centerx += deltax
    #     elif self.rect.left <= 0:
    #         self.rect.centerx +=1
    #     elif self.rect.right >= 1000:
    #         self.rect.centerx -= 1

    def move_right(self):
        self.image = self.images_walk_right[self.index % 2]
        self.image = pygame.transform.scale(self.image, (50,50))
        if self.rect.right <1000:
            self.rect.centerx += 8
        elif self.rect.right >1000:
            self.rect.centerx -= 1
        self.index+=1
        self.heading = "right"

    def move_left(self):
        self.image = self.images_walk_left[self.index % 2]
        self.image = pygame.transform.scale(self.image, (50,50))
        if self.rect.left > 0:
            self.rect.centerx -= 8
        elif self.rect.left < 0:
            self.rect.centerx += 1
        self.index+=1
        self.heading = "left"

    def gravity(self):
        self.y += 5
        self.rect.centery = self.y
        if self.rect.centery > 600:
            self.kill()
            print("Death")
    
    def jump(self):
        if self.jump_count < 20 and (not pygame.sprite.spritecollide(self,walls,False)):
            self.y -= 10
            self.rect.centery = self.y
        self.jump_count += 1
        self.heading = "jump"
    
    def on_ground(self,group):
        for item in group:
            if (item.rect.top < (self.rect.bottom + 5)) and (item.rect.top > (self.rect.bottom - 5)) and (item.rect.left < self.rect.right) and (item.rect.right > self.rect.left):
                return True
            
    def hit_wall(self,move):
        self.rect.centerx += move

    def respawn(self):
        self.rect = self.image.get_rect(center=(self.x,self.y))
        
        


class Wall(pygame.sprite.Sprite):
    def __init__(self,x,y,width,length):
        super(Wall,self).__init__()
        self.x = x
        self.y = y
        self.image = pygame.Surface((width,length), pygame.SRCALPHA, 32 )
        self.image.fill(BLACK)
        self.rect = self.image.get_rect(center=(self.x,self.y))



class Spike(pygame.sprite.Sprite):
    def __init__(self,x,y,width,length):
        super(Spike,self).__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load("spike.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width,length))
        self.rect = self.image.get_rect(center=(self.x,self.y))


class Star(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super(Star,self).__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load("gamestar.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50,50))
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
# players.add(player2)

walls = pygame.sprite.Group()
floor = Wall(500,580,3000,50)
walls.add(floor)

#making more walls
wallx = 50
wally = 500

for i in range(3):
    walls.add(Wall(wallx,wally,60,10))
    wally -= 100
    wallx += 150
    walls.add(Wall(wallx,wally,60,10))
    wally -= 60
    wallx -= 150
walls.add(Wall(250,400,10,700)) #Long Divider from first chute
walls.add(Wall(350,200,10,500)) #Long Divider from rest of course
walls.add(Wall(970,500,60,10)) #Step to 2nd floor
walls.add(Wall(625,400,550,10)) #2nd Floor
walls.add(Wall(395,315,60,10)) #Step to 3rd floor
walls.add(Wall(725,225,550,10)) #3rd Floor
walls.add(Wall(970,125,60,10))

spikes = pygame.sprite.Group()
for i in range(825,425,-150):
    spikes.add(Spike(i,375,30,50))

for i in range(525,950,100):
    spikes.add(Spike(i,210,30,25))

walls.add(spikes)

stars = pygame.sprite.Group()
stars.add(Star(650,25))
    


# FONT SURFACES #
font = pygame.font.SysFont(None, 32)

won = font.render("YOU WON", True, GREEN)
time = font.render(str(player1.time), True, BLACK)

win = False


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
    stars.draw(screen)

    keys = pygame.key.get_pressed()

    # PLAYER 1 CONTROLS #
    if keys[pygame.K_UP]:
        player1.jump()

    if keys[pygame.K_LEFT]:
        player1.move_left()
        
    if keys[pygame.K_RIGHT]:
        player1.move_right()

    # PLAYER 2 CONTROLS #
    # if keys[pygame.K_w]:
    #     player2.jump()

    # if keys[pygame.K_a]:
    #     player2.move(-8,0)
        
    # if keys[pygame.K_d]:
    #     player2.move(8,0)

    for player in players:
        # on_ground = pygame.sprite.spritecollide(player,walls,False) #spritecollide function idea taken from https://stackoverflow.com/questions/43474849/pygame-sprite-collision-with-sprite-group
        if pygame.sprite.spritecollide(player,walls,False):
            if player.heading == "left":
                player.hit_wall(8)
            elif player.heading == "right":
                player.hit_wall(-8)
            elif player.heading == "jump":
                player.rect.centery+=10

        if not player.on_ground(walls):
            player.gravity()

        if player.on_ground(walls):
            player.jump_count = 0
        
        if player.on_ground(spikes):
            player.respawn()
    
    if pygame.sprite.spritecollide(player,stars,False):
        win = True

    if win == True:
        screen.fill(WHITE)
        

    # Updating players time played
    for player in players:
        if player.index % 60 == 0:
            player.time += 1
    # Update the display
    pygame.display.flip()

    # Set a frame rate to 60 frames per second
    clock.tick(60)

# Quit Pygame properly
pygame.quit()
sys.exit()