import pygame
from .animate import Animate


class Food(Animate):
    def __init__(self, initPosX, initPosY, img, spriteCount, spriteWidth, spriteHeight, spriteY = 0):
        super().__init__(initPosX, initPosY, img, spriteCount, spriteWidth, spriteHeight, spriteY)
        self.calc_x = self.rect.x
        self.SINGLESTEP_X = 5
        self.rotation_angle = 0
        self.original_image = self.image

    def rotate(self, degrees):
        self.rotation_angle += degrees
        if self.rotation_angle >= 360:
            self.rotation_angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.rotation_angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update_position(self):
        self.calc_x += (self.direction * self.SINGLESTEP_X)
        if self.calc_x < 0:
            self.calc_x = 0

        if self.calc_x > 800 - self.rect.width:
            self.calc_x = 800 - self.rect.width

        self.rect.x = round(self.calc_x)

    def walk(self, direction):
        self.direction = direction