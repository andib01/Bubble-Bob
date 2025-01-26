import pygame
from constants import GRAVITY, SCREEN_HEIGHT, SCREEN_WIDTH, WHITE

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load images for different states
        self.images = {
            "idle": pygame.image.load("assets/player/faddyidle.jpg").convert_alpha(),
            "runningLeft": pygame.image.load("assets/player/faddyleft.jpg").convert_alpha(),
            "runningRight": pygame.image.load("assets/player/faddyright.jpg").convert_alpha(),
        }

        # Scale all images
        for key in self.images:
            self.images[key] = pygame.transform.scale(self.images[key], (105, 105))
            

        # Set initial state
        self.current_state = "idle"
        self.image = self.images[self.current_state]
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
            self.current_state = "runningLeft"  
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
            self.current_state = "runningRight" 
        else:
            self.current_state = "idle"  

        if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
            self.jump()
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
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
            if not (pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_RIGHT]):
                self.current_state = "idle"  # Return to idle state when grounded

        # Update the displayed image based on the current state
        self.image = self.images[self.current_state]

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
        if not self.hasBubbleRightHand:
            self.hasBubbleRightHand = True

    def clearBubblesFromHand(self):
        self.hasBubbleLeftHand = False
        self.hasBubbleRightHand = False
        self.bubblesHolding = 0

    def remove_hp(self):
        self.hp -= 1

    def getBubblesHolding(self):
        return self.bubblesHolding

    def getHp(self):
        return self.hp