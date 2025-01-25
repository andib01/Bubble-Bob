from blade import Blade
import math

from constants import ORANGE, SCREEN_HEIGHT

class ZigzagBlade(Blade):
    def __init__(self, speed):
        super().__init__(speed)
        self.image.fill(ORANGE) 
        self.angle = 0
        self.frequency = 0.1

    def update(self):
        super().update()
        self.angle += self.frequency
        self.rect.y += math.sin(self.angle) * 3
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))
