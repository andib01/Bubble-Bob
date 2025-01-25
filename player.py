import pygame
from constants import GRAVITY, SCREEN_HEIGHT, SCREEN_WIDTH

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (400, SCREEN_HEIGHT - 10)
        self.velocity = 0
        self.speed = 5
        self.jumping = 0
        self.bubbles = []
        self.max_bubbles = 2

    def move(self, keys):

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.jump()

        # Keep the player within screen boundaries
        self.rect.x = max(0, min(SCREEN_WIDTH - 80-self.rect.width, self.rect.x))

    def jump(self):
        if self.jumping == 0:
            self.velocity = -10
            self.jumping = 1
        elif self.jumping == 1 and self.velocity > 0:
            self.velocity = -6
            self.jumping = 2

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.jumping = 0
