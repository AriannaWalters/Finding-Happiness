# Sprite classes for platform game
import pygame as pg
from Settings import *
from random import choice, randrange
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.jumping = False

        self.image = pg.image.load("Main_Character.png")
        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
        self.rect.center = (40, HEIGHT - 100)
        self.pos = vec(40, HEIGHT - 100)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def jump(self):
        # jump only if standing on a platform
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2
        if hits and not self.jumping:
            self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP


    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2


        self.rect.midbottom = self.pos


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        #self.image = pg.Surface((w, h))
        #self.image = pg.image.load("Stable_Dark.png")
        image = [pg.image.load("Stable_Dark.png"),
                    pg.image.load("Unstable_Dark.png")]
        """light_platforms = [pg.image.load("Stable_Light.png"),
                    pg.image.load("Unstable_Light.png")]"""

        self.image = choice(image)
        # Set a referance to the image rect.
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        if randrange(100) < POW_SPAWN_PCT:
            Pow(self.game, self)

    def setImage(self,image):
        updateimage = pg.image.load(image)
        self.image = updateimage

class Pow(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self._layer = POW_LAYER
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = choice(['boost'])
        self.image = pg.image.load("Good_Feelings.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()

class Mob(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_up = pg.image.load("Bad_Feelings.png")
        self.image_up.set_colorkey(BLACK)
        self.image_down = pg.image.load("Bad_Feelings.png")
        self.image_down.set_colorkey(BLACK)
        self.image = self.image_up
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, WIDTH + 100])
        self.vx = randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.vx *= -1
        self.rect.y = randrange(HEIGHT / 2)
        self.vy = 0
        self.dy = 0.5

    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1
        center = self.rect.center
        if self.dy < 0:
            self.image = self.image_up
        else:
            self.image = self.image_down
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.center = center
        self.rect.y += self.vy
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()
