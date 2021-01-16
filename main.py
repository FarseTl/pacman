import pygame
from constants import *
from pacman import *
from ghost import *
from time import time

class Game:
    def __init__(self):
        self.state = 'title screen'
        self.score = 0
        self.wave = 1
        self.mode = 'scattering'
        self.prev_mode = None

        self.ghost_color = 'blue'
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.bg = pygame.image.load('data/bg.png')
        self.start_time = time()

        self.pacman = Pacman(13, 26)
        self.blinky = Blinky(9, 17)
        self.pinky = Pinky(11, 14)
        self.inky = Inky(18, 16)
        self.clyde = Clyde(13, 20)

        self.blinky.set_target_cell(self.pacman)
        self.inky.set_target_cell(self.pacman)
        self.clyde.set_target_cell(self.pacman)
        self.pinky.set_target_cell(self.pacman)

        self.dots_pos = []
        with open('data/maze_dots.txt', 'r') as maze:
            maze = list(map(lambda x: list(x.strip()), maze.readlines()))
        for i in range(3, len(maze) - 3):
            for j in range(len(maze[0])):
                if maze[i][j] == '.':
                    self.dots_pos.append((j, i))
        self.enegizers_pos = [(1, 26), (26, 26), (1, 6), (26, 6)]

    def update(self):
        self.draw_coins()
        self.pacman.move()
        self.pacman.change_sprite()
        for ghost in enemies:
            ghost.move()
            ghost.set_target_cell(self.pacman)
            if self.mode != 'frightening':
                ghost.change_sprite()
            else:
                if 10 > time() - self.start_time >= 8:
                    ghost.change_sprite(True)
                else:
                    ghost.change_sprite()
        self.eat_dot()
        self.eat_enegizer()
        self.eat_pacman_or_ghost()
        all_sprites.draw(self.screen)

    def draw_coins(self):
        for cords in self.dots_pos:
            pygame.draw.circle(self.screen, (255, 255, 0), (cords[0] * 16 + 9, cords[1] * 16 + 9), 2)
        for cords in self.enegizers_pos:
            pygame.draw.circle(self.screen, (255, 255, 0), (cords[0] * 16 + 9, cords[1] * 16 + 9), 6)

    def eat_dot(self):
        if (self.pacman.x, self.pacman.y) in self.dots_pos:
            del self.dots_pos[self.dots_pos.index((self.pacman.x, self.pacman.y))]
            self.score += 1

    def eat_enegizer(self):
        if (self.pacman.x, self.pacman.y) in self.enegizers_pos:
            del self.enegizers_pos[self.enegizers_pos.index((self.pacman.x, self.pacman.y))]
            for ghost in enemies:
                ghost.direction = (ghost.direction[0] * (-1), ghost.direction[1] * (-1))
            if self.mode != 'frightening':
                self.prev_mode = self.mode
            self.mode = 'frightening'
            self.start_time = time()
            self.change_ghosts_state()
            for ghost in enemies:
                ghost.color = 'blue'

    def eat_pacman_or_ghost(self):
        if self.mode != 'frightening':
            for ghost in enemies:
                if (ghost.x, ghost.y) == (self.pacman.x, self.pacman.y):
                    self.pacman.lives -= 1
        else:
            for ghost in enemies:
                if (ghost.x, ghost.y) == (self.pacman.x, self.pacman.y):
                    ghost.x, ghost.y = ghost.start_cords
                    ghost.rect = pygame.Rect(ghost.x * 16, ghost.y * 16, 16, 16)

    def change_mode(self):
        if self.mode != 'frightening':
            if self.wave == 1 or self.wave == 3:
                if time() - self.start_time >= 7:
                    self.start_time = time()
                    self.wave += 1
                    self.mode = 'chase'
            elif self.wave in (2, 4, 6):
                if time() - self.start_time >= 20:
                    self.start_time = time()
                    self.wave += 1
                    self.mode = 'scattering'
            elif self.wave == 5:
                if time() - self.start_time >= 5:
                    self.start_time = time()
                    self.wave += 1
                    self.mode = 'chase'
            elif self.wave == 7:
                if time() - self.start_time >= 5:
                    self.start_time = None
                    self.mode = 'chase'
            self.change_ghosts_state()
        else:
            if time() - self.start_time >= 10:
                self.start_time = time()
                self.mode = self.prev_mode
                self.change_ghosts_state()
                for ghost in enemies:
                    ghost.color = None

    def change_ghosts_state(self):
        for ghost in enemies:
            ghost.state = self.mode

    def terminate(self):
        pygame.quit()
        exit()

    def main_loop(self):
        while True:
            self.clock.tick(FPS)
            self.screen.blit(self.bg, (0, 0))
            if self.start_time:
                self.change_mode()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.terminate()
                    if event.key == pygame.K_LEFT:
                        self.pacman.next_rotation = 'left'
                        self.pacman.change_direction(-2, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.pacman.next_rotation = 'right'
                        self.pacman.change_direction(2, 0)
                    elif event.key == pygame.K_UP:
                        self.pacman.next_rotation = 'up'
                        self.pacman.change_direction(0, -2)
                    elif event.key == pygame.K_DOWN:
                        self.pacman.next_rotation = 'down'
                        self.pacman.change_direction(0, 2)
            self.update()
            pygame.display.flip()


Game().main_loop()