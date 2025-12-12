import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=-10):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0 or self.rect.top > 600:
            self.kill()
