#!/usr/bin/env python
import pygame
from pygame.locals import *

from frog import Object, Fire, load_sprite_sheets
from frog.Fire import *
from frog.Player import Player
from frog.Block import Block


from os.path import join
pygame.init()

pygame.display.set_caption("Platformer")

WIDTH, HEIGHT = 1280, 720
# WIDTH, HEIGHT = 800, 800
FPS = 60
PLAYER_VEL = 5

#window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

print ("desktops", pygame.display.get_desktop_sizes())
# https://github.com/pygame/pygame/blob/dac5b2e49613670f4c59ee7db06f2830e6e090ff/examples/setmodescale.py
# window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.RESIZABLE)


#         screen.blit(pygame.transform.scale(pic, screen.get_size()), (0, 0))
        # pygame.display.update()


window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)

#window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
#pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)


#https://stackoverflow.com/questions/43845800/how-do-i-add-background-music-to-my-python-game
pygame.mixer.init()
pygame.mixer.music.load("music.wav")
# loops -1 continue indefinitely
pygame.mixer.music.play(-1,0.0)


# TODO config inputs.
# TODO allow controller

# TODO use text file for tile placement

def update_window(fullscreen):
    print(WIDTH)
    if fullscreen:
        #window = 
        pygame.display.set_mode((WIDTH, HEIGHT),pygame.FULLSCREEN | pygame.SCALED)
    else:
        #window = 
        pygame.display.set_mode((WIDTH, HEIGHT),  pygame.SCALED)


def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image


def draw(window, background, bg_image, player, objects, offset_x):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)


    pygame.display.update()


def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects


def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object


def handle_move(player, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)

    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]

    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()



def get_objects_from_file(file_path, block_size = 96):
    objects = []

    with open(file_path) as f:
        row = 0
        col = 0
        for line in f:
            col = 0
            for char in line:
                # print(row,col)
                if char == '0':
                    block = Block(block_size * col, block_size * row, block_size)
                    objects.append(block)
                elif char == 'F':
                    fire = Fire(block_size * col, (block_size * row) + 32, 16, 32)
                    fire.on()
                    objects.append(fire)
                elif char == 'D': #double fire
                    fire = Fire(block_size * col, (block_size * row) + 32, 16, 32)
                    fire.on()
                    objects.append(fire)
                    fire2 = Fire(block_size * col + 64, (block_size * row) + 32, 16, 32)
                    fire2.on()
                    objects.append(fire2)

                col += 1
            row += 1
    return objects


# TODO read map1.txt
def get_objects():
    block_size = 96
    fire = Fire(100, HEIGHT - block_size - 64, 16, 32)
    fire.on()
    floor = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]
    objects = [*floor, Block(0, HEIGHT - block_size * 2, block_size),
               Block(block_size * 3, HEIGHT - block_size * 4, block_size), fire]
    
    # return objects

    return get_objects_from_file("map1.txt")

def main(window):
    fullscreen = False

    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")

    player = Player(100, 100, 50, 50)

    objects = get_objects()

    offset_x = 0
    #scroll_area_width = 200
    scroll_area_width = 400

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()
                elif event.key == K_ESCAPE:
                    run = False
                    #sys.exit()
                if event.key == K_f:
                    fullscreen = not fullscreen
                    
                    update_window(fullscreen)


        player.loop(FPS)

        for object in objects:
            #https://stackoverflow.com/questions/610883/how-can-i-check-if-an-object-has-an-attribute
            if hasattr(object, 'loop'):
                object.loop()
        #fire.loop()


        handle_move(player, objects)
        draw(window, background, bg_image, player, objects, offset_x)

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)
