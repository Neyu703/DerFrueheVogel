import math

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

def calcDelta(posX, posY, targetX, targetY):

    deltaX = targetX - posX
    deltaY = targetY - posY

    distance = math.sqrt(deltaX ** 2 + deltaY ** 2)

    stepX = deltaX / distance
    stepY = deltaY / distance

    if targetX < posX:
        stepX = abs(stepX) * -1
    if targetX > posX:
        stepX = abs(stepX)
    if targetY < posY:
        stepY = abs(stepY) * -1
    if targetY > posY:
        stepY = abs(stepY)


    print(f"stepX = {stepX} stepY = {stepY}")
    print("------------------")

    return stepX, stepY


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
foodWidth   = 32 # pixel width
foodHeight  = 32 # pixel height
foodGroup = pygame.sprite.Group()
foodScaleFactor = 1 # size scale
maxFood = 3


wormColor = 16
wormImg = f"8Bit-Worm-var{wormColor}-byImogiaGames.png"
wormSpritePath = f"assets/8Bit-Worm/{wormImg}"
wormWidth = 16
wormHeight = 6
wormPosX = screenWidth / 2
wormPosY = screenHeight -100
wormScaleFactor = 5
worm = Worm(wormPosX, wormPosY, wormSpritePath, 4, wormWidth, wormHeight, 9, scaleFactor = wormScaleFactor)
wormGroup = pygame.sprite.Group()
wormGroup.add(worm)

birdSpritePath = "assets/Bird16x16/BirdSprite.png"
birdGroup = pygame.sprite.Group()
numberOfBirds = 5
birdHeight = 16
birdWidth = 16
birdScaleFactor = 3
birdSpeedFactor = 1
safeZone = 50 # birds have to spawn this many pixels away from the worm (they shan't kiss the worm on spawn that would be silly)

def spawnBirds():
    #establish the safe zone, define randomX for for two cases: birds that spawn to the left and ones that spawn to the right
    if random.choice([True, False]):
        randomX = random.randint(0, int(wormPosX - safeZone - birdWidth)) #birds that spawn to the left of the worm
    else:
        randomX = random.randint(int(wormPosX + safeZone + birdWidth), screenWidth - birdWidth) #birds that spawn to the right of the worm
    randomY = random.randint(0, (wormPosY - 50) - birdHeight)
    if randomX < screenWidth / 2:
        flipHorzontally = True
    else:
        flipHorzontally = False
    bird = Bird(randomX, randomY, birdSpritePath, 7, birdWidth, birdHeight, flipHorzontally, 17, scaleFactor= birdScaleFactor)
    birdGroup.add(bird)
    birdDeltaX, birdDeltaY = calcDelta(randomX, randomY, wormPosX, wormPosY)
    birdDeltaX = birdDeltaX * birdSpeedFactor
    birdDeltaY = birdDeltaY * birdSpeedFactor

    bird.speedX = birdDeltaX
    bird.speedY = birdDeltaY
for _ in range(numberOfBirds):
    spawnBirds()



ticks = 8
foodDeltaY = 0
foodDeltaX = 0
projectileSpeedFactor = 15

x = 0
scrolling = False
walkDirection = 0
scrollSpeed = 5
speedMult = 4
running = True
while running:
    clock.tick(ticks)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                scrolling = True
                walkDirection = 1
            if event.key == pygame.K_LEFT:
                scrolling = True
                walkDirection = -1
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                scrollSpeed = scrollSpeed * speedMult
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                scrolling = False
                walkDirection = 0
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                scrollSpeed = scrollSpeed / speedMult
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouseX, mouseY = pygame.mouse.get_pos()
                if len(foodGroup) < maxFood:
                    food = Food(wormPosX, wormPosY, foodSpritePath, 1, foodWidth, foodHeight, scaleFactor = foodScaleFactor)
                    foodGroup.add(food)

                    foodDeltaX, foodDeltaY = calcDelta(wormPosX, wormPosY, mouseX, mouseY)
                    foodDeltaX = foodDeltaX * projectileSpeedFactor
                    foodDeltaY = foodDeltaY * projectileSpeedFactor

                    food.speedX = foodDeltaX
                    food.speedY = foodDeltaY
    if scrolling:
        x += scrollSpeed*walkDirection
        maxOffset = levelWidth - screenWidth
        if x >= maxOffset:
            x = maxOffset
        if x <= 0:
            x = 0


    for i in range(repeatImage):
        screen.blit(bg, (i*bg.get_width()-x,0))

    wormGroup.update(walkDirection)

    for bird in birdGroup:
        if bird.rect.centerx < screenWidth / 2:
            direction = 1
        else:
            direction = -1
        bird.update(1)
        bird.look_at_point(worm.rect.centerx, worm.rect.centery, direction)
        bird.move()

    for food in foodGroup:
        food.update(1)
        food.rotate(360/ticks)
        food.move()
        if food.rect.right < 0 or food.rect.left > screenWidth or food.rect.bottom < 0 or food.rect.top > screenHeight:
            food.kill()


    collidedBirds2Food = pygame.sprite.groupcollide(birdGroup, foodGroup, True, True)

    collidedBirds2Worm = pygame.sprite.groupcollide(birdGroup, wormGroup, True, True)


    if random.random() < 0.05:
        # TODO set max number of birds that are allowed to spawn
        spawnBirds()

    wormGroup.draw(screen)
    birdGroup.draw(screen)
    foodGroup.draw(screen)

    len(birdGroup)
    pygame.display.update()
pygame.quit()