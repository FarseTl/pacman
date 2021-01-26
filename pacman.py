import pygame
from constants import *


class Pacman(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.lives = 0
        self.direction = (-2, 0)
        self.rotation = 'left'
        self.next_rotation = None
        self.x, self.y = x, y
        self.rect = pygame.Rect(self.x * 16, self.y * 16, 16, 16)
        self.stored_direction = None
        self.cell_rect = pygame.Rect(self.x * 16, self.y * 16, 16, 16)

        self.sprites = [pygame.image.load('data/pacman_sprites/pacman_1.png'),
                        pygame.image.load('data/pacman_sprites/pacman_2.png'),
                        pygame.image.load('data/pacman_sprites/pacman_3.png')]
        self.image = self.sprites[0]
        self.sprite = 0
        self.animCount = 0

    def change_direction(self, vx, vy):
        self.stored_direction = (vx, vy)

    def can_move(self):
        if self.cell_rect.center == self.rect.center:
            if self.stored_direction:
                    self.direction = self.stored_direction
                    self.stored_direction = None
            if self.x + 1 < 28:
                if MAZE[self.y + self.direction[1] // 2][self.x + self.direction[0] // 2] == '#':
                    return False
                else:
                    return True
        return True

    def move(self):
        if self.can_move():
            pygame.mixer.music.unpause()
            self.change_rotation()
            self.x = self.rect.center[0] // 16
            self.y = self.rect.center[1] // 16
            self.cell_rect = pygame.Rect(self.x * 16, self.y * 16, 16, 16)
            self.rect = self.rect.move(self.direction[0], self.direction[1])
            if (self.x, self.y) == (-1, 17):
                self.rect = self.rect.move(28 * 16, 0)
            elif (self.x, self.y) == (28, 17):
                self.rect = self.rect.move(-28 * 16, 0)

    def change_rotation(self):
        if self.next_rotation != self.rotation and self.next_rotation is not None:
            self.rotation = self.next_rotation
            self.next_rotation = None

    def change_sprite(self):
        if self.animCount % 7 == 0:
            if self.sprite == 2:
                self.sprite = 0
                self.animCount = 0
            elif self.can_move():
                self.sprite += 1
            if self.rotation == 'right':
                self.image = self.sprites[self.sprite]
            elif self.rotation == 'left':
                self.image = self.sprites[self.sprite]
                self.image = pygame.transform.flip(self.image, 1, 0)
            elif self.rotation == 'up':
                self.image = self.sprites[self.sprite]
                self.image = pygame.transform.rotate(self.image, 90)
            elif self.rotation == 'down':
                self.image = self.sprites[self.sprite]
                self.image = pygame.transform.rotate(self.image, 270)
        self.animCount += 1
