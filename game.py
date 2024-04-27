import sys

import pgzrun
import pygame

from sprites_logic import build
from button import Button
from sprites_logic import *


# НАСТРОЙКИ КАРТЫ
TILE_SIZE = 18
ROWS = 30
COLS = 20


# НАСТРОЙКИ PGZERO
WIDTH = 800
HEIGHT = 540
TITLE = "Platformer"

menu_font = "far_cry_cyr_regular_0"
main_menu_background_image = "background_image.png"

game_background_image = "image"

click_sound = "sounds/click_button.mp3"
background_music = "background_sound.mp3"

music.play(background_music)
music.set_volume(0.5)

show_main_menu = True
sound_on = True
mute_button_clicked = False

# ЗАГРУЗКА ВСЕХ ЭЛЕМЕНТОВ КАРТЫ
platforms = build("platformer_water_platforms.csv", TILE_SIZE)
mini_objects = build("platformer_water_mini_objects.csv", TILE_SIZE)
trees = build("platformer_water_trees.csv", TILE_SIZE)
water_obstacles = build("platformer_water_water_obstacles.csv", TILE_SIZE)
diamonds = build("platformer_water_diamonds.csv", TILE_SIZE)
obstacles = build("platformer_water_obstacles.csv", TILE_SIZE)

# СПРАЙТЫ
color_key = (0, 0, 0)
fox_stand = Sprite("fox_sprite_sheet.png", (0, 32, 32, 32), 14, color_key, 30)
fox_walk = Sprite("fox_sprite_sheet.png", (0, 64, 32, 32), 8, color_key, 5)

player = SpriteActor(fox_stand)
player.bottomleft = (0, HEIGHT - TILE_SIZE)
player.velocity_x = 4
player.velocity_y = 0
player.jumping = False
player.alive = True
player.scale = 1.3

gravity = 1
jump_velocity = -10
over = False
win = False
pause = False


def draw():
    screen.clear()
    if show_main_menu:
        main_menu()
    else:
        screen.blit(game_background_image, (0, 0))
        for platform in platforms:
            platform.draw()
        for water in water_obstacles:
            water.draw()
        for tree in trees:
            tree.draw()
        for mini_obj in mini_objects:
            mini_obj.draw()
        for diamond in diamonds:
            diamond.draw()
        for obstacle in obstacles:
            obstacle.draw()

        if player.alive:
            player.draw()

        if over:
            screen.draw.text("ИГРА ОКОНЧЕНА, ДЛЯ ПРОДОЛЖЕНИЯ НАЖМИТЕ КНОПКУ 'ENTER'", center=(WIDTH / 2, HEIGHT / 2))
        if win:
            screen.draw.text("YOU WON", center=(WIDTH / 2, HEIGHT / 2))
        if pause:
            screen.draw.text('ИГРА ПРИОСТАНОВЛЕНА, НАЖМИТЕ ПРОБЕЛ ДЛЯ ВОЗОБНОВЛЕНИЯ', center=(WIDTH / 2, HEIGHT / 2))


def update():
    # declare scope of global variables
    global win, over, pause, show_main_menu

    # if game is over, no more updating game state, just return
    if over or win or pause:
        return

    # handle fox left movement
    if keyboard.LEFT and player.left > 0:
        player.x -= player.velocity_x
        # flip image and change sprite
        player.sprite = fox_walk
        player.flip_x = True
        # if the movement caused a collision
        if player.collidelist(platforms) != -1:
            # get object that fox collided with
            collided = platforms[player.collidelist(platforms)]
            # use it to calculate position where there is no collision
            player.left = collided.right

    # handle fox right movement
    elif keyboard.RIGHT and player.right < WIDTH:
        player.x += player.velocity_x
        # flip image and change sprite
        player.sprite = fox_walk
        player.flip_x = False
        # if the movement caused a collision
        if player.collidelist(platforms) != -1:
            # get object that fox collided with
            collided = platforms[player.collidelist(platforms)]
            # use it to calculate position where there is no collision
            player.right = collided.left

    # handle gravity
    player.y += player.velocity_y
    player.velocity_y += gravity
    # if the movement caused a collision, move position back
    if player.collidelist(platforms) != -1:
        # get object that fox collided with
        collided = platforms[player.collidelist(platforms)]
        # moving down - hit the ground
        if player.velocity_y >= 0:
            # move fox up to no collision position
            player.bottom = collided.top
            # no longer jumping
            player.jumping = False
        # moving up - bumped their head
        else:
            # move fox down to no collision position
            player.top = collided.bottom
        # reset velocity
        player.velocity_y = 0

    # fox collided with obstacle, game over
    if player.collidelist(obstacles) != -1:
        player.alive = False
        over = True

    if player.collidelist(water_obstacles) != -1:
        player.alive = False
        over = True

    # check if fox collected mushrooms
    for diamond in diamonds:
        if player.colliderect(diamond):
            diamonds.remove(diamond)

    # check if fox collected all mushrooms
    if len(diamonds) == 0:
        win = True

