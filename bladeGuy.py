import random
import pygame

from blade import Blade
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, WHITE


class BladeGuy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/svenolai.png")
        self.image = pygame.transform.scale(self.image, (75,75)) 
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2))
        self.direction = 1
        self.speed = 3  # Base speed for movement
        self.change_direction_timer = 0  # Timer for changing direction

    def update(self):
        # Randomly change direction and speed every 30 frames
        if self.change_direction_timer <= 0:
            self.direction = random.choice([-1, 1])  # Randomly choose up or down
            self.speed = random.randint(2, 5)  # Random speed between 2 and 5
            self.change_direction_timer = random.randint(30, 60)  # Random time for next direction change

        self.rect.y += self.direction * self.speed
        self.change_direction_timer -= 1  # Decrease timer

        # Prevent BladeGuy from moving off-screen
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.direction *= -1  # Reverse direction to stay in bounds

    def shoot_blade(self):
        return Blade(self.rect.centerx, self.rect.centery)