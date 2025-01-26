import pygame
from constants import BLUE, SCREEN_WIDTH


class FightBubble(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.image.load("assets/bubble.png").convert_alpha()
        self.original_image = pygame.transform.smoothscale(self.original_image, (50, 50))

        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > SCREEN_WIDTH:
            self.kill()