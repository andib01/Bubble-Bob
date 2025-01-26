import pygame
from constants import SCREEN_HEIGHT
from fightBubble import FightBubble
from utils import graphics_helper

class BigGuy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.images = {
            "idle": pygame.image.load("assets/big_guy/idle.png").convert_alpha(),
            "eat1": pygame.image.load("assets/big_guy/eat_1.png").convert_alpha(),
            "eat2": pygame.image.load("assets/big_guy/eat_2.png").convert_alpha(),
            "eat3": pygame.image.load("assets/big_guy/eat_3.png").convert_alpha(),
            "eat4": pygame.image.load("assets/big_guy/eat_4.png").convert_alpha(),
        }
        graphics_helper.scale_surfaces(self.images, 120)

        self.image = pygame.Surface((120, 120), pygame.SRCALPHA)

        self.current_state = "idle"
        self.image = self.images[self.current_state]
        self.rect = self.image.get_rect(bottomleft=(5, SCREEN_HEIGHT))
        self.bubble_active = False
        self.bubble_cooldown = 0  # Cooldown timer in milliseconds
        self.angle = 0
        self.update()

    def update(self):
        self.angle += 1
        if self.angle >= 360:
            self.angle = 0
        self.image = pygame.transform.rotate(self.images[self.current_state], self.angle)
        bottomleft = self.rect.bottomleft
        self.rect = self.image.get_rect()
        self.rect.bottomleft = bottomleft
        self.speed = 4
        self.hp = 3

    def eat(self, bubble_count):
        if bubble_count == 4:
            self.current_state = "eat1"
        elif bubble_count == 6:
            self.current_state = "eat2"
        elif bubble_count == 10:
            self.current_state = "eat3"
        elif bubble_count == 12:
            self.current_state = "eat4"

        # TODO: Add sound effect for eating: e.g. burping sound

        # Update the displayed image
        self.image = self.images[self.current_state]

        # Update rect so sprite doesn't shift if image size changes
        bottomleft = self.rect.bottomleft
        self.rect = self.image.get_rect()
        self.rect.bottomleft = bottomleft

    def move(self, keys):
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Keep within bounds
        self.rect.y = max(0, min(SCREEN_HEIGHT - self.rect.height, self.rect.y))

    def shoot_bubble(self, current_time):
        if current_time >= self.bubble_cooldown:  # Check if cooldown has passed
            self.bubble_active = True
            self.bubble_cooldown = current_time + 500  # 500ms cooldown
            return FightBubble(self.rect.right, self.rect.centery)
        return None
