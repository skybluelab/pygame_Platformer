#Sprite classes for platform game
import pygame as pg
from sympy import *
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.pos = vec(20, HEIGHT - 100)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.image = pg.image.load("Sprites/Player/Body.png")
        self.image.blit(pg.image.load("Sprites/Player/Eye.png"),
                        (int(self.image.get_rect().width*0.3), int(self.image.get_rect().height*0.3)))
        self.image.blit(pg.image.load("Sprites/Player/Eye.png"),
                        (int(self.image.get_rect().width * 0.75), int(self.image.get_rect().height * 0.3)))
        self.image = pg.transform.scale(self.image, (int(self.image.get_rect().width*0.5), int(self.image.get_rect().height*0.5)))
        self.original_image = self.image
        #self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (self.pos.x, self.pos.y)
        self.show = True

        # sounds
        self.jump_sound = pg.mixer.Sound("Audio/jump.wav")

    def update(self):
        self.acc = vec(0, PLAYER_GRAVITY)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
            self.image = pg.transform.flip(self.original_image, True, False)
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
            self.image = self.original_image
        if keys[pg.K_SPACE] or keys[pg.K_UP]:
            self.jump()

        # apply x-direction friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel - 0.5 * self.acc #-0.5*self.acc가 맞다. pos_t = 값을 더한 횟수에 맞게 하려면.
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.center = self.pos

    def jump(self):
        # jump only if standing on platform
        if self.vel.y >= 0:
            self.rect.y += 1
            hits = pg.sprite.spritecollide(self, self.game.platforms, False)
            self.rect.y -= 1
            if hits:
                self.vel.y = -PLAYER_JUMPPOWER
                pg.mixer.Sound.play(self.jump_sound)

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.tile_image = pg.image.load("Sprites/Ground/GrassMid.png")
        self.tile_rect = self.tile_image.get_rect()
        self.tile_image = pg.transform.scale(self.tile_image, (int(self.tile_image.get_rect().width*0.25), int(self.tile_image.get_rect().height*0.25)))
        self.tile_rect = self.tile_image.get_rect()

        for x in range(0, self.rect.width, self.tile_rect.width):
            self.image.blit(self.tile_image, (x, 0))

        self.show = True

