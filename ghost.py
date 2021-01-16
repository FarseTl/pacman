import pygame
from constants import *
from math import sqrt
from random import randint


class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.x, self.y = x, y
        self.add(enemies)
        self.target_cell = None
        self.direction = (0, 1)
        self.stored_direction = None
        self.image = pygame.Surface((20, 20))
        self.rect = pygame.Rect(self.x * 16 - 2, self.y * 16 - 2, 20, 20)
        self.cell_rect = pygame.Rect(self.x * 16, self.y * 16, 16, 16)
        self.state = 'chase'
        self.right, down, up = None, None, None
        self.rotation = 'left'
        self.sprite = 0
        self.animCount = 0
        self.fright_blue = [pygame.image.load('data/fright_1.png'), pygame.image.load('data/fright_2.png')]
        self.fright_white = [pygame.image.load('data/fright_3.png'), pygame.image.load('data/fright_4.png')]
        self.color = None

    def set_target_cell(self, pacman):
        if self.state == 'frightening':
            self.target_cell = (randint(0, 27), randint(3, 33))

    def change_path(self, nx, ny):
        x, y = self.target_cell
        distances = {}

        if MAZE[ny - 1][nx] == '0' and ny - 1 != self.y:
            cell_3 = (nx, ny - 1)
            distances[abs(cell_3[0] - x) ** 2 + abs(cell_3[1] - y) ** 2] = cell_3
        if MAZE[ny][nx - 1] == '0' and nx - 1 != self.x:
            cell_1 = (nx - 1, ny)
            distances[abs(cell_1[0] - x) ** 2 + abs(cell_1[1] - y) ** 2] = cell_1
        if MAZE[ny + 1][nx] == '0' and ny + 1 != self.y:
            cell_4 = (nx, ny + 1)
            distances[abs(cell_4[0] - x) ** 2 + abs(cell_4[1] - y) ** 2] = cell_4
        if MAZE[ny][nx + 1] == '0' and nx + 1 != self.x:
            cell_2 = (nx + 1, ny)
            distances[abs(cell_2[0] - x) ** 2 + abs(cell_2[1] - y) ** 2] = cell_2
        res = distances[min(distances.keys())]
        if nx == res[0]:
            if ny > res[1]:
                self.stored_direction = (0, -1)
            elif ny < res[1]:
                self.stored_direction = (0, 1)
        elif ny == res[1]:
            if nx > res[0]:
                self.stored_direction = (-1, 0)
            if nx < res[0]:
                self.stored_direction = (1, 0)
        
    def move(self):
        if (self.x, self.y) == (-1, 17):
            self.rect = self.rect.move(28 * 16, 0)
        elif (self.x, self.y) == (28, 17):
            self.rect = self.rect.move(-28 * 16, 0)
        else:
            if (self.x + self.direction[0], self.y + self.direction[1]) in CROSSROADS_1:
                self.change_path(self.x + self.direction[0], self.y + self.direction[1])
            elif (self.x, self.y + self.direction[1]) in CROSSROADS_2 and self.direction[0] == 0:
                self.change_path(self.x + self.direction[0], self.y + self.direction[1])
            if (self.x, self.y) in CROSSROADS_1:
                if self.stored_direction and self.cell_rect.center == self.rect.center:
                    self.direction, self.stored_direction = self.stored_direction, None
            elif self.x + self.direction[0] < 28:
                if MAZE[self.y + self.direction[1]][self.x + self.direction[0]] == '#':
                    if self.cell_rect.center == self.rect.center:
                        if MAZE[self.y - 1][self.x] == '0' and self.direction[1] != 1:
                            self.direction = (0, -1)
                        elif MAZE[self.y][self.x - 1] == '0' and self.direction[0] != 1:
                            self.direction = (-1, 0)
                        elif MAZE[self.y + 1][self.x] == '0' and self.direction[1] != -1:
                            self.direction = (0, 1)
                        elif MAZE[self.y][self.x + 1] == '0' and self.direction[0] != -1:
                            self.direction = (1, 0)
        self.change_rotation()
        self.x = self.rect.center[0] // 16
        self.y = self.rect.center[1] // 16
        self.rect = self.rect.move(self.direction[0], self.direction[1])
        self.cell_rect = pygame.Rect(self.x * 16, self.y * 16, 16, 16)

    def change_rotation(self):
        vx, vy = self.direction[0], self.direction[1]
        if vx == 1:
            self.rotation = 'right'
        elif vx == -1:
            self.rotation = 'left'
        elif vy == 1:
            self.rotation = 'down'
        elif vy == -1:
            self.rotation = 'up'

    def change_sprite(self, flag=False):
        if self.animCount % 7 == 0:
            if self.sprite == 1:
                self.sprite = 0
                self.animCount = 0
            else:
                self.sprite += 1
            if self.color == 'blue':
                self.image = self.fright_blue[self.sprite]
                if flag:
                    self.color = 'white'
            elif self.color == 'white':
                self.image = self.fright_white[self.sprite]
                if flag:
                    self.color = 'blue'
            elif self.rotation == 'right':
                self.image = self.right[self.sprite]
            elif self.rotation == 'left':
                self.image = pygame.transform.flip(self.right[self.sprite], 1, 0)
            elif self.rotation == 'up':
                self.image = self.up[self.sprite]
            elif self.rotation == 'down':
                self.image = self.down[self.sprite]
        self.animCount += 1


