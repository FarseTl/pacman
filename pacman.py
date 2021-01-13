import pygame
from constants import *


class Pacman(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.lives = 3
        self.direction = (-1, 0)
        self.x, self.y = x, y
        self.image = pygame.Surface((16, 16))
        pygame.draw.rect(self.image, pygame.Color('Yellow'),
                        (0, 0, 16, 16))
        self.rect = pygame.Rect(self.x * 16, self.y * 16, 16, 16)
        self.stored_direction = None
        self.cell_rect = pygame.Rect(self.x * 16, self.y * 16, 16, 16)

    def change_direction(self, vx, vy):
        self.stored_direction = (vx, vy)

    def can_move(self):
        if self.cell_rect.center == self.rect.center:
            if self.stored_direction:
                    self.direction = self.stored_direction
                    self.stored_direction = None
            if self.x + 1 < 28:
                if MAZE[self.y + self.direction[1]][self.x + self.direction[0]] == '#':
                    self.direction = (0, 0)
                    return False
                else:
                    return True
        return True

    def move(self):
        if self.can_move():
            self.x = self.rect.center[0] // 16
            self.y = self.rect.center[1] // 16
            self.cell_rect = pygame.Rect(self.x * 16, self.y * 16, 16, 16)
            self.rect = self.rect.move(self.direction[0], self.direction[1])
            if (self.x, self.y) == (-1, 17):
                self.rect = self.rect.move(28 * 16, 0)
            elif (self.x, self.y) == (28, 17):
                self.rect = self.rect.move(-28 * 16, 0)
