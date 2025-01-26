import pygame
from constants import SCREEN_WIDTH

class Blade(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.image.load("assets/blade.png").convert_alpha()
        self.original_image = pygame.transform.smoothscale(self.original_image, (20, 20))

        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = 7
        self.angle = 0 

    def update(self):
        self.rect.x -= self.speed
        self.angle += 5
        old_center = self.rect.center
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=old_center)

        if self.rect.right < 0:
            self.kill()
