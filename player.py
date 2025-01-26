import pygame
from constants import GRAVITY, SCREEN_HEIGHT, SCREEN_WIDTH,WHITE

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load the placeholder stickman image
        self.image = pygame.image.load("assets/placeholderStick.png")
        self.image = pygame.transform.scale(self.image, (125,125)) 
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (400, SCREEN_HEIGHT - 10)
        self.velocity = 0
        self.speed = 5
        self.bubblesHolding = 0
        self.jumping = 0
        self.bubbles = []
        self.max_bubbles = 2
        self.hasBubbleLeftHand = False
        self.hasBubbleRightHand = False
        self.hp = 3

    def move(self, keys):

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
            self.jump()
        if keys [pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += 12   

        # Keep the player within screen boundaries
        self.rect.x = max(90, min(SCREEN_WIDTH - 80-self.rect.width, self.rect.x))

    def jump(self):
        if self.jumping == 0:
            self.velocity = -12
            self.jumping = 1
        elif self.jumping == 1 and self.velocity > 0:
            self.velocity = -7
            self.jumping = 2

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.jumping = 0

    def handleHitByBlade(self,stop_game):
        if self.bubblesHolding > 0:
            self.bubblesHolding -= 1
            return
        elif self.getHp() == 0:
            stop_game()
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