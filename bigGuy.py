import pygame
from constants import SCREEN_HEIGHT



class BigGuy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((60, 80))
        self.image.fill((255, 165, 0))
        self.rect = self.image.get_rect(bottomleft=(10, SCREEN_HEIGHT))


