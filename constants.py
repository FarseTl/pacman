import pygame


WIDTH, HEIGHT = 448, 576
GRID_WIDTH, GRID_HEIGHT = 28, 36
FPS = 60

CELL_SIZE = 16
with open('data/maze_no_dots.txt', 'r') as lab:
    MAZE = list(map(lambda x: list(x.rstrip()), lab))

CROSSROADS_1 = [(1, 8), (6, 4), (6, 8), (6, 11), (9, 8), (12, 8),
              (15, 8), (18, 8), (21, 8), (26, 8), (21, 4), (21, 11),
              (6, 17), (9, 17), (18, 17), (21, 17), (9, 20), (18, 20),
              (6, 23), (9, 23), (18, 23), (21, 23), (6, 26), (9, 26),
              (18, 26), (21, 26), (3, 29), (24, 29), (12, 32), (15, 32)]
CROSSROADS_2 = [(12, 8), (15, 8), (12, 26), (15, 26)]



WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

FONT = 'arial black'

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
fruit = pygame.sprite.Group()