class Blinky(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.start_cords = (x, y)
        self.right = [pygame.image.load('data/ghosts_sprites/blinky/RL1.png'),
                      pygame.image.load('data/ghosts_sprites/blinky/RL2.png')]
        self.down = [pygame.image.load('data/ghosts_sprites/blinky/D1.png'),
                     pygame.image.load('data/ghosts_sprites/blinky/D2.png')]
        self.up = [pygame.image.load('data/ghosts_sprites/blinky/U1.png'),
                   pygame.image.load('data/ghosts_sprites/blinky/U2.png')]

    def set_target_cell(self, pacman):
        super().set_target_cell(pacman)
        if self.state == 'chase':
            self.target_cell = pacman.x, pacman.y
        elif self.state == 'scattering':
            self.target_cell = (27, 3)


    def change_path(self, nx, ny):
        super().change_path(nx, ny)

    def move(self):
        super().move()

    def change_rotation(self):
        super().change_rotation()

    def change_sprite(self, flag=False):
        super().change_sprite(flag)


class Pinky(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.start_cords = (x, y)
        self.right = [pygame.image.load('data/ghosts_sprites/pinky/RL1.png'),
                      pygame.image.load('data/ghosts_sprites/pinky/RL2.png')]
        self.down = [pygame.image.load('data/ghosts_sprites/pinky/D1.png'),
                     pygame.image.load('data/ghosts_sprites/pinky/D2.png')]
        self.up = [pygame.image.load('data/ghosts_sprites/pinky/U1.png'),
                   pygame.image.load('data/ghosts_sprites/pinky/U2.png')]

    def set_target_cell(self, pacman):
        super().set_target_cell(pacman)
        if self.state == 'chase':
            self.target_cell = (pacman.x + pacman.direction[0] * 2, pacman.y + pacman.direction[1] * 2)
        elif self.state == 'scattering':
            self.target_cell = (0, 3)

    def change_path(self, nx, ny):
        super().change_path(nx, ny)

    def move(self):
        super().move()

    def change_rotation(self):
        super().change_rotation()

    def change_sprite(self, flag=False):
        super().change_sprite(flag)



class Inky(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.start_cords = (x, y)
        self.right = [pygame.image.load('data/ghosts_sprites/inky/RL1.png'),
                      pygame.image.load('data/ghosts_sprites/inky/RL2.png')]
        self.down = [pygame.image.load('data/ghosts_sprites/inky/D1.png'),
                     pygame.image.load('data/ghosts_sprites/inky/D2.png')]
        self.up = [pygame.image.load('data/ghosts_sprites/inky/U1.png'),
                   pygame.image.load('data/ghosts_sprites/inky/U2.png')]

    def set_target_cell(self, pacman):
        super().set_target_cell(pacman)
        if self.state == 'chase':
            if pacman.direction[0] != 0:
                if self.y < pacman.y:
                    y = self.y - (pacman.y - self.y) * 2
                elif self.y > pacman.y:
                    y = self.y + (self.y - pacman.y) * 2
                else:
                    y = pacman.y
                x = pacman.x + pacman.direction[0]
            elif pacman.direction[1] != 0:
                if self.x < pacman.x:
                    x = self.x - (pacman.x - self.x) * 2
                elif self.x > pacman.x:
                    x = self.x + (self.x - pacman.x) * 2
                else:
                    x = pacman.x
                y = pacman.y + pacman.direction[1]
            else:
                x, y = pacman.x, pacman.y
            if y < 3:
                y = 3
            elif y > 33:
                y = 33
            if x < 0:
                x = 0
            elif x > 27:
                x = 27
            self.target_cell = (x, y)
        elif self.state == 'scattering':
            self.target_cell= (27, 33)

    def change_path(self, nx, ny):
        super().change_path(nx, ny)

    def move(self):
        super().move()

    def change_rotation(self):
        super().change_rotation()

    def change_sprite(self, flag=False):
        super().change_sprite(flag)

class Clyde(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.start_cords = (x, y)
        self.right = [pygame.image.load('data/ghosts_sprites/clyde/RL1.png'),
                      pygame.image.load('data/ghosts_sprites/clyde/RL2.png')]
        self.down = [pygame.image.load('data/ghosts_sprites/clyde/D1.png'),
                     pygame.image.load('data/ghosts_sprites/clyde/D2.png')]
        self.up = [pygame.image.load('data/ghosts_sprites/clyde/U1.png'),
                   pygame.image.load('data/ghosts_sprites/clyde/U2.png')]

    def set_target_cell(self, pacman):
        super().set_target_cell(pacman)
        if sqrt((self.x - pacman.x) ** 2 + (self.y - pacman.y) ** 2) > 8:
            self.target_cell = (pacman.x, pacman.y)
            self.state = 'chase'
        elif self.state == 'scattering':
            self.target_cell = (0, 33)

    def change_path(self, nx, ny):
        super().change_path(nx, ny)

    def move(self):
        super().move()

    def change_rotation(self):
        super().change_rotation()

    def change_sprite(self, flag=False):
        super().change_sprite(flag)
