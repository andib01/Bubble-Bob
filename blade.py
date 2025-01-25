import pygame
import random
from constants import BLUE, SCREEN_WIDTH, SCREEN_HEIGHT

class Blade(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(
            center=(SCREEN_WIDTH + 50, random.randint(50, SCREEN_HEIGHT - 50))
        )
        self.passed = False
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()
