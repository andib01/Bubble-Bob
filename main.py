import pygame
import sys
from ballon import Balloon
from blade import Blade
from zigzag_blade import ZigzagBlade
from split_blade import SplitBlade
from constants import *

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Balloon Dodge")
clock = pygame.time.Clock()

def initialize_game():
    global balloon, all_sprites, blades, score, game_over, previous_level, split_level, zigzag_level
    balloon = Balloon()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(balloon)
    blades = pygame.sprite.Group()
    score = 0
    game_over = False
    previous_level = 0
    split_level = 0
    zigzag_level = 0

# Game initialization
initialize_game()
font = pygame.font.Font(None, 36)
BLADE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(BLADE_EVENT, 1500)

# Bottom wall settings
WALL_HEIGHT = int(SCREEN_HEIGHT * 0.05)
wall_top = SCREEN_HEIGHT - WALL_HEIGHT

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == BLADE_EVENT and not game_over:
            current_level = score // 25
            blade_speed = BASE_BLADE_SPEED * (1.05 ** current_level)
            
            current_split = score // 15
            current_zigzag = score // 7

            if current_split > split_level:
                new_blade = SplitBlade(blade_speed)
                all_sprites.add(new_blade)
                blades.add(new_blade)
                split_level = current_split
            elif current_zigzag > zigzag_level:
                zigzag1 = ZigzagBlade(blade_speed)
                zigzag2 = ZigzagBlade(blade_speed)
                all_sprites.add(zigzag1, zigzag2)
                blades.add(zigzag1, zigzag2)
                zigzag_level = current_zigzag
            else:
                new_blade = Blade(blade_speed)
                all_sprites.add(new_blade)
                blades.add(new_blade)

    keys = pygame.key.get_pressed()
    
    if not game_over:
        # Controls
        if keys[pygame.K_SPACE]:
            balloon.lift()
        if keys[pygame.K_LEFT]:
            balloon.move_left()
        if keys[pygame.K_RIGHT]:
            balloon.move_right()

        # Update game state
        all_sprites.update()

        # Bottom wall collision
        if balloon.rect.bottom >= wall_top:
            game_over = True

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
    
    # Draw bottom wall
    pygame.draw.rect(screen, RED, (0, wall_top, SCREEN_WIDTH, WALL_HEIGHT))

    # UI Elements
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
