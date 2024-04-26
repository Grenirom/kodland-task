import pgzrun

WIDTH = 800
HEIGHT = 600

sounds_enabled = True
menu_font = 'far_cry_cyr_regular_0'
background_image = 'main_menu_image.png'


def draw():
    screen.blit(background_image, (0, 0))
    screen.draw.text('Главное меню', midtop=(WIDTH // 2, 100), color='turquoise', fontsize=70, fontname=menu_font)
    screen.draw.text('Начать игру', midtop=(WIDTH // 2, 250), color='mediumspringgreen', fontsize=40, fontname=menu_font)
    screen.draw.text('Вкл/Выкл музыку и звуки', midtop=(WIDTH // 2, 350), color='mediumspringgreen', fontsize=40,
                     fontname=menu_font)
    screen.draw.text('Выйти', midtop=(WIDTH // 2, 450), color='firebrick', fontsize=40, fontname=menu_font)


pgzrun.go()
