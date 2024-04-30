import pygame
import sys
import random
import math
### CLASSES ###

class Player(pygame.sprite.Sprite):
    def __init__(self,color):
        super(Player,self).__init__()
        self.x = 115
        self.y = 520
        self.images_standing = [pygame.image.load("kidleft.png").convert_alpha(),
                                pygame.image.load("kidright.png").convert_alpha()]
        self.images_walk_right = [pygame.image.load("kidrightwalk1.png").convert_alpha(),
                                  pygame.image.load("kidrightwalk2.png").convert_alpha()]
        self.images_walk_left = [pygame.image.load("kidleftwalk1.png").convert_alpha(), 
                                 pygame.image.load("kidleftwalk2.png").convert_alpha()]
        self.image = self.images_standing[0]
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect(center=(self.x,self.y))
        self.jump_count = 0
        self.index = 0
        self.heading = "left"
        self.jumping = False
        self.time = 0

    def move_right(self):
        if self.index % 12 == 0:
            self.image = self.images_walk_right[0]
        elif self.index % 12 == 6:
            self.image = self.images_walk_right[1]
        self.image = pygame.transform.scale(self.image, (50,50))
        if self.rect.right <1000:
            self.rect.centerx += 8
        elif self.rect.right >1000:
            self.rect.centerx -= 1
        self.index+=1
        self.heading = "right"

    def move_left(self):
        if self.index % 12 == 0:
            self.image = self.images_walk_left[0]
        elif self.index % 12 == 6:
            self.image = self.images_walk_left[1]
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
        self.jumping = True
        if self.jump_count > 20:
            self.jumping = False
    
    def on_ground(self,group):
        for item in group:
            if (item.rect.top < (self.rect.bottom + 5)) and (item.rect.top > (self.rect.bottom - 5)) and (item.rect.left < self.rect.right) and (item.rect.right > self.rect.left):
                return True
            
    def hit_wall(self,move):
        self.rect.centerx += move

    def respawn(self):
        self.rect.centerx = 50
        self.rect.centery = 520
        
        


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
        self.image = pygame.image.load("gamestar1.png").convert_alpha()
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
wally = 480

for i in range(3):
    walls.add(Wall(wallx,wally,60,10))
    wally -= 80
    wallx += 150
    walls.add(Wall(wallx,wally,60,10))
    wally -= 80
    wallx -= 150
walls.add(Wall(250,400,10,700)) #Long Divider from first chute
walls.add(Wall(350,200,10,550)) #Long Divider from rest of course
walls.add(Wall(970,500,60,10)) #Step to 2nd floor
walls.add(Wall(625,400,550,10)) #2nd Floor
walls.add(Wall(395,315,60,10)) #Step to 3rd floor
walls.add(Wall(725,225,550,10)) #3rd Floor
walls.add(Wall(970,125,60,10)) #Step to Star

spikes = pygame.sprite.Group()
# 2nd Floor Spikes
for i in range(825,425,-150):
    spikes.add(Spike(i,375,30,50))
# 3rd Floor Spikes
for i in range(525,950,100):
    spikes.add(Spike(i,210,20,25))

walls.add(spikes)

stars = pygame.sprite.Group()
stars.add(Star(650,25))
    


win = False
index = 0
timer = 0

# FONT SURFACES #
font = pygame.font.SysFont(None, 70)

won = font.render("YOU WON", True, GREEN)
time_score = font.render(str(timer), True, BLACK)
time_word = font.render("TIME:",True,BLACK)
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
    if keys[pygame.K_UP]: # or player1.jumping == True
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
        if pygame.sprite.spritecollide(player,walls,False):
            if player.heading == "left":
                player.hit_wall(8)
            elif player.heading == "right":
                player.hit_wall(-8)
            elif player.heading == "jump":
                player.rect.centery+=10
                player.jump_count = 20

        if not player.on_ground(walls):
            player.gravity()

        if player.on_ground(walls):
            player.jump_count = 0
            player.jumping = False
        
        if player.on_ground(spikes) and player.jumping == False:
            player.respawn()
    
    if pygame.sprite.spritecollide(player,stars,False):
        win = True

    if win:
        screen.fill(WHITE)
        screen.blit(won,(400,200))
        screen.blit(time_word,(425,300))
        screen.blit(time_score,(570,300))
        

    # Updating players time played
    elif win != True:
 
        if index % 60 == 0:
            timer += 1
            time_score = font.render(str(timer), True, BLACK)
        screen.blit(time_score,(0,0))
    index += 1
    # Update the display
    pygame.display.flip()

    # Set a frame rate to 60 frames per second
    clock.tick(60)

# Quit Pygame properly
pygame.quit()
sys.exit()

