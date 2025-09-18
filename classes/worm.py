import pygame
from .animate import Animate


class Worm(Animate):
    def __init__(self, initPosX, initPosY, img, spriteCount, spriteWidth, spriteHeight, spriteY = 0, scaleFactor = 1):
        super().__init__(initPosX, initPosY, img, spriteCount, spriteWidth, spriteHeight, spriteY,False, scaleFactor)
        self.calc_x = self.rect.x
        self.SINGLESTEP_X = 5

    def update_position(self):
        self.calc_x += (self.direction * self.SINGLESTEP_X)
        if self.calc_x < 0:
            self.calc_x = 0

        if self.calc_x > 800 - self.rect.width:
            self.calc_x = 800 - self.rect.width

        self.rect.x = round(self.calc_x)

    def walk(self, direction):
        self.direction = direction


    #( 0, 20) - (15,31)
    #(16, 21) - (31,31)