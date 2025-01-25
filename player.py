import pygame
from constants import GRAVITY, SCREEN_HEIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (400, SCREEN_HEIGHT - 10)
        self.velocity = 0
        self.speed = 5
        self.bubblesHolding = 0
        self.max_bubbles = 2
        self.hasBubbleLeftHand = False
        self.hasBubbleRightHand = False
        self.hp = 3

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

    def jump(self):
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.velocity = -12

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def handleHitByBlade(self):
        if self.bubblesHolding > 0:
            self.bubblesHolding -= 1
            return
        else:
            self.remove_hp()

    def catchBubble(self):
        if self.bubblesHolding < self.max_bubbles:
            self.bubblesHolding += 1
            self.addNewBubbleToHand()

    def addNewBubbleToHand(self):
        if not self.hasBubbleLeftHand:
            self.hasBubbleLeftHand = True
            # DRAW THE ACTUAL BUBBLE IN LEFT HAND 
          
        if not self.hasBubbleRightHand:
            self.hasBubbleRightHand = True
            # DRAW THE ACTUAL BUBBLE IN RIGHT HAND 

    def clearBubblesFromHand(self):
        self.hasBubbleLeftHand = False
        self.hasBubbleRightHand = False
        self.bubblesHolding = 0

    # Function to remove a heart (decrease HP)
    def remove_hp(self):
        self.hp -= 1

    # GETTERS

    def getBubblesHolding(self):
        return self.bubblesHolding

    def getHp(self):
        return self.hp