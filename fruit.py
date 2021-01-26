from constants import *

class Fruit(pygame.sprite.Sprite):
    def __init__(self, sprite):
        super().__init__(fruit)
        self.image = pygame.image.load(sprite)
        self.rect = pygame.Rect(13 * 16 + 8, 20 * 16, 16, 16)
