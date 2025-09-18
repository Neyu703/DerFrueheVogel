import math

import pygame
from .animate import Animate


class Bird(Animate):
    def __init__(self, initPosX, initPosY, img, spriteCount, spriteWidth, spriteHeight,flipHorzontally, spriteY = 0):
        super().__init__(initPosX, initPosY, img, spriteCount, spriteWidth, spriteHeight, spriteY, flipHorzontally)
        self.current_angle = 0
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

    def look_at_point(self, target_x, target_y, direction = 1):
        #https://stackoverflow.com/questions/58603835/how-to-rotate-an-imageplayer-to-the-mouse-direction
        dx = self.rect.centerx - target_x
        dy = self.rect.centery - target_y

        angle_rad = math.atan2(dy, -dx)
        angle_deg = math.degrees(angle_rad)

        #sprite looking left, so corrextion angle ist 180
        correctionAngle = 180

        if direction == 1:
            angle_deg += correctionAngle
        elif direction == -1:
            angle_deg -= correctionAngle

        self.image = self.rotate(angle_deg)
        self.current_angle = angle_deg
