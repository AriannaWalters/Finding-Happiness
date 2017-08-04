# ""- Made by Arianna Walters and Israeliah Davis
import pygame as pg
import random
from random import choice
from Settings import *
from Sprites import *
from os import path

#img_dir = path.join(path.dirname(__file__), 'img')

class Game:
    def __init__(self):
        # initialize pygame and create window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        # load high score
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        # load sounds
        self.snd_dir = path.join(self.dir, 'snd')
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Jump.wav'))
        self.boost_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Boost16.wav'))



    def new(self):
        # start a new game
        self.score = 0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
             Platform(self, *plat)
        self.mob_timer = 0
        pg.mixer.music.load(path.join(self.snd_dir, 'Background_Music.mp3'))
        self.run()

    def run(self):
        # Game Loop
        pg.mixer.music.play(loops=-1)
        self.playing = True
            # Set positions of graphics

            # Load and set up graphics.
        self.screen.blit(background_image1, background_position)
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()

        # spawn a mob?
        now = pg.time.get_ticks()
        if now - self.mob_timer > 5000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            Mob(self)
        # hit mobs?
        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False, pg.sprite.collide_mask)
        if mob_hits:
            self.playing = False

        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.y < lowest.rect.centery:
                    self.player.pos.y = lowest.rect.top
                    self.player.vel.y = 0
                    self.player.jumping = False

         # if player reaches top 1/4 of screen
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y), 2)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10


        # if player hits powerup
        pow_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for pow in pow_hits:
            if pow.type == 'boost':
                self.boost_sound.play()
                self.player.vel.y = -BOOST_POWER
                self.player.jumping = False

        #Die!
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

        # spawn new platforms to keep same average number
        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            p = Platform(self, random.randrange(0, WIDTH - width),
                         random.randrange(-75, -35))

    def events(self):
        # Game Loop - events
        pause = False
        for event in pg.event.get():
            #  check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()
                if event.key == pg.K_p:
                    pause = True
        while pause == True:
            self.draw_text("Paused", 50, RED, WIDTH / 2, HEIGHT / 2.5)
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.KEYUP:
                    if event.key == pg.K_p:
                        pause = False

    def draw(self):
        # Game Loop - draw
        #self.screen.fill(BGCOLOR)
        # Copy image to screen:
        if self.score < 100:
            self.screen.blit(background_image1, background_position)
            #self.image = image
        elif self.score >= 100 and self.score <300:
            self.screen.blit(background_image2, background_position)
        else:
            for platform in self.platforms:
                platform.setImage("Stable_Light.png")
                self.update
            self.screen.blit(background_image3, background_position)
            #self.image = image1

        #background = pg.image.load("bottom_Background.jpg")
        #background_rect = background.get_rect()
        #self.screen.blit(background, background_rect)
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.draw_text(str(self.score), 22, RED, WIDTH / 2, 15)
        # *after* drawing everything, flip the display
        pg.display.flip()



    def show_start_screen(self):
        # game splash/start screen
        pg.mixer.music.load(path.join(self.snd_dir, 'Morning Walk.mp3'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        #self.image = pg.image.load("gameSelection.png")
        # Set a referance to the image rect.
        #self.rect = self.image.get_rect()

        self.draw_text("Arrows to move, Space to jump", 22, WHITE, WIDTH / 2, HEIGHT / 2.5)
        self.draw_text("Avoid the bad feelings, jump on the good feelings for a boost", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press P to pause", 22, WHITE, WIDTH / 2, HEIGHT / 1.8)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("Hint: Transport from one side to the other", 22, WHITE, WIDTH / 2, HEIGHT * 3.5 / 4)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        pg.mixer.music.load(path.join(self.snd_dir, 'Old Soul.mp3'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER!", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Happiness Level: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2.5)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("Quote:", 24, BLACK, WIDTH /2, HEIGHT/ 1.7)
        Quotes = ["Once you choose hope, anything is possible.","Storms Don't Last Forever",
                    "Stars can't shine without Darkness", "There are hidden blessings in every struggle",
                    "One day at a time. One moment at a time.", "No one is perfect, that's why pencils have erasers.",
                    "Be a Warrior, not a Worrier", "There's light at the end of the tunnel."]
        self.Quotes = choice(Quotes)
        self.draw_text(self.Quotes, 24, BLUE, WIDTH/2, HEIGHT/ 1.6 )
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("Highest Happiness Score : " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 10)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)



g = Game()
background_image1 = pg.image.load("bottomBackground3.jpg")
background_image2 = pg.image.load("middleBackground2.jpg")
background_image3 = pg.image.load("topBackground2.jpg")
background_position = [0, 0]



g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
