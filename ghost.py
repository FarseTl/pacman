import pygame
from constants import *
from math import sqrt


class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.x, self.y = x, y
        self.add(enemies)
        self.target_cell = None
        self.direction = (0, 1)
        self.stored_direction = None
        self.image = pygame.Surface((16, 16))
        self.rect = pygame.Rect(self.x * 16, self.y * 16, 16, 16)
        self.cell_rect = pygame.Rect(self.x * 16, self.y * 16, 16, 16)
        self.mode = 'chase'

    def set_target_cell(self, pacman):
        pass

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
        self.x = self.rect.center[0] // 16
        self.y = self.rect.center[1] // 16
        self.rect = self.rect.move(self.direction[0], self.direction[1])
        self.cell_rect = pygame.Rect(self.x * 16, self.y * 16, 16, 16)


class Blinky(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y)
        pygame.draw.rect(self.image, pygame.Color('Red'),
                        (0, 0, 16, 16))

    def set_target_cell(self, pacman):
        self.target_cell = pacman.x, pacman.y

    def change_path(self, nx, ny):
        super().change_path(nx, ny)

    def move(self):
        super().move()


class Pinky(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y)
        pygame.draw.rect(self.image, pygame.Color('Pink'),
                        (0, 0, 16, 16))

    def set_target_cell(self, pacman):
        self.target_cell = (pacman.x + pacman.direction[0] * 4, pacman.y + pacman.direction[1] * 4)

    def change_path(self, nx, ny):
        super().change_path(nx, ny)

    def move(self):
        super().move()


class Inky(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y)
        pygame.draw.rect(self.image, pygame.Color('Blue'),
                        (0, 0, 16, 16))

    def set_target_cell(self, pacman):
        if pacman.direction[0] != 0:
            if self.y < pacman.y:
                y = self.y - (pacman.y - self.y) * 2
            elif self.y > pacman.y:
                y = self.y + (self.y - pacman.y) * 2
            else:
                y = pacman.y
            x = pacman.x + pacman.direction[0] * 2
        elif pacman.direction[1] != 0:
            if self.x < pacman.x:
                x = self.x - (pacman.x - self.x) * 2
            elif self.x > pacman.x:
                x = self.x + (self.x - pacman.x) * 2
            else:
                x = pacman.x
            y = pacman.y + pacman.direction[1] * 2
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

    def change_path(self, nx, ny):
        super().change_path(nx, ny)

    def move(self):
        super().move()


class Clyde(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y)
        pygame.draw.rect(self.image, pygame.Color('Green'),
                        (0, 0, 16, 16))

    def set_target_cell(self, pacman):
        if sqrt((self.x - pacman.x) ** 2 + (self.y - pacman.y) ** 2) > 8:
            self.target_cell = (pacman.x, pacman.y)
            self.mode = 'chase'
        else:
            self.target_cell = (0, 35)

    def change_path(self, nx, ny):
        super().change_path(nx, ny)

    def move(self):
        super().move()