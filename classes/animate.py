import pygame


class Animate(pygame.sprite.Sprite):
    def __init__(self, posX, posY, img, lastImg):
        super().__init__()
        self.animated = True
        self.fullImage = pygame.image.load(img).convert_alpha()

        self.images = []
        self.imagesLeft = []
        for image in range(lastImg):
            subsurface = self.fullImage.subsurface((image * 32, 0, 32, 32))
            self.images.append(pygame.transform.scale2x(subsurface))
            self.imagesLeft.append(pygame.transform.flip(subsurface, True, False))

        self.imageIndex = 0
        self.image = self.images[self.imageIndex]
        self.rect = self.image.get_rect()
        self.rect.topleft = (posX, posY)
        self.direction = 0

    def update(self):
        self.update_position()
        if self.animated:
            self.update_image(self.direction)

    def update_image(self, direction):
        if direction == 1:
            self.image = self.images[self.imageIndex]
        elif direction == -1:
            self.image = self.imagesLeft[self.imageIndex]
        self.imageIndex += 1
        if self.imageIndex >= len(self.images):
            self.imageIndex = 0