#
# def update():
#     global over, win
#     if not show_main_menu:
#         if keyboard.LEFT and player.midleft[0] > 0:
#             player.x -= player.velocity_x
#             player.sprite = fox_walk
#             player.flip_x = True
#
#             if player.collidelist(platforms) != -1:
#                 object = platforms[player.collidelist(platforms)]
#                 player.x = object.x + (object.width / 2 + player.width / 2)
#
#         elif keyboard.RIGHT and player.midright[0] < WIDTH:
#             player.x += player.velocity_x
#             player.sprite = fox_walk
#             player.flip_x = False
#
#             if player.collidelist(platforms) != -1:
#                 object = platforms[player.collidelist(platforms)]
#                 player.x = object.x - (object.width / 2 + player.width / 2)
#
#     player.y += player.velocity_y
#     player.velocity_y += gravity
#
#     if player.collidelist(platforms) != -1:
#         object = platforms[player.collidelist(platforms)]
#
#         if player.velocity_y >= 0:
#             player.y = object.y - (object.height / 2 + player.height / 2)
#             player.jumping = False
#
#         else:
#             player.y = object.y + (object.height / 2 + player.height / 2)
#
#         player.velocity_y = 0
#
#     if player.collidelist(water_obstacles) != -1:
#         player.alive = False
#         over = True
#
#     for diamond in diamonds:
#         if player.colliderect(diamond):
#             diamonds.remove(diamond)
#
#         if len(diamonds) == 0:
#             win = True
#             over = True


def main_menu():
    global show_main_menu
    global mute_button_clicked
    play_button = Button(
        WIDTH / 2 - (375 / 2),
        150,
        375,
        48,
        "Начать игру",
        "images/game_button.png",
        "images/game_button_hover.png",
        None if mute_button_clicked else click_sound,
    )
    sounds_play_button = Button(
        WIDTH / 2 - (375 / 2),
        250,
        375,
        48,
        "Вкл/Выкл музыку и звуки",
        "images/game_button.png",
        "images/game_button_hover.png",
        None if mute_button_clicked else click_sound,
    )
    exit_button = Button(
        WIDTH / 2 - (375 / 2),
        350,
        375,
        48,
        "Выйти",
        "images/game_button.png",
        "images/game_button_hover.png",
        None if mute_button_clicked else click_sound,
    )

    while show_main_menu:
        screen.fill((0, 0, 0))
        screen.blit(main_menu_background_image, (0, 0))

        font = pygame.font.Font(None, 90)
        text_surface = font.render("Главное меню", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH / 2, 80))
        screen.blit(text_surface, text_rect)

        play_button.sound = (
            None if mute_button_clicked else pygame.mixer.Sound(click_sound)
        )
        sounds_play_button.sound = (
            None if mute_button_clicked else pygame.mixer.Sound(click_sound)
        )
        exit_button.sound = (
            None if mute_button_clicked else pygame.mixer.Sound(click_sound)
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.USEREVENT and event.button == play_button:
                show_main_menu = False
                draw()

            if event.type == pygame.USEREVENT and event.button == sounds_play_button:
                sound_on_off()
                mute_button_clicked = not mute_button_clicked

            if event.type == pygame.USEREVENT and event.button == exit_button:
                quit()

            for btn in [play_button, sounds_play_button, exit_button]:
                btn.handle_event(event)

        for btn in [play_button, sounds_play_button, exit_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        pygame.display.flip()


def sound_on_off():
    global sound_on, mute_button_clicked
    if sound_on:
        music.stop()
    else:
        music.play("background_sound.mp3")
    sound_on = not sound_on


def on_key_down(key):
    global pause, show_main_menu, win, over

    if not over:
        if key == keys.SPACE:
            pause = not pause

    if key == keys.UP and not player.jumping:
        player.velocity_y = jump_velocity
        player.jumping = True

    if over:
        if key == keys.RETURN:
            reset_game()


def on_key_up(key):
    if key == keys.LEFT or key == keys.RIGHT:
        player.sprite = fox_stand


def reset_game():
    global win, over, pause, diamonds

    over = False
    win = False
    pause = False

    player.alive = True
    player.bottomleft = (0, HEIGHT - TILE_SIZE)
    player.velocity_x = 4
    player.velocity_y = 0
    player.jumping = False

    for diamond in diamonds:
        diamonds.remove(diamond)

    diamonds = build("platformer_water_diamonds.csv", TILE_SIZE)


pgzrun.go()
