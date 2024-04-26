import sys

import pgzrun
import pygame

from platformer import build
from button import Button


# НАСТРОЙКИ КАРТЫ
TILE_SIZE = 18
ROWS = 30
COLS = 20


# НАСТРОЙКИ PGZERO
WIDTH = 800
HEIGHT = 540
TITLE = 'Platformer'

menu_font = 'far_cry_cyr_regular_0'
background_image = 'background_image.png'

click_sound = "sounds/click_button.mp3"
background_music = "background_sound.mp3"

music.play(background_music)
music.set_volume(0.5)

sound_on = True
mute_button_clicked = False

platforms = build('platformer_platforms.csv', TILE_SIZE)
mini_trees = build('platformer_mini_trees.csv', TILE_SIZE)
trees = build('platformer_trees.csv', TILE_SIZE)
water_obstacles = build('platformer_water.csv', TILE_SIZE)
diamonds = build('platformer_diamonds.csv', TILE_SIZE)


def draw():
    main_menu()
    pygame.display.flip()


def main_menu():
    global mute_button_clicked
    play_button = Button(WIDTH/2 - (375/2), 150, 375, 48,
                         "Начать игру", 'images/game_button.png',
                         'images/game_button_hover.png', None if mute_button_clicked else click_sound)
    sounds_play_button = Button(WIDTH/2-(375/2), 250, 375, 48,
                                "Вкл/Выкл музыку и звуки", 'images/game_button.png',
                                'images/game_button_hover.png', None if mute_button_clicked else click_sound)
    exit_button = Button(WIDTH/2-(375/2), 350, 375, 48,
                         "Выйти", 'images/game_button.png',
                         'images/game_button_hover.png', None if mute_button_clicked else click_sound)

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(background_image, (0, 0))

        font = pygame.font.Font(None, 90)
        text_surface = font.render("Главное меню", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH/2, 80))
        screen.blit(text_surface, text_rect)

        play_button.sound = None if mute_button_clicked else pygame.mixer.Sound(click_sound)
        sounds_play_button.sound = None if mute_button_clicked else pygame.mixer.Sound(click_sound)
        exit_button.sound = None if mute_button_clicked else pygame.mixer.Sound(click_sound)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit()

            if event.type == pygame.USEREVENT and event.button == play_button:
                print("Кнопка 'Старт' была нажата!")
                play()


            if event.type == pygame.USEREVENT and event.button == sounds_play_button:
                sound_on_off()
                mute_button_clicked = not mute_button_clicked

            if event.type == pygame.USEREVENT and event.button == exit_button:
                running = False
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
        music.play('background_sound.mp3')
    sound_on = not sound_on

def play():

    running = True
    while True:
        screen.clear()
        screen.fill('skyblue')
        for platform in platforms:
            platform.draw()
        for water in water_obstacles:
            water.draw()
        for tree in trees:
            tree.draw()
        for mini_tree in mini_trees:
            mini_tree.draw()
        for diamond in diamonds:
            diamond.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        pygame.display.flip()



pgzrun.go()
