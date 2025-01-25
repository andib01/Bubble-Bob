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
pygame.display.set_caption("Bubble Chaos")
clock = pygame.time.Clock()

def initialize_game():
    global player, bubblesFalling, blades, all_sprites, fat_guy, evil_guy, game_over, score, hp
    player = Player()
    fat_guy = BigGuy()
    evil_guy = BladeGuy()
    bubblesFalling = pygame.sprite.Group()
    blades = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(player, fat_guy, evil_guy)
    game_over = False
    score = 0

# Game initialization
initialize_game()
font = pygame.font.Font(None, 36)
BUBBLE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(BUBBLE_EVENT, 1000)  # Spawn a bubble every second

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == BUBBLE_EVENT and not game_over:
            # Spawn a new bubble
            bubble = Bubble(random.randint(50, SCREEN_WIDTH - 50), 0)
            all_sprites.add(bubble)
            bubblesFalling.add(bubble)

    keys = pygame.key.get_pressed()

    if not game_over:

        # Controls
        if keys[pygame.K_SPACE]:
            player.jump()
        player.move(keys)

        # Update game state
        all_sprites.update()

        # Collision: player collects bubbles 
        for collision in pygame.sprite.spritecollide(player, bubblesFalling, True):
            player.catchBubble()

        # Collision: star hits player
        for collision in pygame.sprite.spritecollide(player, blades, True):
            if player.getHp() == 1:
                game_over = True
                break
            else:
                player.handleHitByBlade()

        # Collision: blade hits a falling bubble
        for bubble in bubblesFalling:
            bladeCollisions = pygame.sprite.spritecollide(bubble, blades, True)  # Check blades colliding with this bubble
            if bladeCollisions:
                bubble.kill()  # Remove the bubble

        # Add bubbles holding in hand to "feed fat guy"
        if pygame.sprite.collide_rect(player, fat_guy):
            score += player.getBubblesHolding() 
            player.clearBubblesFromHand()

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
        if keys[pygame.K_SPACE]:
            initialize_game()

    # Drawing
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # UI Elements
    if game_over:
        game_over_text = font.render("GAME OVER", True, BLACK)
        restart_text = font.render("PRESS SPACE TO RESTART", True, BLACK)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 10))
    else:
        score_text = font.render(f"SCORE: {score}", True, BLACK)
        hp_text = font.render(f"HP: {player.getHp()}", True, BLACK)
        temp_bubblesHolding = font.render(f"You are holding: {player.getBubblesHolding()} bubbles", True, BLACK)
        screen.blit(score_text, (10, 50))
        screen.blit(temp_bubblesHolding, (10, 100))
        screen.blit(hp_text, (10, 150))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
