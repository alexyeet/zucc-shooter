# Imports
import pygame

# Initialize game engine
pygame.init()


# Window
WIDTH = 1200
HEIGHT = 650
SIZE = (WIDTH, HEIGHT)
TITLE = "Space War"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (150, 255, 150)

# Images



# Game classes
class Ship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 150
        self.h = 72
        self.speed = 3
        self.shield = 10

    def move_left(self):
        self.x -= self.speed
        
    def move_right(self):
        self.x += self.speed

    def shoot(self):
        x = self.x + 50
        y = self.y
        laser = Laser(x, y)
        lasers.append(laser)

    def update(self):
        pass

    def draw(self):
        cnn = pygame.image.load("cnn.png")
        screen.blit(cnn, [self.x, self.y])
    
class Laser:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 75
        self.h = 53
        self.speed = 5

    def update(self):
        self.y-= self.speed

    def draw(self):
        t_n_p = pygame.image.load("thoughts_and_prayers_small.png")
        screen.blit(t_n_p, [self.x, self.y])

    
class Mob:

    def __init__(self):
        pass

    def update(self):
        pass


class Bomb:
    
    def __init__(self):
        pass

    def update(self):
        pass
    
    
class Fleet:

    def __init__(self):
        pass

    def update(self):
        pass

    
# Make game objects
player = Ship(384, 536)
lasers = []

# Game loop
done = False

while not done:
    # Event processing (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_LEFT]:
        player.move_left()
    elif pressed[pygame.K_RIGHT]:
        player.move_right()
        
    
    # Game logic (Check for collisions, update points, etc.)
    
    for l in lasers:
        l.update()
        
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.fill(BLACK)
    player.draw()
    for l in lasers:
        l.draw()


    
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
