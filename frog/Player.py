import pygame
from pygame.locals import *

from frog import load_sprite_sheets
from frog.Object import *






class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    ANIMATION_DELAY = 3



    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0

        self.health = 3

        self.hit_sound = pygame.mixer.Sound('assets/Sfx/hit.wav')  # Load a sound.
        self.hit_voice = pygame.mixer.Channel(5)

        self.sprites = load_sprite_sheets("MainCharacters", "MaskDude", 32, 32, True)
        # self.sprites = load_sprite_sheets("MainCharacters", "VirtualGuy", 32, 32, True)
        self.buttons = load_sprite_sheets("Menu", "Buttons", 18, 18, False)
        print(self.buttons)
        self.heart_sprite = self.buttons['Play'][0]


    #https://stackoverflow.com/questions/14432851/python-pygame-get-if-specific-sound-is-playing
    #https://nerdparadise.com/programming/pygame/part3
    def play_hit(self):
        if not self.hit_voice.get_busy():
             self.hit_voice.play(self.hit_sound)


    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        self.hit = True


#        print("play sound hit")
        self.play_hit()
        #if sound1.
        #sound1.get_b

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.sprites[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))
        for i in range(0, self.health):
            x = 10 + (i * 40)
            # print(x)
            win.blit(self.heart_sprite, (x, 10))

        # draw player health

