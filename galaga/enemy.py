import pygame
import math
import random
from bullet import Bullet

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 24), pygame.SRCALPHA)
        
        # Bug colors
        blue = (0, 100, 255)
        yellow = (255, 200, 0)
        
        # Draw bug body (simplified Galaga bee/moth)
        # Wings
        pygame.draw.rect(self.image, blue, (2, 0, 8, 8))
        pygame.draw.rect(self.image, blue, (22, 0, 8, 8))
        pygame.draw.rect(self.image, blue, (0, 8, 10, 8))
        pygame.draw.rect(self.image, blue, (22, 8, 10, 8))
        
        # Body
        pygame.draw.rect(self.image, yellow, (10, 4, 12, 16))
        
        # Eyes/Mandibles
        pygame.draw.rect(self.image, blue, (8, 20, 4, 4))
        pygame.draw.rect(self.image, blue, (20, 20, 4, 4))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.start_y = y
        self.rect.y = y
        self.speed_x = 2
        self.t = 0
        self.shoot_delay = random.randint(1000, 3000)
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.t += 0.05
        self.rect.x += self.speed_x
        self.rect.y = self.start_y + math.sin(self.t) * 50
        
        # Bounce off walls (simplified)
        if self.rect.right > 800 or self.rect.left < 0:
            self.speed_x *= -1

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.shoot_delay = random.randint(2000, 5000)
            return Bullet(self.rect.centerx, self.rect.bottom, speed=5)
        return None
