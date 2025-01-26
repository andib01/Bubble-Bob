import random
import pygame

from blade import Blade
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, WHITE


class BladeGuy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/svenolai.png")
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2))
        self.direction = 1
        self.speed = 3  # Base speed for movement
        self.change_direction_timer = 0  # Timer for changing direction
        self.hp = 3
        self.speed_boost = False 

    def update(self):
        # Randomly change direction and speed every 30 frames
        if self.change_direction_timer <= 0:
            self.direction = random.choice([-1, 1])  # Randomly choose up or down
            if self.speed_boost:
                self.speed = random.randint(5, 10)  # Increased speed range
            else:
                self.speed = random.randint(2, 5)
            # self.speed = random.randint(2, 5)  # Random speed between 2 and 5
            self.change_direction_timer = random.randint(30, 60)  # Random time for next direction change

        self.rect.y += self.direction * self.speed
        self.change_direction_timer -= 1  # Decrease timer

        # Prevent BladeGuy from moving off-screen
        if self.rect.top < 0:
            self.rect.top = 0  # Clamp position to the top
            self.direction = 1  # Move downward
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT  # Clamp position to the bottom
            self.direction = -1  # Move upward

    def shoot_blade(self):
        return Blade(self.rect.centerx, self.rect.centery)
    def increase_speed(self):
        """Increase Blade Guy's movement speed."""
        self.speed_boost = True