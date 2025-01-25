from blade import Blade
from constants import GREEN, SCREEN_HEIGHT, SCREEN_WIDTH

class SplitBlade(Blade):
    def __init__(self, speed):
        super().__init__(speed)
        self.image.fill(GREEN) 
        self.has_split = False

    def update(self):
        super().update()
        if not self.has_split and self.rect.x < SCREEN_WIDTH:
            blade1 = Blade(self.speed)
            blade1.rect = self.rect.copy()
            blade1.rect.y = min(SCREEN_HEIGHT - blade1.rect.height, self.rect.y + 40)
            blade2 = Blade(self.speed)
            blade2.rect = self.rect.copy()
            blade2.rect.y = max(0, self.rect.y - 40)
            self.has_split = True
            self.kill()
