import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAVITY = 0.3
LIFT = -8
BASE_BLADE_SPEED = 5
BALLOON_SPEED = 7
BASE_BALLOON_SIZE = (30, 40)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Balloon Dodge")
clock = pygame.time.Clock()

class Balloon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.base_image = pygame.Surface(BASE_BALLOON_SIZE)
        self.base_image.fill((255, 0, 0))
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

class Blade(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(
            center=(SCREEN_WIDTH + 50, random.randint(50, SCREEN_HEIGHT-50))
        )
        self.passed = False
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

class ZigzagBlade(Blade):
    def __init__(self, speed):
        super().__init__(speed)
        self.image.fill((255, 165, 0))  # Orange
        self.angle = 0
        self.amplitude = 50
        self.frequency = 0.1

    def update(self):
        super().update()
        self.angle += self.frequency
        self.rect.y += math.sin(self.angle) * 3
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))

class SplitBlade(Blade):
    def __init__(self, speed):
        super().__init__(speed)
        self.image.fill((0, 255, 0))  # Green
        self.has_split = False
        self.split_position = SCREEN_WIDTH - 500  # Split at x=300

    def update(self):
        super().update()
        if not self.has_split and self.rect.x < self.split_position:
            # Create two new blades with position constraints
            blade1 = Blade(self.speed)
            blade1.rect = self.rect.copy()
            blade1.rect.y = min(SCREEN_HEIGHT - blade1.rect.height, self.rect.y + 40)
            
            blade2 = Blade(self.speed)
            blade2.rect = self.rect.copy()
            blade2.rect.y = max(0, self.rect.y - 40)
            
            all_sprites.add(blade1, blade2)
            blades.add(blade1, blade2)
            self.has_split = True
            self.kill()

def initialize_game():
    global balloon, all_sprites, blades, score, game_over, previous_level, blade_counter, split_level
    balloon = Balloon()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(balloon)
    blades = pygame.sprite.Group()
    score = 0
    game_over = False
    previous_level = 0
    blade_counter = 0
    split_level = 0  # Track 15-point intervals

# Game initialization
initialize_game()
font = pygame.font.Font(None, 36)
BLADE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(BLADE_EVENT, 1500)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == BLADE_EVENT and not game_over:
            current_level = score // 25
            blade_speed = BASE_BLADE_SPEED * (1.05 ** current_level)
            
            # Check for special blades
            blade_counter += 1
            current_split_level = score // 15
            
            if current_split_level > split_level:
                # Spawn split blade for every 15 points
                new_blade = SplitBlade(blade_speed)
                split_level = current_split_level
            elif blade_counter % 7 == 0:
                # Every 7th blade is zigzag
                new_blade = ZigzagBlade(blade_speed)
            else:
                # Regular blade
                new_blade = Blade(blade_speed)
            
            all_sprites.add(new_blade)
            blades.add(new_blade)

    keys = pygame.key.get_pressed()
    
    if not game_over:
        # Handle controls
        if keys[pygame.K_SPACE]:
            balloon.lift()
        if keys[pygame.K_LEFT]:
            balloon.move_left()
        if keys[pygame.K_RIGHT]:
            balloon.move_right()

        # Update game state
        all_sprites.update()

        # Score counting
        for blade in blades:
            if not blade.passed and blade.rect.right < balloon.rect.left:
                score += 1
                blade.passed = True

        # Progressive difficulty
        current_level = score // 25
        if current_level > previous_level:
            balloon.update_scale(1.05 ** current_level)
            previous_level = current_level

        # Collision detection
        if pygame.sprite.spritecollide(balloon, blades, True):
            game_over = True

    else:
        if keys[pygame.K_SPACE]:
            initialize_game()

    # Drawing
    screen.fill(WHITE)
    all_sprites.draw(screen)

    if game_over:
        game_over_text = font.render("GAME OVER", True, BLACK)
        score_text = font.render(f"Final Score: {score}", True, BLACK)
        restart_text = font.render("PRESS SPACE TO TRY AGAIN", True, BLACK)
        
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 50))
        screen.blit(score_text, (SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2))
        screen.blit(restart_text, (SCREEN_WIDTH//2 - 160, SCREEN_HEIGHT//2 + 50))
    else:
        score_text = font.render(f"SCORE: {score}", True, BLACK)
        high_text = font.render("HIGH SCORE: 0", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(high_text, (10, 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()