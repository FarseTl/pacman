import pygame
from constants import *
from pacman import *
from ghost import *
from maze import *


class Game:
    def __init__(self):
        self.state = 'title screen'
        self.score = 0

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.bg = pygame.image.load('data/bg.png')

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
        for ghost in enemies:
            ghost.move()
            ghost.set_target_cell(self.pacman)
        self.eat_dot()
        self.eat_enegizer()
        self.eat_pacman()
        all_sprites.draw(self.screen)

    def draw_coins(self):
        for cords in self.dots_pos:
            pygame.draw.circle(self.screen, (0, 128, 0), (cords[0] * 16 + 8, cords[1] * 16 + 8), 4)
        for cords in self.enegizers_pos:
            pygame.draw.circle(self.screen, (0, 128, 0), (cords[0] * 16 + 8, cords[1] * 16 + 8), 8)

    def eat_dot(self):
        if (self.pacman.x, self.pacman.y) in self.dots_pos:
            del self.dots_pos[self.dots_pos.index((self.pacman.x, self.pacman.y))]
            self.score += 1

    def eat_enegizer(self):
        if (self.pacman.x, self.pacman.y) in self.enegizers_pos:
            del self.enegizers_pos[self.enegizers_pos.index((self.pacman.x, self.pacman.y))]

    def eat_pacman(self):
        for ghost in enemies:
            if (ghost.x, ghost.y) == (self.pacman.x, self.pacman.y):
                self.pacman.lives -= 1
                print(self.pacman.lives)

    def terminate(self):
        pygame.quit()
        exit()

    def main_loop(self):
        while True:
            self.clock.tick(FPS)
            self.screen.blit(self.bg, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.terminate()
                    if event.key == pygame.K_LEFT:
                        self.pacman.change_direction(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.pacman.change_direction(1, 0)
                    elif event.key == pygame.K_UP:
                        self.pacman.change_direction(0, -1)
                    elif event.key == pygame.K_DOWN:
                        self.pacman.change_direction(0, 1)
            self.update()
            pygame.display.flip()


Game().main_loop()