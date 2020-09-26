import pygame as pg
import random
from settings import *
from sprites import *

class Game:
    def __init__(self):
        # initialize game wiindow, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()

        self.platforms = pg.sprite.Group()

        self.player = Player(self)
        self.all_sprites.add(self.player)

        self.playerSimulation = PlayerSimulation(self.player)
        self.all_sprites.add(self.playerSimulation)
        self.playerSimulation.updateMotionScript(
                                {0: ((0, PLAYER_GRAVITY), (0, 0)),
                                 10.7: ((0, 0), (0, 'break')),
                                 11: ((PLAYER_ACC, 0), (0, 0)),
                                 120: ((0, 0), (0, 0)),
                                 130: ((PLAYER_ACC, PLAYER_GRAVITY), (0, -PLAYER_JUMPPOWER)),
                                 167.5: ((-PLAYER_ACC, 0), (0, 'break')),
                                 200: ((PLAYER_ACC, 0), (0, 0)),
                                 382: ((0, 0), (0, 0))})
        self.playerSimulation.time = 0
        self.playerSimulation.play = True

        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        #Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        #Game Loop - Update
        self.all_sprites.update()
        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                for hit in hits:
                    if self.player.rect.bottom < hit.rect.bottom:
                        self.player.pos.y = hit.rect.top - self.player.rect.height*0.5
                        self.player.rect.center = self.player.pos
                        self.player.vel.y = 0
        """
        # if player reaches top 1/4 of the screen
        if self.player.rect.top <= HEIGHT/4:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
        # if player reaches top 3/4 of the screen
        if self.player.rect.bottom >= HEIGHT*3/4:
            self.player.pos.y -= abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y -= abs(self.player.vel.y)
        """



    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                pass

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BACKGROUND_COLOR)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

g = Game()
while g.running:
    g.new()

pg.quit()
