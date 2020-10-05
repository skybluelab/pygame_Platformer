import pygame as pg
import random
from settings import *
vec = pg.math.Vector2

class particle_deathPop(pg.sprite.Sprite):
    def __init__(self, player):
        pg.sprite.Sprite.__init__(self)
        self.player = player
        self.pos = vec(player.pos.x+random.randrange(-10, 11), player.pos.y+random.randrange(-10, 11))
        self.vel = vec(player.vel.x*0.5+random.randrange(-7, 8), player.vel.y*0.5+random.randrange(-12, 4))
        self.acc = vec(0, PLAYER_GRAVITY*0.8)
        self.time = 100
        self.image = pg.image.load("Sprites/Player/Body.png")
        k = random.randrange(10, 20)*0.01
        self.image = pg.transform.scale(self.image, (int(self.image.get_rect().width*k), int(self.image.get_rect().height*k)))
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (self.pos.x, self.pos.y)
        self.show = True

    def update(self):
        if self.time > 0:
            self.vel += self.acc
            self.pos += self.vel + 0.5*self.acc
            self.rect.center = (self.pos.x, self.pos.y)
            self.time -= 1
        else:
            self.show = False