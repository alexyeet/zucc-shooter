# imports
import pygame
import random
from random import randint

# initialize game engine
pygame.init()


# window
WIDTH = 1200
HEIGHT = 650
SIZE = (WIDTH, HEIGHT)
TITLE = "zucc vs congress"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)


# timer
clock = pygame.time.Clock()
refresh_rate = 60


# colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (100, 255, 100)

# zuccs
zucc1 = pygame.image.load("zucc1.png")
zucc2 = pygame.image.load("zucc2.png")
zucc3 = pygame.image.load("zucc3.png")
zucc4 = pygame.image.load("zucc4.png")
zucc5 = pygame.image.load("zucc5.png")

zuccs = [zucc1, zucc2, zucc3, zucc4, zucc5]

# images

bomb_img = pygame.image.load('thoughts_and_prayers_small.png')
mob_img = random.choice(zuccs)
laser_img = pygame.image.load('water.png')
splash = pygame.image.load('splash_screen.png')
end_screen = pygame.image.load('end_screen.png')
background = pygame.image.load('courtroom.png')
ship_img1 = pygame.image.load('congress.png')
ship_img2 = pygame.image.load('congress_fire.png')
ship_images = [ship_img1, ship_img2]
ufo_img = pygame.image.load('trump.png')

#stages
START = 0
PLAYING = 1
END = 2

# fonts
FONT_SM = pygame.font.Font(None, 24)
FONT_MD = pygame.font.Font(None, 32)
FONT_LG = pygame.font.Font(None, 64)
FONT_XL = pygame.font.Font("fonts/spacepunk_PG.ttf", 70)

# sounds
pygame.mixer.music.load("background_music.ogg")
pygame.mixer.music.play(-1)
explosion = pygame.mixer.Sound("explosion.ogg")
hit = pygame.mixer.Sound("hit.ogg")


#helper functions
def show_splash_screen():
    screen.blit(splash, [0, 0])

def show_stats(player):
    score_text = FONT_XL.render('score = ' + str(player.score), 1, WHITE)
    screen.blit(score_text, [32, 32])
    shield_text = FONT_XL.render('shield: ' + str(ship.shield), 1, WHITE)
    screen.blit(shield_text, [32, 100])

def show_end_screen(player):
    screen.blit(end_screen, [0, 0])
    end_score = FONT_XL.render('final score = ' + str(player.score), 1, WHITE)
    text_rect = end_score.get_rect(center = (WIDTH/2, HEIGHT/2 + 275))
    screen.blit(end_score, text_rect)

def show_win():
    pass

# game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, ship_images):
        super().__init__()

        self.image = ship_img1
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.speed = 3
        self.shield = 3
        self.score = 0

    def move_left(self):
        self.rect.x -= self.speed
        if self.rect.right <= -1:
            self.rect.left = WIDTH
        
    def move_right(self):
        self.rect.x += self.speed
        if self.rect.left >= 1201:
            self.rect.right = 0

    def shoot(self):
        laser = Laser(laser_img)
        laser.rect.centerx = self.rect.centerx
        laser.rect.centery = self.rect.top
        lasers.add(laser)

    def update(self, bombs, mobs, ufos):
        hit_list = pygame.sprite.spritecollide(self, bombs, True, \
                                               pygame.sprite.collide_mask)
        mobs_hit = pygame.sprite.spritecollide(self, mobs, False)      

        if self.shield <= 1:
            self.image = ship_images[1]

        for hit in hit_list:
            hit.play()
            self.shield -= 1

        for hit in mobs_hit:
            explosion.play()
            self.kill()

        if self.shield == 0:
            explosion.play()
            self.kill()
            
    
