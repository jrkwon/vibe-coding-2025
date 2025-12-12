import pygame
import random

class Star(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.Surface((2, 2))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(screen_width)
        self.rect.y = random.randrange(screen_height)
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > self.screen_height:
            self.rect.y = 0
            self.rect.x = random.randrange(self.screen_width)
