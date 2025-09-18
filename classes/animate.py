import pygame

class Animate(pygame.sprite.Sprite):
    def __init__(self, initPosX, initPosY, img, spriteCount, spriteWidth, spriteHeight, spriteY = 0, flipHorzontally=False):
        super().__init__()
        self.flipHorzontally = flipHorzontally
        self.spriteY = spriteY
        self.fullImage = pygame.image.load(img).convert_alpha()
        self.images = []
        self.imagesFlipped = []
        self.setSpriteDimensions(spriteCount, spriteWidth, spriteHeight)

        self.imageIndex = 0
        self.image = self.images[self.imageIndex]
        self.base_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = (initPosX, initPosY)

    def setSpriteDimensions(self, spriteCount, spriteWidth, spriteHeight, spriteY = 0):
        for image in range(spriteCount):
            subsurface = self.fullImage.subsurface((image * spriteWidth, self.spriteY, spriteWidth, spriteHeight))

            scaled_subsurface = pygame.transform.scale2x(subsurface)

            if self.flipHorzontally:
                self.images.append(pygame.transform.flip(scaled_subsurface, False, self.flipHorzontally))
                self.imagesFlipped.append(pygame.transform.flip(scaled_subsurface, True, self.flipHorzontally))
            else:
                self.images.append(scaled_subsurface)
                self.imagesFlipped.append(pygame.transform.flip(scaled_subsurface, True, False))

    def update(self, direction = 1):
        if direction == 1:
            self.cycleSprite(self.images)
        elif direction == -1:
            self.cycleSprite(self.imagesFlipped)

    def rotate(self, angle):
        rotated_image = pygame.transform.rotate(self.base_image, angle)
        self.rect = rotated_image.get_rect(center=self.rect.center)
        return rotated_image

    def cycleSprite(self, images):
        self.base_image = images[self.imageIndex].copy()
        self.image = self.base_image
        self.imageIndex += 1
        if self.imageIndex >= len(images):
            self.imageIndex = 0

