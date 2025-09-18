import pygame
import random
from classes.bird import Bird
from classes.worm import Worm
from classes.food import Food

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

foodNumber = 43
foodImg = f"colourwheel_{foodNumber}.png"
foodSpritePath = f"assets/Food Icons/{foodImg}"
foodWidth = 32
foodHeight = 32
food = Food(100, 100, foodSpritePath, 1, foodWidth, foodHeight)
foodGroup = pygame.sprite.Group()
foodGroup.add(food)


birdSpritePath = "assets/Bird16x16/BirdSprite.png"
birdGroup = pygame.sprite.Group()
numberOfBirds = 5
birdHeight = 16
birdWidth = 16
for _ in range(numberOfBirds):
    randomX = random.randint(0, screenWidth - birdWidth)
    randomY = random.randint(0, screenHeight - birdHeight)
    if randomX < screenWidth / 2:
        flipHorzontally = True
    else:
        flipHorzontally = False
    bird = Bird(randomX, randomY, birdSpritePath, 7, birdWidth, birdHeight, flipHorzontally, 17)
    birdGroup.add(bird)


wormColor = 16
wormImg = f"8Bit-Worm-var{wormColor}-byImogiaGames.png"
wormSpritePath = f"assets/8Bit-Worm/{wormImg}"
wormWidth = 16
wormHeight = 6
wormPosX = screenWidth / 2
wormPosY = screenHeight -100
worm = Worm(wormPosX, wormPosY, wormSpritePath, 4, wormWidth, wormHeight, 9)
wormGroup = pygame.sprite.Group()
wormGroup.add(worm)

def calcDelta(posX, posY, targetX, targetY, inf = True):

    deltaX = targetX - posX
    deltaY = targetY - posY

    if inf:
        if deltaX > 0:
            deltaX = 1
        else:
            deltaX = -1
        if deltaY > 0:
            deltaY = 1
        else:
            deltaY = -1

    return deltaX, deltaY

    print(f"deltaX: {deltaX}, deltaY: {deltaY}")
    print("------------------")

ticks = 8

running = True
while running:
    clock.tick(ticks)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouseX, mouseY = pygame.mouse.get_pos()
                calcDelta(wormPosX, wormPosY, mouseX, mouseY, True)

    
    for i in range(repeatImage):
        screen.blit(bg, (i*bg.get_width(),0))


    wormGroup.update(1)

    for bird in birdGroup:
        if bird.rect.centerx < screenWidth / 2:
            direction = 1
        else:
            direction = -1
        bird.update(1)
        bird.look_at_point(worm.rect.centerx, worm.rect.centery, direction)

    for food in foodGroup:
        food.update(1)
        food.rotate(360/ticks)

    wormGroup.draw(screen)
    birdGroup.draw(screen)
    foodGroup.draw(screen)


    pygame.display.update()
pygame.quit()