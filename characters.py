import pygame
from blade import Blade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class EvilGuy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((128, 0, 128))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2))
        self.direction = 1

    def update(self):
        self.rect.y += self.direction * 3
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.direction *= -1

    def shoot_blade(self):
        return Blade(self.rect.centerx, self.rect.centery)

class FatGuy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((60, 80))
        self.image.fill((255, 165, 0))
        self.rect = self.image.get_rect(bottomleft=(10, SCREEN_HEIGHT))
        self.timer = 500

    def update(self):
        self.timer -= 1
