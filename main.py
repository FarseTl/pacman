import pygame
from constants import *
from pacman import *
from ghost import *
from fruit import *
from time import time


class Game:
    def __init__(self):
        pygame.init()

        self.state = 'title screen'
        self.score = 0
        self.dots_eaten = 0
        self.wave = 1
        self.mode = 'scattering'
        self.prev_mode = None

        self.ghost_color = 'blue'
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.bg = pygame.image.load('data/bg.png')
        self.game_over_screen = pygame.image.load('data/game_over_screen.png')
        self.title_screen = pygame.image.load('data/title_screen.png')
        self.win_screen = pygame.image.load('data/you_win_screen.png')
        self.start_time = time()
        self.mult = 1
        self.fruit = None
        self.fruit_eaten_text = False
        self.text_timer = None

        self.eat_ghost_sound = pygame.mixer.Sound('data/sounds/eat_ghost.wav')
        self.eat_fruit_sound = pygame.mixer.Sound('data/sounds/eat_fruit.wav')
        self.game_over_sound = pygame.mixer.Sound('data/sounds/game_over.wav')
        self.eat_ghost_sound.set_volume(0.1)
        self.eat_fruit_sound.set_volume(0.1)

    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0]-text_size[0]//2
            pos[1] = pos[1]-text_size[1]//2
        screen.blit(text, pos)

    def draw_lives(self):
        for i in range(self.pacman.lives):
            self.screen.blit(self.pacman.sprites[self.pacman.sprite], (80 + 25 * i, 549))

    def create_characters(self):
        self.pacman = Pacman(13, 26)
        self.blinky = Blinky(13, 14)
        self.pinky = Pinky(11, 17)
        self.inky = Inky(13, 17)
        self.clyde = Clyde(16, 17)

        self.blinky.set_target_cell(self.pacman)
        self.inky.set_target_cell(self.pacman)
        self.clyde.set_target_cell(self.pacman)
        self.pinky.set_target_cell(self.pacman)

    def create_dots(self):
        self.dots_pos = []
        with open('data/maze_dots.txt', 'r') as maze:
            maze = list(map(lambda x: list(x.strip()), maze.readlines()))
        for i in range(3, len(maze) - 3):
            for j in range(len(maze[0])):
                if maze[i][j] == '.':
                    self.dots_pos.append((j, i))
        self.enegizers_pos = [(1, 26), (26, 26), (1, 6), (26, 6)]

    def create_fruit(self):
        if not self.fruit and self.dots_eaten == 70:
            self.fruit = Fruit('data/cherry.png')
        elif not self.fruit and self.dots_eaten == 170:
            self.fruit = Fruit('data/raspberry.png')

    def update(self):
        self.draw_coins()
        self.create_fruit()
        self.pacman.move()
        self.pacman.change_sprite()
        self.draw_text(f'SCORE:', self.screen, (5, 10), 20, (183, 36, 35), 'arial black')
        self.draw_text(str(self.score), self.screen, (95  , 10), 20, WHITE, 'arial black')
        self.draw_text(f'LIVES:', self.screen, (5, 544), 25, (183, 36, 35), 'roboto medium')
        self.draw_lives()
        for ghost in enemies:
            ghost.move()
            ghost.set_target_cell(self.pacman)
            if ghost.text_timer:
                if time() - ghost.text_timer > 0.8:
                    ghost.text_timer = None
                else:
                    self.draw_text(ghost.score_for_eating, self.screen, ghost.text_pos, 15, WHITE, 'arial black')
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
        fruit.draw(self.screen)
        all_sprites.draw(self.screen)
        if self.text_timer:
            if time() - self.text_timer > 0.8:
                self.text_timer = None
            else:
                self.draw_text('150', self.screen, (16 * 13 + 2, 16 * 20 - 5), 15, WHITE, 'arial black')

    def draw_coins(self):
        for cords in self.dots_pos:
            pygame.draw.circle(self.screen, (255, 255, 0), (cords[0] * 16 + 9, cords[1] * 16 + 9), 2)
        for cords in self.enegizers_pos:
            pygame.draw.circle(self.screen, (255, 255, 0), (cords[0] * 16 + 9, cords[1] * 16 + 9), 6)

    def eat_dot(self):
        if (self.pacman.x, self.pacman.y) in self.dots_pos:
            del self.dots_pos[self.dots_pos.index((self.pacman.x, self.pacman.y))]
            self.score += 1
            self.dots_eaten += 1
            if self.dots_eaten == 294:
                self.state = 'win'
                pygame.mixer.music.pause()
        elif self.fruit in fruit and (self.pacman.x, self.pacman.y) in ((13, 20), (14, 20)):
            self.eat_fruit_sound.play()
            self.fruit_eaten_text = True
            self.text_timer = time()
            self.fruit.kill()
            self.fruit = None
            self.score += 150

    def eat_enegizer(self):
        if (self.pacman.x, self.pacman.y) in self.enegizers_pos:
            del self.enegizers_pos[self.enegizers_pos.index((self.pacman.x, self.pacman.y))]
            for ghost in enemies:
                if MAZE[ghost.direction[0] * (-1)][ghost.direction[1] * (-1)] != '#': 
                    ghost.direction = (ghost.direction[0] * (-1), ghost.direction[1] * (-1))
            if self.mode != 'frightening':
                self.prev_mode = self.mode
            self.mult = 1
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
                    if self.pacman.lives <= 0:
                        self.state = 'game over'
                        pygame.mixer.music.pause()
                        self.game_over_sound.play()
                    else:
                        self.state = 'pause'
                        pygame.mixer.music.pause()
                        for char in all_sprites:
                            char.kill()
                        lives = self.pacman.lives
                        self.create_characters()
                        self.pacman.lives = lives
        else:
            for ghost in enemies:
                if (ghost.x, ghost.y) == (self.pacman.x, self.pacman.y):
                    self.eat_ghost_sound.play()
                    self.score += (300 * self.mult)
                    ghost.text_pos = (ghost.x * 16 - 5, ghost.y * 16 - 2)
                    ghost.score_for_eating = str(300 * self.mult)
                    self.draw_text(ghost.score_for_eating, self.screen, ghost.text_pos, 15, WHITE, 'arial black')
                    self.mult += 1
                    ghost.text_timer = time()
                    ghost.x, ghost.y = ghost.start_cords
                    ghost.rect = pygame.Rect(ghost.x * 16, ghost.y * 16, 16, 16)
                    ghost.flag = True
                    ghost.direction = (0, -1)

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
        self.create_characters()
        self.create_dots()
        while True:
            self.clock.tick(FPS)
            if self.state == 'playing':
                self.screen.blit(self.bg, (0, 0))
                if self.start_time:
                    self.change_mode()
                if self.mode != 'frightening':
                    for ghost in enemies:
                        ghost.set_free(self.dots_eaten)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.terminate()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.mixer.music.pause()
                            self.state = 'pause'
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
            elif self.state == 'game over':
                self.screen.blit(self.game_over_screen, (0, 0))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.terminate()
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                        self.restart_game()
            elif self.state == 'title screen':
                self.screen.blit(self.title_screen, (0, 0))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.terminate()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.state = 'playing'
                            pygame.mixer.music.load('data/sounds/music.mp3')
                            pygame.mixer.music.set_volume(0.1)
                            pygame.mixer.music.play(11)
            elif self.state == 'pause':
                self.screen.fill((0, 0, 0))
                self.draw_text(f'{self.pacman.lives}', self.screen, (120, 250), 30, WHITE, 'arial black')
                self.draw_text(' LIVES LEFT', self.screen, (140, 250), 30, (153, 36, 35), 'arial black')
                self.draw_text('PRESS SPACE TO CONTINUE', self.screen, (110, 350), 15, WHITE, 'arial black')
                self.draw_text(f'SCORE:', self.screen, (5, 10), 20, (183, 36, 35), 'arial black')
                self.draw_text(str(self.score), self.screen, (95  , 10), 20, WHITE, 'arial black')
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.terminate()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            pygame.mixer.music.unpause()
                            self.state = 'playing'
            elif self.state == 'win':
                self.screen.blit(self.win_screen,(0, 0))
                self.draw_text(f'SCORE:', self.screen, (5, 10), 20, (183, 36, 35), 'arial black')
                self.draw_text(str(self.score), self.screen, (95  , 10), 20, WHITE, 'arial black')
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.terminate()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            pygame.mixer.music.load('data/sounds/music.mp3')
                            pygame.mixer.music.set_volume(0.1)
                            pygame.mixer.music.play(11)
                            self.restart_game()
            pygame.display.flip()

    def restart_game(self):
        for char in all_sprites:
            char.kill()
        self.create_characters()
        self.create_dots()

        self.score = 0
        self.state = 'playing'


Game().main_loop()