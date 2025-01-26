import pygame
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Bubble(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.original_image = pygame.image.load("assets/bubble.png").convert_alpha()
        self.original_image = pygame.transform.smoothscale(self.original_image, (50, 50))

        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = random.randint(3, 6)
        self.angle = 0


        self.image.set_alpha(180)

    def update(self):
        self.rect.y += self.speed
        
        self.angle += 1
        old_center = self.rect.center
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=old_center)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
