import pygame
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        # Galaga ship pixel art style (simplified)
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
        
        # Colors
        white = (255, 255, 255)
        red = (200, 0, 0)
        
        # Draw ship body
        # Main body
        pygame.draw.rect(self.image, white, (14, 0, 4, 8))   # Top tip
        pygame.draw.rect(self.image, white, (12, 8, 8, 8))   # Upper body
        pygame.draw.rect(self.image, white, (10, 16, 12, 8)) # Lower body
        pygame.draw.rect(self.image, white, (4, 20, 24, 8))  # Base wings
        
        # Red details (engines/guns)
        pygame.draw.rect(self.image, red, (4, 16, 4, 12))  # Left engine
        pygame.draw.rect(self.image, red, (24, 16, 4, 12)) # Right engine
        pygame.draw.rect(self.image, red, (14, 8, 4, 4))   # Cockpit detail
        
        self.rect = self.image.get_rect()
        self.rect.midbottom = (screen.get_width() // 2, screen.get_height() - 20)
        self.speed = 5
        self.last_shot_time = 0
        self.shoot_delay = 250 # ms
        self.ready_to_shoot = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            
        if keys[pygame.K_SPACE]:
            self.ready_to_shoot = True
        else:
            self.ready_to_shoot = False

        # Clamp to screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen.get_width():
            self.rect.right = self.screen.get_width()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time > self.shoot_delay:
            self.last_shot_time = now
            return Bullet(self.rect.centerx, self.rect.top)
        return None
        
    def draw_player(self, screen):
        screen.blit(self.image, self.rect)