# 플레이어의 움직임을 식으로 변환해 저장할 수 있게 도와주고, 저장한 움직임을 시각적으로 볼 수 있게 해준다.
class PlayerSimulation(pg.sprite.Sprite):
    # 초기화할 때 플레이어 클래스를 전달해야 한다(모양, 초기 좌표를 같게 하기 위해).
    def __init__(self, player):
        pg.sprite.Sprite.__init__(self)
        self.player_pos = player.pos
        self.pos = player.pos
        self.original_image = player.image.copy()
        self.original_image.fill(BLUE)
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (self.pos.x, self.pos.y)
        self.show = True

        # 움직임을 보여줄 때의 변수 (self.time: 시간, self.play: 재생 여부)
        self.time = 1
        self.play = False

        self.t = Symbol('t')
        # 모션(motion)의 형식: (가속도 튜플, 속도 튜플).
        # 가속도는 다음 모션이 발동할 시간이 되기 전까지 계속 가해지고, 속도는 발동 시간에 한번 더해진다.
        # (바닥에 부딫히는 등)정지하고 싶다면, 'break'를 입력한다.  (예시: 바닥에 떨어져 y축 움직임을 0으로 만들고싶다면 속도 튜플을 (0, 'bkeak')로 한다.)
        self.time_list = []
        self.motion_list = []
        self.posFunc_list = []
        self.velFunc_list = []

    # main에서 all_sprites에 추가해 같이 update시키면 입력한 스크림트대로 이동하는 것을 볼 수 있다. self.time을 수정해서 시간을 정할 수 있다.
    def update(self):
        if self.play:
            self.image = self.original_image
            self.pos = self.get_position(self.time)
            self.rect.center = self.pos

            self.time += 1
        else:
            self.image = pg.Surface((0, 0))

    # 모션을 {시간: 모션} 형태의 딕셔너리로 전달하면 각 시간에 각 모션을 발동하도록 정보를 업데이트 해준다.
    def updateMotionScript(self, new_motionScript):
        new_time_list = sorted(list(new_motionScript.keys()))
        delete_list = []
        for time in self.time_list:
            if not time in new_time_list:
                delete_list.append(time)
        for n in delete_list:
            self.deleteTime(n)

        for new_time in new_time_list:
            new_motion = new_motionScript[new_time]
            if new_time in self.time_list:
                index = self.get_index(new_time)
                motion = self.motion_list[index]
                if motion != new_motion:
                    self.deleteTime(new_time)
                    self.addMotion(new_time, new_motion)
            else:
                self.addMotion(new_time, new_motion)

    # addMotion은 위치함수, 속도함수를 생성하여 저장한다. 이미 time에 해당하는 값이 있으면 교체한다(오류가 생길 수 있음. 따라서 가능하면 입력했던 최대 time값보다 작은 값을 대입하지 말것).
    def addMotion(self, time, motion):
        # time에 해당하는 좌표
        pos = self.get_position(time)

        # motion에서 가속도를 가져온다.
        acc = vec(*motion[0])

        vel = vec(0, 0)
        # motion의 속도값이 'break'라면 속도를 0, 속도함수를 가속도에만 영향을 받도록 정한다.
        # 아니라면 속도를 time에 해당하는 속도 + motion의 속도로, 속도함수를 속도도 고려하여 정한다.
        if motion[1][0] == 'break':
            vel.x = 0
            velFunc_x = (acc.x / PLAYER_FRICTION) * (
                    1 + PLAYER_FRICTION) ** (self.t - time) - acc.x / PLAYER_FRICTION
        else:
            vel.x = self.get_velocity(time).x + motion[1][0]
            velFunc_x = (vel.x + acc.x / PLAYER_FRICTION) * (
                    1 + PLAYER_FRICTION) ** (self.t - time) - acc.x / PLAYER_FRICTION + motion[1][0]

        if motion[1][1] == 'break':
            vel.y = 0
            velFunc_y = acc.y * (self.t - time)
        else:
            vel.y = self.get_velocity(time).y + motion[1][1]
            velFunc_y = vel.y + acc.y * (self.t - time) + motion[1][1]

        # 위치함수
        x = pos.x + \
            ((vel.x + acc.x / PLAYER_FRICTION) * (1 + PLAYER_FRICTION) * (
                    (1 + PLAYER_FRICTION) ** (self.t - time) - 1) / PLAYER_FRICTION - acc.x * (
                     self.t - time) / PLAYER_FRICTION) - \
            0.5 * PLAYER_FRICTION * ((vel.x + acc.x / PLAYER_FRICTION) * (1 + PLAYER_FRICTION) * (
                (1 + PLAYER_FRICTION) ** ((self.t - time) - 1) - 1) / PLAYER_FRICTION -
                                     acc.x * ((self.t - time) - 1) / PLAYER_FRICTION) - \
            0.5 * acc.x * (self.t - time)
        y = pos.y + \
            vel.y * (self.t - time) + 0.5 * acc.y * (self.t - time) ** 2

        # 시간, 모션, 위치함수, 속도함수를 저장한다.
        index = self.get_index(time) + 1
        self.time_list.insert(index, time)
        self.motion_list.insert(index, motion)
        self.posFunc_list.insert(index, (x, y))
        self.velFunc_list.insert(index, (velFunc_x, velFunc_y))

    # time에 해당하는 저장된 모든 정보(모션, 위치함수, 속도함수, 시간)를 삭제한다.
    def deleteTime(self, time):
        index = self.get_index(time)
        if index == -1:
            print("오류: time 인수가 음수거나 저장된 값이 없습니다.")
        elif self.time_list[index] != time:
            print("오류: time 인수에 해당하는 값이 저장되어있지 않습니다. " + str(self.time_list[index]) + "값에 해당하는 함수가 입력한 값을 포함하고 있습니다.")
        else:
            del self.time_list[index]
            del self.motion_list[index]
            del self.posFunc_list[index]
            del self.velFunc_list[index]

    # time값에 해당하는 자료들이 위치한 인덱스를 반환한다.
    def get_index(self, time):
        if time < 0:
            print("오류: time 인수의 값이 0 이상이여야 합니다")
            return -1  # 시간값이 음수거나 아무것도 추가되어있지 않은 상태라면 -1을 반환한다.
        elif len(self.time_list) == 0:
            return -1

        for index in range(0, len(self.time_list)):
            if(time < self.time_list[index]):
                return index -1 #time이 대입될 수 있는 함수들의 위치를 반환한다.
        return len(self.time_list) - 1

    # 시간이 time값일 떄 위치를 vector로 반환한다.
    def get_position(self, time):
        index = self.get_index(time)
        if index == -1:
            return self.player_pos
        x = self.posFunc_list[index][0].subs(self.t, time)
        y = self.posFunc_list[index][1].subs(self.t, time)
        return vec(x, y)

    # 시간이 time값일 때 속도를 vector로 반환한다.
    def get_velocity(self, time):
        index = self.get_index(time)
        if index == -1:
            return vec(0, 0)
        vel_x = self.velFunc_list[index][0].subs(self.t, time)
        vel_y = self.velFunc_list[index][1].subs(self.t, time)
        return vec(vel_x, vel_y)

    # 시간이 time값일 때 가속도를 vector로 반환한다.
    def get_acceleration(self, time):
        index = self.get_index(time)
        if index == -1:
            return vec(0, 0)
        acc = self.motion_list[index][0]
        return vec(acc[0], acc[1])

    # time값에 해당하는 위치함수를 반환한다.
    def get_positionFunction(self, time):
        index = self.get_index(time)
        if index == -1:
            return ((self.player_pos.x + self.t*0), (self.player_pos.y + self.t*0))
        return self.posFunc_list[index]

    # time값에 해당하는 속도함수를 반환한다.
    def get_velocityFunction(self, time):
        index = self.get_index(time)
        if index == -1:
            return (0*self.t, 0*self.t)
        return self.posFunc_list[index]

#장애물을 플레이어의 정해진 경로에 부딫히지 않도록 설치하는 클래스
class EnemyGenerator:
    def __init__(self):
        pass
    def generate_Blade(self):
        pass
    def generate_Laser(self):
        pass