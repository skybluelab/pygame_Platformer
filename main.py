import pygame as pg
import random
from settings import *
from sprites import *
from enemies import *
from particles import *

class Game:
    def __init__(self):
        # initialize game wiindow, etc
        pg.init()
        pg.mixer.init(buffer=16)
        pg.mixer.quit()
        pg.mixer.init(buffer=16)    # 효과음 지연 오류 때문에 다시 불러옴

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

        # user events
        self.DEAD = pg.USEREVENT

        # sounds
        self.death_sound = pg.mixer.Sound("Audio/die.wav")

    def new(self):
        global playerSimulation

        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.enemies = pg.sprite.Group()

        self.player = Player(self)
        self.all_sprites.add(self.player)

        self.all_sprites.add(playerSimulation)
        playerSimulation.time = 1
        playerSimulation.play = True

        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)

        self.all_sprites.add(*ENEMY_LIST)
        self.enemies.add(*ENEMY_LIST)

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

        # check if player hits enemy
        hits_enemy = pg.sprite.spritecollide(self.player, list(filter(lambda e: e.activate, self.enemies)), False,
                                             pg.sprite.collide_mask)
        if hits_enemy:
            for n in range(0, 30):
                self.all_sprites.add(particle_deathPop(self.player))
            pg.mixer.Sound.play(self.death_sound)
            self.all_sprites.remove(self.player)
            self.enemies = []
            pg.time.set_timer(self.DEAD, 1200)



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
            if event.type == self.DEAD:
                self.playing = False
                pg.time.set_timer(self.DEAD, 0)

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BACKGROUND_COLOR)
        pg.sprite.Group(list(filter(lambda e: e.show, self.all_sprites))).draw(self.screen)
        pg.display.flip()

g = Game()

playerSimulation = PlayerSimulation((20, HEIGHT - 100), pg.rect.Rect(20, HEIGHT - 100, 32, 32))
enemyGenerator = EnemyGenerator(playerSimulation)

while g.running:
    playerSimulation.updateMotionScript(
        {0: ((0, PLAYER_GRAVITY), (0, 0)),
         10.7: ((0, 0), (0, 'break')),
         11: ((0, 0), (PLAYER_VEL, 0)),
         120: ((0, 0), ('break', 0)),
         130: ((0, PLAYER_GRAVITY), (PLAYER_VEL, -PLAYER_JUMPPOWER)),
         167.5: ((0, 0), (-PLAYER_VEL, 'break')),
         200: ((0, 0), (PLAYER_VEL, 0)),
         380: ((0, 0), ('break', 'break'))})
    #test enemy
    enemyGenerator.generate_Laser((WIDTH / 2 - 30, HEIGHT / 2), 72)
    enemyGenerator.enemies["Blade"].append([(300, 500)])
    ENEMY_LIST = enemyGenerator.set_all()

    g.new()

pg.quit()
