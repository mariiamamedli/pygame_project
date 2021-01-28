import pygame
from pygame import mixer
from random import choice

if __name__ == '__main__':
    pygame.mixer.pre_init()
    mixer.init()
    pygame.init()

    # иконка
    pygame.display.set_icon(pygame.image.load("data/icon.ico"))

    # не менять, а то счетчик времени работать не будет
    clock = pygame.time.Clock()
    fps = 60

    # размеры экрана, тайлов, персонажа, врагов и т.д.
    screen_width = 640
    screen_height = 640

    tile_size = 32
    particle_size = 40

    player_width = 28
    player_height = 40
    enemy_width = 32
    enemy_height = 25
    liquid_width = 32
    liquid_height = 18

    restart_btn_height = 32
    start_btn_height = 100

    # шрифт
    font_name = 'Berlin Sans FB Demi'
    font = pygame.font.SysFont(font_name, 64)
    font_score = pygame.font.SysFont(font_name, 16)

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('pygame_project')

    # загрузка изображений для тайлов, платформ, кнопок и всего такого
    bg_img = pygame.image.load('data/bg.png')
    bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))

    block_1_img = pygame.image.load('data/block_1.png')
    block_1_img = pygame.transform.scale(block_1_img, (tile_size, tile_size))
    block_2_img = pygame.image.load('data/block_2.png')
    block_2_img = pygame.transform.scale(block_2_img, (tile_size, tile_size))

    platform_img = pygame.image.load('data/platform.png')
    platform_img = pygame.transform.scale(platform_img, (tile_size, tile_size // 2))

    enemy_img = pygame.image.load('data/enemy.png')
    enemy_img = pygame.transform.scale(enemy_img, (enemy_width, enemy_height))

    liquid_img = pygame.image.load('data/liquid.png')
    liquid_img = pygame.transform.scale(liquid_img, (liquid_width, liquid_height))

    exit_img = pygame.image.load('data/exit.png')
    exit_img = pygame.transform.scale(exit_img, (tile_size, int(tile_size * 1.5)))

    coin_img = pygame.image.load('data/coin.png')
    coin_img = pygame.transform.scale(coin_img, (tile_size // 2, tile_size // 2))

    clock_img = pygame.image.load('data/clock.png')
    clock_img = pygame.transform.scale(clock_img, (tile_size // 2, tile_size // 2))

    death_img = pygame.image.load('data/death.png')
    death_img = pygame.transform.scale(death_img, (tile_size // 2, tile_size // 2))

    restart_img = pygame.image.load('data/restart.png')
    restart_img = pygame.transform.scale(restart_img,
                                         (int(restart_img.get_width() / restart_img.get_height() * restart_btn_height),
                                          restart_btn_height))

    start_img = pygame.image.load('data/start.png')
    start_img = pygame.transform.scale(start_img, (int(start_img.get_width() / start_img.get_height() * start_btn_height),
                                                   start_btn_height))

    star_img = pygame.image.load('data/star.png')
    star_img = pygame.transform.scale(star_img, (particle_size, particle_size))

    game_over = False
    level_completed = True

    cur_level = -1

    # карты уровней
    lvl1 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 8, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 2, 2, 1],
            [1, 0, 0, 0, 2, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 2, 2, 1, 1, 1],
            [1, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

    lvl2 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 8, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 2, 1, 0, 0, 0, 2, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 1, 1, 2, 2, 2, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1]]

    lvl3 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 7, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 1],
            [1, 2, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 2, 0, 0, 0, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 3, 7, 0, 7, 0, 1],
            [1, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1]]

    lvl4 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 1],
            [1, 2, 2, 0, 0, 4, 0, 0, 4, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 2, 2, 2, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 2, 2, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 5, 0, 0, 1],
            [1, 0, 0, 2, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 7, 0, 1],
            [1, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1]]

    lvl5 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 7, 0, 2, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 5, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 2, 2, 6, 6, 6, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 7, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 2, 1],
            [1, 0, 0, 0, 0, 2, 2, 2, 6, 6, 2, 0, 3, 0, 0, 3, 0, 2, 1, 1],
            [1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1]]

    lvl6 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 1],
            [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1],
            [1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1],
            [1, 0, 0, 2, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1],
            [1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

    levels = [lvl1, lvl2, lvl3, lvl4, lvl5, lvl6]
    max_level = min(5, len(levels) - 1)
    num_comp_lvls = -1

    # подключение музыки
    main_music_loud = 0.5
    signal_sound_loud = 1
    pygame.mixer.music.load('data/music.mp3')
    pygame.mixer.music.set_volume(main_music_loud)
    pygame.mixer.music.play(-1)
    musics = []
    for i in range(1, 1 + max_level):
        musics += ['data/music{i}.mp3']
    coin_sound = pygame.mixer.Sound('data/coin.mp3')
    coin_sound.set_volume(signal_sound_loud)
    jump_sound = pygame.mixer.Sound('data/jump.mp3')
    jump_sound.set_volume(signal_sound_loud)
    game_over_sound = pygame.mixer.Sound('data/game_over.mp3')
    game_over_sound.set_volume(signal_sound_loud)

    score_coins = 0
    score_time = 0
    score_death = 0

    black = (0, 0, 0)
    white = (255, 255, 255)


    # функция отрисовки надписей
    def draw_text(text, font, color, pos):
        x, y = pos
        text = font.render(text, True, color)
        screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))


    # функция для открытия нового уровня из его карты
    def open_level(cur_level):
        global world
        player.create(tile_size * 2, screen_height - tile_size - player_height)

        enemy_group.empty()
        liquid_group.empty()
        exit_group.empty()
        coin_group.empty()
        coin_group.add(coin_0)
        platform_group.empty()

        world_data = levels[cur_level]
        world = World(world_data)

        # на всякий случай
        try:
            pygame.mixer.music.load(f'data/music{cur_level + 1}.mp3')
        except Exception:
            pygame.mixer.music.load(f'data/music.mp3')
        pygame.mixer.music.play(-1)


    # класс кнопок (для кнопки старта и рестарта)
    class Button:
        def __init__(self, x, y, image):
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.clicked = False

        def update(self):
            pos = pygame.mouse.get_pos()

            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                    self.clicked = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            screen.blit(self.image, self.rect)


    # сам игрок
    class Player:
        def __init__(self, x, y):
            self.create(x, y)

        def update(self):
            global game_over, level_completed, score_death
            dx = 0  # перемещение горизонтальное
            dy = 0  # и вертикальное

            # константы - скорость изменения спрайта, скорость прыжка/ходьба и для движения по платформам
            walk_cooldown = 4
            jump_v = 14
            walk_v = 4
            col_thresh = 20

            if not game_over:
                key = pygame.key.get_pressed()
                if key[pygame.K_UP] and not self.jumped and not self.in_air:
                    jump_sound.play()
                    self.grv = -jump_v
                    self.jumped = True
                if not key[pygame.K_UP]:
                    self.jumped = False
                if key[pygame.K_LEFT]:
                    dx -= walk_v
                    self.counter += 1
                    self.direction = -1
                if key[pygame.K_RIGHT]:
                    dx += walk_v
                    self.counter += 1
                    self.direction = 1
                if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
                    self.counter = 0
                    self.index = 0
                    if self.direction == 1:
                        self.image = self.images_right[self.index]
                    if self.direction == -1:
                        self.image = self.images_left[self.index]

                # смена спрайта
                if self.counter > walk_cooldown:
                    self.counter = 0
                    self.index += 1
                    if self.index >= len(self.images_right):
                        self.index = 0
                    if self.direction == 1:
                        self.image = self.images_right[self.index]
                    if self.direction == -1:
                        self.image = self.images_left[self.index]

                # гравитация (чтобы падать) (надо добавить смерть от падения)
                self.grv += 1
                if self.grv > 10:
                    self.grv = 10
                dy += self.grv

                # проверка нахождение не на чем-то
                self.in_air = True

                for tile in world.tile_list:
                    if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                        dx = 0

                    if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                        if self.grv < 0:
                            dy = tile[1].bottom - self.rect.top
                            self.grv = 0

                        elif self.grv >= 0:
                            dy = tile[1].top - self.rect.bottom
                            self.grv = 0
                            self.in_air = False

                # проверка живости (?) игрока
                if pygame.sprite.spritecollide(self, enemy_group, False):
                    game_over = True

                if pygame.sprite.spritecollide(self, liquid_group, False):
                    game_over = True

                if game_over:
                    game_over_sound.play()
                    score_death += 1

                # пройден ли уровень
                if pygame.sprite.spritecollide(self, exit_group, False):
                    level_completed = True

                # платформы (почти как с тайлами, там где in_air)
                for platform in platform_group:
                    if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                        dx = 0

                    if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                        if abs(self.rect.top + dy - platform.rect.bottom) < col_thresh:
                            self.grv = 0
                            dy = platform.rect.bottom - self.rect.top

                        elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                            self.rect.bottom = platform.rect.top - 1
                            self.in_air = False
                            dy = 0

                        if platform.move_x != 0:
                            self.rect.x += platform.move_direction

                # собственно, само перемещение
                self.rect.x += dx
                self.rect.y += dy

                # чтобы с экрана не падать, если рамки нет (но она есть)
                # if self.rect.bottom > screen_height:
                #    self.rect.bottom = screen_height

            else:
                # умерли, бывает
                self.image = self.dead
                if self.rect.y > -100:
                    self.rect.y -= 5

            # отрисовка игрока
            screen.blit(self.image, self.rect)
            # pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # и сетки вокруг него

        def create(self, x, y):
            self.images_right = []
            self.images_left = []
            self.index = 0
            self.counter = 0

            for num in range(1, 1 + 4):  # загрузка спрайтов игрока
                right_img = pygame.image.load(f'data/player_{num}.png')
                right_img = pygame.transform.scale(right_img, (player_width, player_height))

                left_img = pygame.transform.flip(right_img, True, False)

                self.images_right += [right_img]
                self.images_left += [left_img]

            # и картинка для призрака
            ghost_img = pygame.image.load('data/ghost.png')
            ghost_img = pygame.transform.scale(ghost_img, (player_width, player_width))
            self.dead = ghost_img

            self.image = self.images_right[self.index]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.width = self.image.get_width()
            self.height = self.image.get_height()

            self.grv = 0
            self.jumped = False
            self.direction = 0
            self.in_air = True


    # класс самого уровня
    class World:
        def __init__(self, data):
            self.tile_list = []  # список тайлов

            row_count = 0
            for row in data:
                col_count = 0
                for tile in row:
                    if tile == 1:  # блоки, которые не на поверхности
                        img = block_1_img
                        img_rect = img.get_rect()
                        img_rect.x = col_count * tile_size
                        img_rect.y = row_count * tile_size
                        tile = (img, img_rect)
                        self.tile_list.append(tile)

                    if tile == 2:  # которые на поверхности (с полосочкой)
                        img = block_2_img
                        img_rect = img.get_rect()
                        img_rect.x = col_count * tile_size
                        img_rect.y = row_count * tile_size
                        tile = (img, img_rect)
                        self.tile_list.append(tile)

                    if tile == 3:  # слизняки
                        enemy = Enemy(col_count * tile_size, row_count * tile_size)
                        enemy.rect.bottom = ((row_count + 1) * tile_size)
                        enemy_group.add(enemy)

                    if tile == 4:  # платформы горизонтальные
                        platform = Platform(col_count * tile_size, row_count * tile_size, 1, 0)
                        platform_group.add(platform)

                    if tile == 5:  # вертикальные
                        platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1)
                        platform_group.add(platform)

                    if tile == 6:  # жидкость, в которую лучше не падать
                        liquid = Liquid(col_count * tile_size, row_count * tile_size)
                        liquid.rect.bottom = ((row_count + 1) * tile_size)
                        liquid_group.add(liquid)

                    if tile == 7:  # монетки (собирать надо, бросать не надо)
                        coin = Coin(col_count * tile_size + (tile_size // 2),
                                    row_count * tile_size + (tile_size // 2))
                        coin_group.add(coin)

                    if tile == 8:  # выход с уровня
                        exit = Exit(col_count * tile_size, row_count * tile_size)
                        exit.rect.bottom = ((row_count + 1) * tile_size)
                        exit_group.add(exit)

                    col_count += 1
                row_count += 1

        def draw(self):
            for tile in self.tile_list:
                screen.blit(tile[0], tile[1])
                # pygame.draw.rect(screen, (0, 0, 0), tile[1], 2)  # сеточка вокруг блоков


    # класс врагов (слизняков)
    class Enemy(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = enemy_img
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.move_direction = 1
            self.move_counter = 0

        def update(self):
            self.rect.x += self.move_direction
            self.move_counter += 1
            if abs(self.move_counter) > 32:
                self.move_direction *= -1
                self.move_counter *= -1


    # жижа
    class Liquid(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = liquid_img
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y


    # выход
    class Exit(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = exit_img
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y


    # монетки
    class Coin(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = coin_img
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)


    # платформы
    class Platform(pygame.sprite.Sprite):
        def __init__(self, x, y, move_x, move_y):
            pygame.sprite.Sprite.__init__(self)
            self.image = platform_img
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.move_counter = 0
            self.move_direction = 1
            self.move_x = move_x
            self.move_y = move_y

        def update(self):
            self.rect.x += self.move_direction * self.move_x
            self.rect.y += self.move_direction * self.move_y
            self.move_counter += 1
            if abs(self.move_counter) > 32:
                self.move_direction *= -1
                self.move_counter *= -1


    # звездочки в результатах
    class Particle(pygame.sprite.Sprite):
        fire = [star_img]
        for scale in (5, 10, 20):
            fire.append(pygame.transform.scale(fire[0], (scale, scale)))

        def __init__(self, pos, dx, dy):
            super().__init__(star_group)
            self.image = choice(self.fire)
            self.rect = self.image.get_rect()

            self.velocity = [dx, dy]
            self.rect.x, self.rect.y = pos

            self.gravity = 1

        def update(self):
            self.velocity[1] += self.gravity
            self.rect.x += self.velocity[0]
            self.rect.y += self.velocity[1]

            if not self.rect.colliderect((0, 0, screen_width, screen_height)):
                self.kill()


    def create_particles(position):
        numbers = range(-5, 6)
        Particle(position, choice(numbers), choice(numbers))


    player = Player(tile_size * 2, screen_height - tile_size - player_height)

    enemy_group = pygame.sprite.Group()
    liquid_group = pygame.sprite.Group()
    exit_group = pygame.sprite.Group()
    coin_group = pygame.sprite.Group()
    platform_group = pygame.sprite.Group()

    star_group = pygame.sprite.Group()

    world = World(levels[cur_level])

    restart_btn = Button(screen_width // 2 - restart_img.get_width() // 2,
                         screen_height // 2 + restart_img.get_height() * 1.5, restart_img)

    start_btn = Button(screen_width // 2 - start_img.get_width() // 2,
                       screen_height // 2 - start_img.get_height() // 2, start_img)

    # значок монетки в панельке сверху (зачем рисовать отдельно)
    coin_0 = Coin(tile_size // 2, tile_size // 2)
    coin_group.add(coin_0)

    running_start_window = True
    running_game = False
    running_ending = False

    while running_start_window:
        screen.blit(bg_img, (0, 0))
        start_btn.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_start_window = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running_start_window = False
                    running_game = True

        if start_btn.clicked:
            running_start_window = False
            running_game = True

        pygame.display.flip()

    while running_game:
        clock.tick(fps)
        score_time += 1

        if level_completed:
            cur_level += 1
            if cur_level <= max_level:
                open_level(cur_level)
            else:
                cur_level = max_level + 1
                running_game = False
                running_ending = True
            level_completed = False

        screen.blit(bg_img, (0, 0))
        world.draw()

        if not game_over:
            game_over_sound.stop()
            enemy_group.update()
            platform_group.update()
            if pygame.sprite.spritecollide(player, coin_group, True):
                coin_sound.play()
                score_coins += 1

        # панелька сверху
        draw_text('X ' + str(score_coins), font_score, white, (tile_size + 10, tile_size // 2))

        screen.blit(clock_img, (tile_size * 3, tile_size // 4))
        draw_text(f'{str(score_time // 3600).rjust(2, "0")}:{str(score_time % 3600 // 60).rjust(2, "0")}',
                  font_score, white, (tile_size * 4 + 10, tile_size // 2))

        screen.blit(death_img, (tile_size * 6, tile_size // 4))
        draw_text('X ' + str(score_death), font_score, white, (tile_size * 7 + 2, tile_size // 2))

        lvls_img = pygame.transform.scale(exit_img, (tile_size // 3, tile_size // 2))
        screen.blit(lvls_img, (screen_width - tile_size * 2, tile_size // 4))
        draw_text('X ' + str(cur_level), font_score, white, (screen_width - tile_size - 1, tile_size // 2))

        enemy_group.draw(screen)
        liquid_group.draw(screen)
        exit_group.draw(screen)
        coin_group.draw(screen)
        platform_group.draw(screen)

        player.update()

        if game_over:
            draw_text('GAME OVER!', font, black, (screen_width // 2, screen_height // 2))
            restart_btn.update()
            key = pygame.key.get_pressed()
            if restart_btn.clicked or key[pygame.K_RETURN]:
                player.create(tile_size * 2, screen_height - tile_size - player_height)
                game_over = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_game = False

        pygame.display.flip()

    if running_ending:
        pygame.mixer.music.load('data/music.mp3')
        pygame.mixer.music.set_volume(main_music_loud)
        pygame.mixer.music.play(-1)

    while running_ending:
        clock.tick(fps)

        screen.blit(bg_img, (0, 0))

        for i in range(-300, 310, 50):
            create_particles((screen_width // 2 + i, 0))

        star_group.update()
        star_group.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_ending = False

        # результаты
        draw_text('YOU WIN!', font, black, (screen_width // 2, screen_height // 2 - 120))
        draw_text(f'COINS{"." * ((292 - (len(str(score_coins)) * 8 + 46)) // 5)}{score_coins}', font_score, black,
                  (screen_width // 2, screen_height // 2 - 80))
        time = f'{str(score_time // 3600).rjust(2, "0")}:{str(score_time % 3600 // 60).rjust(2, "0")}'
        draw_text(f'TIME{"." * ((292 - (len(time) * 8 + 35)) // 5)}{time}', font_score, black, (screen_width // 2,
                                                                                                screen_height // 2 - 50))
        draw_text(f'DEATHS{"." * ((292 - (len(str(score_death)) * 8 + 58)) // 5)}{score_death}', font_score, black,
                  (screen_width // 2, screen_height // 2 - 20))

        pygame.display.flip()

    pygame.quit()
