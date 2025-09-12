import pygame, animate


class Bird(animate.Animate):
    def __init__(self, x, y, img, lastImg):
        super().__init__(x, y, img, lastImg)
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