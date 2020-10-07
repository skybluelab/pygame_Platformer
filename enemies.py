import pygame as pg
import math
from settings import *

vec = pg.math.Vector2

class Blade(pg.sprite.Sprite):
    def __init__(self, pos):
        pg.sprite.Sprite.__init__(self)

        self.pos = vec(pos[0], pos[1])
        self.angle = 0
        self.image = pg.image.load("Sprites/Enemies/Grinder.png")
        self.rect = self.image.get_rect()
        self.image = pg.transform.scale(self.image, (int(self.rect.width*0.125), int(self.rect.height*0.125)))
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (self.pos.x, self.pos.y)

        self.show = True
        self.activate = True

    def update(self):
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.pos.x, self.pos.y)

        self.angle += 3
        if self.angle >= 360:
            self.angle = 0


class Thorn(pg.sprite.Sprite):
    def __init__(self , pos):
        pg.sprite.Sprite.__init__(self)

        self.pos = vec(pos[0],pos[1])
        self.angle = 0
        self.image = pg.image.load("Sprites/Enemies/Spike_Up.png")  #바꿀 예정(임시)
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (self.pos.x, self.pos.y)

        self.show = True
        self.activate = True

    def update(self):
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.pos.x, self.pos.y)



class Laser(pg.sprite.Sprite):
    def __init__(self, pos, angle, t):
        pg.sprite.Sprite.__init__(self)

        self.pos = vec(pos[0], pos[1])
        self.angle = angle
        self.image = pg.image.load("Sprites/Enemies/Laser.png")
        self.original_image = self.image
        self.rect = self.image.get_rect()
        if angle == 90:
            self.image = pg.transform.scale(self.image, (int(HEIGHT*1.25), int(self.rect.height * 0.125)))
        else:
            self.image = pg.transform.scale(self.image, (int(abs(HEIGHT/math.sin(math.radians(angle)))*1.25), int(self.rect.height * 0.125)))
        self.track_image = pg.transform.rotate(pg.transform.scale(self.image, (WIDTH, 4)), self.angle)
        self.image = pg.transform.rotate(self.image, angle)
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.original_rect = self.rect
        self.track_rect = self.track_image.get_rect()
        self.rect.center = (self.pos.x, self.pos.y)
        self.original_rect.center = (self.pos.x, self.pos.y)
        self.track_rect.center = (self.pos.x, self.pos.y)

        self.t = t
        self.show = False
        self.activate = False

    def update(self):
        self.t += 1
        if self.t >= 240:
            self.show = False
            self.activate = False
            self.t = 0
        elif self.t >= 180:
            self.show = True
            self.activate = True
            self.image = self.original_image
            self.rect = self.original_rect
        elif self.t >= 120:
            self.show = True
            self.activate = False
            self.image = self.track_image
            self.rect = self.track_rect

