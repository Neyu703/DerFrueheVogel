import pygame
import random
from classes.bird import Bird
from classes.worm import Worm

pygame.init()

clock = pygame.time.Clock()

screenHeight = 600
screenWidth = 800

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Der frühe Vogel")

# start at level 1, needs to be increased at some point to load the other background images
level = 1
bg = pygame.image.load("assets/levels/nature_"+str(level)+"/origbig.png").convert_alpha()
targetHeight = screenHeight
scale = targetHeight / bg.get_height()
targetWidth = bg.get_width() * scale
bg = pygame.transform.scale(bg, (targetWidth, targetHeight))
repeatImage = 7 #repeat background this many times (higher number = bigger level)
levelWidth = bg.get_width() * repeatImage #need this later to determine when to stop sidescrolling

wormColor = 16
wormImg = f"8Bit-Worm-var{wormColor}-byImogiaGames.png"


birdSpritePath = "assets/Bird16x16/BirdSprite.png"
birdGroup = pygame.sprite.Group()

numberOfBirds = 5
birdHeight = 16
birdWidth = 16

for _ in range(numberOfBirds):
    randomX = random.randint(0, screenWidth - birdWidth)
    randomY = random.randint(0, screenHeight - birdHeight)
    bird = Bird(randomX, randomY, birdSpritePath, 7, birdWidth, birdHeight, 17)
    birdGroup.add(bird)


wormSpritePath = f"assets/8Bit-Worm/{wormImg}"
wormWidth = 16
wormHeight = 6
worm = Worm(screenWidth/2 - 50, screenHeight-100, wormSpritePath, 4, wormWidth, wormHeight, 9)
wormGroup = pygame.sprite.Group()
wormGroup.add(worm)


running = True
while running:
    clock.tick(8)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    for i in range(repeatImage):
        screen.blit(bg, (i*bg.get_width(),0))

    birdGroup.update(1)
    birdGroup.draw(screen)

    wormGroup.update(1)
    wormGroup.draw(screen)



    pygame.display.update()
pygame.quit()