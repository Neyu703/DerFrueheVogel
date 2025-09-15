import pygame

class Animate(pygame.sprite.Sprite):
    def __init__(self, initPosX, initPosY, img, spriteCount, spriteWidth, spriteHeight, spriteY = 0):
        super().__init__()
        self.spriteY = spriteY
        self.fullImage = pygame.image.load(img).convert_alpha()
        self.images = []
        self.imagesFlipped = []
        self.setSpriteDimensions(spriteCount, spriteWidth, spriteHeight)

        self.imageIndex = 0
        self.image = self.images[self.imageIndex]
        self.rect = self.image.get_rect()
        self.rect.topleft = (initPosX, initPosY)

    def setSpriteDimensions(self, spriteCount, spriteWidth, spriteHeight, spriteY = 0):
        for image in range(spriteCount):
            subsurface = self.fullImage.subsurface((image * spriteWidth, self.spriteY, spriteWidth, spriteHeight))
            subsurface = pygame.transform.scale2x(subsurface)
            self.images.append(pygame.transform.scale2x(subsurface))
            self.imagesFlipped.append(pygame.transform.flip(subsurface, True, False))

    def update(self, direction):
        if direction == 1:
            self.cycleSprite(self.images)
        elif direction == -1:
            self.cycleSprite(self.imagesFlipped)

    def cycleSprite(self, images):
        self.image = images[self.imageIndex]
        self.imageIndex += 1
        if self.imageIndex >= len(images):
            self.imageIndex = 0

