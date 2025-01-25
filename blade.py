import pygame
from constants import SCREEN_WIDTH

class Blade(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 7

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()