class Laser(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        
        self.speed = 5

    def update(self):
        self.rect.y -= self.speed
    
class Mob(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.SS = randint(1, 3)
        self.shield = self.SS

    def drop_bomb(self):
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)

    def update(self, lasers, player):
        hit_list = pygame.sprite.spritecollide(self, lasers, True, \
                                               pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            self.shield -= 1
            hit.play()

        if self.shield == 0:
            self.kill()
            player.score += (self.SS * 5)
            explosion.play()



class Bomb(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        
        self.speed = 3
        
    def update(self):
        self.rect.y += self.speed
    
    
class Fleet:

    def __init__(self, mobs):
        super().__init__()

        self.mobs = mobs
        self.moving_right = True
        self.speed = 5
        self.bomb_rate = 60

    
    def move(self):
        reverse = False
        
        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed
                if m.rect.right >= WIDTH:
                    reverse = True
            else:
                m.rect.x -= self.speed
                if m.rect.left <=0:
                    reverse = True
                    
        if reverse == True:
            self.moving_right = not self.moving_right
            for m in mobs:
                m.rect.y += 32
    

    def choose_bomber(self):
        rand = random.randrange(0, self.bomb_rate)
        all_mobs = mobs.sprites()
        
        if len(all_mobs) > 0 and rand == 0:
            return random.choice(all_mobs)
        else:
            return None


    def update(self):
        self.move()

        bomber = self.choose_bomber()
        if bomber != None:
            bomber.drop_bomb()


class UFO(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 6

    def move(self):
        #self.rect.x = randint(-10000, -1000)
        self.rect.x += self.speed

    def update(self, lasers):
        hit_list = pygame.sprite.spritecollide(self, lasers, True, \
                                       pygame.sprite.collide_mask)

        if len(hit_list) >= 1:
            self.kill()
            player.score += 30

        self.move()

    
# make game objects
ship = Ship(384, 536, ship_images)

mob1 = Mob(128, 64, random.choice(zuccs))
mob2 = Mob(256, 64, random.choice(zuccs))
mob3 = Mob(384, 64, random.choice(zuccs))
mob4 = Mob(512, 64, random.choice(zuccs))
mob5 = Mob(640, 64, random.choice(zuccs))
mob6 = Mob(768, 64, random.choice(zuccs))
mob7 = Mob(896, 64, random.choice(zuccs))

mob8 = Mob(320, -100, random.choice(zuccs))
mob9 = Mob(448, -100, random.choice(zuccs))
mob10 = Mob(576, -100, random.choice(zuccs))
mob11 = Mob(704, -100, random.choice(zuccs))

ufo = UFO(randint(-5000, -1000), 50, ufo_img)

# make sprite groups
player = pygame.sprite.GroupSingle()
player.add(ship)
player.score = 0
player.shield = ship.shield

lasers = pygame.sprite.Group()

mobs = pygame.sprite.Group()
mobs.add(mob8, mob9, mob10, mob11, mob1, mob2, mob3, mob4, mob5, mob6, mob7)
if len(mobs) == 0:
    stage = END

fleet = Fleet(mobs)

bombs = pygame.sprite.Group()

ufos = pygame.sprite.GroupSingle()
ufos.add(ufo)


# game loop
done = False
stage = START
win = False

while not done:
    # event processing 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if stage == START or stage == END:
                if event.key == pygame.K_SPACE:
                    stage = PLAYING
            elif stage == PLAYING:
                if event.key == pygame.K_SPACE:
                    ship.shoot()

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_LEFT]:
        ship.move_left()
    elif pressed[pygame.K_RIGHT]:
        ship.move_right()
        
    
    # game logic
    if stage == PLAYING:
        player.update(bombs, mobs, ufos)
        lasers.update()
        mobs.update(lasers, player)
        bombs.update()
        fleet.update()
        ufos.update(lasers)

        if len(player) == 0:
            stage = END
            win = False

        elif len(mobs) == 0:
            stage = END
            win = True
        
        
        # drawing code
        screen.blit(background, [0, 0])
        lasers.draw(screen)
        player.draw(screen)
        mobs.draw(screen)
        bombs.draw(screen)
        ufos.draw(screen)
        show_stats(player)

    if stage == START:
        show_splash_screen()

    if stage == END:
        show_end_screen(player)

    
    # update screen 
    pygame.display.flip()


    # limit refresh rate of game loop 
    clock.tick(refresh_rate)


# close window and quit
pygame.quit()
