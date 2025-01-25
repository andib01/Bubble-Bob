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
    global player, bubblesFalling, blades, all_sprites, big_guy, evil_guy, game_over, win_state, score
    player = Player()
    big_guy = BigGuy()
    evil_guy = BladeGuy()
    bubblesFalling = pygame.sprite.Group()
    blades = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(player, big_guy, evil_guy)
    game_over = False
    win_state = False
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
        if event.type == BUBBLE_EVENT and not game_over and not win_state:
            x_position = random.randint(*allowed_spawn_areas[0])
            # Create and add the bubble
            bubble = Bubble(x_position, 0)
            all_sprites.add(bubble)
            bubblesFalling.add(bubble)

    keys = pygame.key.get_pressed()

    if not game_over and not win_state:
        # Controls
        player.move(keys)

        # Update game state
        all_sprites.update()

        # Collision: player collects bubbles 
        for collision in pygame.sprite.spritecollide(player, bubblesFalling, True):
            player.catchBubble()

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

        # Add bubbles holding in hand to "feed big guy"
        if pygame.sprite.collide_rect(player, big_guy):
            score += player.getBubblesHolding() 
            if player.getBubblesHolding() > 0:
                big_guy.eat(score)
                player.clearBubblesFromHand()

        # Blade shooting from Evil Guy
        if random.random() < 0.02:  # Adjust frequency
            blade = evil_guy.shoot_blade()
            all_sprites.add(blade)
            blades.add(blade)

        # Check win condition
        if score >= 14:  # Win condition
            win_state = True

    else:
        if keys[pygame.K_p]:
            initialize_game()

    # Drawing
    screen.fill(WHITE)
    pygame.draw.line(screen,BLACK, (SCREEN_WIDTH - 80, 0), (SCREEN_WIDTH - 80, SCREEN_HEIGHT), 2)
    all_sprites.draw(screen)

    # UI Elements
    if game_over or win_state:
        state_text = "YOU WIN!" if win_state else "GAME OVER"
        state_message = font.render(state_text, True, BLACK)
        restart_text = font.render("PRESS P TO RESTART", True, BLACK)
        screen.blit(state_message, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
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
