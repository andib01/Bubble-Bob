import pygame
from constants import *

class Balloon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.base_image = pygame.Surface(BASE_BALLOON_SIZE)
        self.base_image.fill(RED)
        self.scale_factor = 1.0
        self.image = pygame.transform.scale(self.base_image, 
            (int(BASE_BALLOON_SIZE[0] * self.scale_factor), 
             int(BASE_BALLOON_SIZE[1] * self.scale_factor)))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.velocity = 0
        self.speed = BALLOON_SPEED

    def reset(self):
        self.scale_factor = 1.0
        self.image = pygame.transform.scale(self.base_image, 
            (int(BASE_BALLOON_SIZE[0] * self.scale_factor), 
             int(BASE_BALLOON_SIZE[1] * self.scale_factor)))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))

    def lift(self):
        self.velocity = LIFT

    def move_left(self):
        self.rect.x = max(0, self.rect.x - self.speed)

    def move_right(self):
        self.rect.x = min(SCREEN_WIDTH - self.rect.width, self.rect.x + self.speed)

    def update_scale(self, scale_factor):
        current_center = self.rect.center
        self.scale_factor = scale_factor
        self.image = pygame.transform.scale(self.base_image, 
            (int(BASE_BALLOON_SIZE[0] * scale_factor), 
             int(BASE_BALLOON_SIZE[1] * scale_factor)))
        self.rect = self.image.get_rect(center=current_center)
