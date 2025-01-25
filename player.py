import pygame
from constants import GRAVITY, SCREEN_HEIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (400, SCREEN_HEIGHT - 10)
        self.velocity = 0
        self.speed = 5
        self.bubbles = []
        self.max_bubbles = 2

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

    def jump(self):
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.velocity = -12

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
