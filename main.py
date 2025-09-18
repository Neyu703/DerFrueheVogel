#-------------------------------------------------------------------------------
# Name:        Der Frühe Vogel
# Purpose:     Spiel
#
# Author:      Stefan Güttler, Herbert Nguyen
#
# Created:     08.09.2025
# Copyright:   no copyright
# Licence:     no licence
#-------------------------------------------------------------------------------



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
levelUpTime = None
LEVEL_UP_DISPLAY_TIME = 2000 # milliseconds
bg = pygame.image.load("assets/levels/nature_"+str(level)+"/origbig.png").convert_alpha()
targetHeight = screenHeight
scale = targetHeight / bg.get_height()
targetWidth = bg.get_width() * scale
bg = pygame.transform.scale(bg, (targetWidth, targetHeight))
repeatImage = 3 #repeat background this many times (higher number = bigger level)
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
    #establish the safe zone, define randomX for two cases: birds that spawn to the left and ones that spawn to the right
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

font = pygame.font.SysFont("freesans",32)

birdKillCount = 0
ticks = 8
foodDeltaY = 0
foodDeltaX = 0
projectileSpeedFactor = 15

x = 0
scrolling = False
walkDirection = 0
scrollSpeed = 5
speedMult = 4
gameLost = False

def show_start_screen(screen, screenWidth, screenHeight):
    helpFont = pygame.font.SysFont("Arial", 48)
    smallHelpFont = pygame.font.SysFont("Arial", 32)
    title = helpFont.render("Der frühe Vogel", True, (0, 0, 0))
    controls = [
        "Steuerung:",
        "Pfeiltasten links/rechts - Bewegen",
        "Umschalt - Schneller bewegen",
        "Rechte Maustaste - Essen werfen",
        "",
        "Viel Glück!"
    ]
    control_texts = [smallHelpFont.render(line, True, (0, 0, 0)) for line in controls]
    start_time = pygame.time.get_ticks()
    while True:
        screen.blit(bg, (0, 0))
        # make a semitransparent surface for better text visibility
        overlay = pygame.Surface((screenWidth, screenHeight))
        overlay.set_alpha(200)  # Set transparency level (0-255)
        overlay.fill((255, 255, 255))  # Fill with white color
        screen.blit(overlay, (0, 0))
        screen.blit(title, (screenWidth // 2 - title.get_width() // 2, 100))
        for i, text in enumerate(control_texts):
            screen.blit(text, (screenWidth // 2 - text.get_width() // 2, 200 + i * 40))
        info = smallHelpFont.render("Beliebige Taste drücken, um das Spiel zu starten...", True, (100, 100, 100))
        screen.blit(info, (screenWidth // 2 - info.get_width() // 2, 450))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        if pygame.time.get_ticks() - start_time > 10000:
            return

show_start_screen(screen, screenWidth, screenHeight)
running = True
started = False

while running:
    clock.tick(ticks)

    collidedBirds2Worm = pygame.sprite.groupcollide(birdGroup, wormGroup, True, True)
    if collidedBirds2Worm:
        gameLost = True


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not gameLost:
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
                if not gameLost:
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
    if not gameLost:
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
    if collidedBirds2Food:
        birdKillCount += 1

    if not gameLost:
        score = font.render(f"score: {birdKillCount}", True, (0, 0, 0))
        screen.blit(score, (0, 0))
    if gameLost:
        screen.fill((0, 0, 0))
        lose1 = font.render("DU HAST VERLOREN", True, (255, 255, 255))
        lose2 = font.render(f"Dein Score ist {birdKillCount}", True, (255, 255, 255))
        screen.blit(lose1, ((screenWidth - lose1.get_width()) / 2, (screenHeight - lose1.get_height()) / 2))
        screen.blit(lose2, ((screenWidth - lose2.get_width()) / 2, (screenHeight - lose2.get_height()) / 2 + 30))


    if not gameLost:
        if random.random() < 0.05:
            if len(birdGroup) < numberOfBirds:
                spawnBirds()

    if not gameLost:
        wormGroup.draw(screen)
        birdGroup.draw(screen)
        foodGroup.draw(screen)

    len(birdGroup)
    if x >= levelWidth - screenWidth - 100:
        level += 1
        if level < 8:
            bg = pygame.image.load("assets/levels/nature_"+str(level)+"/origbig.png").convert_alpha()
            scale = targetHeight / bg.get_height()
            targetWidth = bg.get_width() * scale
            bg = pygame.transform.scale(bg, (targetWidth, targetHeight))
            levelWidth = bg.get_width() * repeatImage
            x = 0
            levelUpTime = pygame.time.get_ticks()
        else: # max level reached
            level = 7
            screen.fill((0,0,0))
            font = pygame.font.SysFont("Arial", 72)
            levelUpText = font.render(f"You win!", True, (255, 255, 255))
            screen.blit(levelUpText, (screenWidth / 2 - levelUpText.get_width() / 2, screenHeight / 2 - levelUpText.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(3000)
            running = False
    if levelUpTime and pygame.time.get_ticks() - levelUpTime < LEVEL_UP_DISPLAY_TIME:
        levelUpFont = pygame.font.SysFont("Arial", 72)
        levelUpText = levelUpFont.render(f"Level {level}", True, (255, 255, 255))
        screen.blit(levelUpText, (screenWidth / 2 - levelUpText.get_width() / 2, screenHeight / 2 - levelUpText.get_height() / 2))
    else:
        levelUpTime = None
    pygame.display.update()
pygame.quit()