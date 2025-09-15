import pygame
from classes.bird import Bird
from classes.worm import Worm

pygame.init()

clock = pygame.time.Clock()

screenHeight = 600
screenWidth = 800

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Der frühe Vogel")

wormColor = 16
wormImg = f"8Bit-Worm-var{wormColor}-byImogiaGames.png"

birdSpritePath = "assets/Bird16x16/BirdSprite.png"
wormSpritePath = f"assets/8Bit-Worm/{wormImg}"

bird = Bird(100, 100, birdSpritePath, 7, 16, 16, 20)
birdGroup = pygame.sprite.Group()
birdGroup.add(bird)

worm = Worm(200, 100, wormSpritePath, 4, 16, 6, 9)
wormGroup = pygame.sprite.Group()
wormGroup.add(worm)


running = True
while running:
    clock.tick(8)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    birdGroup.update(1)
    birdGroup.draw(screen)

    wormGroup.update(1)
    wormGroup.draw(screen)



    pygame.display.update()
pygame.quit()