import pygame
import sys
import random
from bigGuy import BigGuy
from bladeGuy import BladeGuy
from player import Player
from bubble import Bubble

from constants import *

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BubbleZilla")
clock = pygame.time.Clock()

def initialize_game():
    global player, bubbles, blades, all_sprites, fat_guy, evil_guy, game_over, score
    player = Player()
    fat_guy = BigGuy()
    evil_guy = BladeGuy()
    bubbles = pygame.sprite.Group()
    blades = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(player, fat_guy, evil_guy)
    game_over = False
    score = 0

# Game initialization
initialize_game()
font = pygame.font.Font(None, 36)
BUBBLE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(BUBBLE_EVENT, 1000)  # Spawn a bubble every second
allowed_spawn_areas = [
    (50, SCREEN_WIDTH - 80 - 50)  
]
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == BUBBLE_EVENT and not game_over:
            x_position = random.randint(*allowed_spawn_areas[0])
            
            # Create and add the bubble
            bubble = Bubble(x_position, 0)
            all_sprites.add(bubble)
            bubbles.add(bubble)

    keys = pygame.key.get_pressed()

    if not game_over:
        # Controls
       
        player.move(keys)

        # Update game state
        all_sprites.update()

        # Collision: Player collects bubbles
        for bubble in pygame.sprite.spritecollide(player, bubbles, True):
            if len(player.bubbles) < player.max_bubbles:
                player.bubbles.append(bubble)

        # Collision: Blades destroy bubbles
        for bubble in player.bubbles[:]:
            if pygame.sprite.spritecollideany(bubble, blades):
                player.bubbles.remove(bubble)
                bubble.kill()

        # Feed Fat Guy
        if len(player.bubbles) == 2 and pygame.sprite.collide_rect(player, fat_guy):
            player.bubbles.clear()  # Empty the player's hand
            score += 1  # Increment score only when the Fat Guy is fed

        # Blade shooting from Evil Guy
        if random.random() < 0.02:  # Adjust frequency
            blade = evil_guy.shoot_blade()
            all_sprites.add(blade)
            blades.add(blade)

        # Check win condition
        if score >= 10:  # Win condition: feed Fat Guy 10 times
            print("You win!")
            running = False

    else:
        if keys[pygame.K_p]:
            initialize_game()

    # Drawing
    screen.fill(WHITE)
    pygame.draw.line(screen,BLACK, (SCREEN_WIDTH - 80, 0), (SCREEN_WIDTH - 80, SCREEN_HEIGHT), 2)
    all_sprites.draw(screen)

    # UI Elements
    if game_over:
        game_over_text = font.render("GAME OVER", True, BLACK)
        restart_text = font.render("PRESS P TO RESTART", True, BLACK)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 10))
    else:
        score_text = font.render(f"SCORE: {score}", True, BLACK)
        screen.blit(score_text, (10, 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
