import pygame
import sys
import random
from bigGuy import BigGuy
from bladeGuy import BladeGuy
from player import Player
from bubble import Bubble
import os
from constants import *

# Initialize Pygame
pygame.init()
# init sounds
pygame.mixer.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BubbleZilla")
clock = pygame.time.Clock()
heart_image = pygame.image.load("assets/heart.png").convert_alpha()
heart_image = pygame.transform.smoothscale(heart_image, (30, 30))

def draw_hearts(screen, hp):
    x_offset = SCREEN_WIDTH - 120
    for i in range(hp):
        screen.blit(heart_image, (x_offset, 10))
        x_offset += heart_image.get_width() + 5

# Load the background image
background_image = pygame.image.load("assets/background.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale to screen size

def initialize_game():
    global player, bubblesFalling, blades, all_sprites, big_guy, evil_guy, game_over, win_state, score, popSound, jumpSound, disposeSound, ouchSound, dieSound, s
    player = Player()
    big_guy = BigGuy()
    evil_guy = BladeGuy()
    bubblesFalling = pygame.sprite.Group()
    blades = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(player, big_guy, evil_guy)
    game_over = False
    win_state = False
    score = 0
    s = 'sounds'
    popSound = pygame.mixer.Sound(os.path.join(s, 'pop.mp3'))
    jumpSound = pygame.mixer.Sound(os.path.join(s, 'jump.mp3'))
    disposeSound = pygame.mixer.Sound(os.path.join(s, 'dispose.mp3'))
    ouchSound = pygame.mixer.Sound(os.path.join(s, 'ouch.mp3'))
    dieSound = pygame.mixer.Sound(os.path.join(s, 'die.mp3'))

# Game initialization
initialize_game()
font = pygame.font.Font(None, 36)
BUBBLE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(BUBBLE_EVENT, 1000)  # Spawn a bubble every second
allowed_spawn_areas = [
    (90, SCREEN_WIDTH - 80 - 50)  
]
def stop_game():
    global game_over
    game_over = True
    state_text = "YOU WIN!" if win_state else "GAME OVER"
    state_message = font.render(state_text, True, BLACK)
    restart_text = font.render("PRESS P TO RESTART", True, BLACK)
    screen.blit(state_message, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 10))
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
        # jump sound
        if keys[pygame.K_SPACE]:  # Check for spacebar key
            pygame.mixer.Sound.play(jumpSound)

        # Controls
        player.move(keys)

        # Update game state
        all_sprites.update()

        # Collision: player collects bubbles 
        for collision in pygame.sprite.spritecollide(player, bubblesFalling, True):
            player.catchBubble()

        # Collision hit by blade
        for collision in pygame.sprite.spritecollide(player, blades, True):
                result = player.handleHitByBlade(stop_game)
                if result == "lostBubble":
                    break  
                elif result == "lostHp":
                    pygame.mixer.Sound.play(ouchSound)
                else:
                    pygame.mixer.Sound.play(dieSound)  
                    stop_game()                       

        # Collision: blade hits a falling bubble
        for bubble in bubblesFalling:
            bladeCollisions = pygame.sprite.spritecollide(bubble, blades, True)  # Check blades colliding with this bubble
            if bladeCollisions:
                pygame.mixer.Sound.play(popSound)
                bubble.kill()  # Remove the bubble

        # Add bubbles holding in hand to "feed big guy", must be 2 bubbles
        if pygame.sprite.collide_rect(player, big_guy) and player.getBubblesHolding() == 2:
            score += player.getBubblesHolding() 
            if player.getBubblesHolding() > 0:
                big_guy.eat(score)
                pygame.mixer.Sound.play(disposeSound)
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
    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)
    draw_hearts(screen, player.hp)

    # UI Elements
    if game_over or win_state:
        stop_game()
    else:
        score_text = font.render(f"SCORE: {score}", True, BLACK)
        temp_bubblesHolding = font.render(f"You are holding: {player.getBubblesHolding()} bubbles", True, BLACK)
        screen.blit(score_text, (10, 50))
        screen.blit(temp_bubblesHolding, (10, 100))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
