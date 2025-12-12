import pygame
from player import Player
from stars import Star
from bullet import Bullet
from enemy import Enemy

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.player = Player(screen)
        self.bullets = pygame.sprite.Group() # Player bullets
        self.enemy_bullets = pygame.sprite.Group() # Enemy bullets
        self.enemies = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        
        # Create stars
        for _ in range(100):
            star = Star(screen.get_width(), screen.get_height())
            self.stars.add(star)
            
        # Create enemies
        self.create_enemy_wave()

        self.all_sprites = pygame.sprite.Group(self.stars, self.player, self.bullets, self.enemies, self.enemy_bullets)
        
        self.score = 0
        self.lives = 5
        self.font = pygame.font.Font(None, 36)
        self.game_over = False

    def create_enemy_wave(self):
        for row in range(3):
            for col in range(8):
                enemy = Enemy(100 + col * 60, 50 + row * 50)
                self.enemies.add(enemy)

    def reset_game(self):
        self.score = 0
        self.lives = 5
        self.game_over = False
        self.enemies.empty()
        self.bullets.empty()
        self.enemy_bullets.empty()
        self.create_enemy_wave()
        self.player.rect.midbottom = (self.screen.get_width() // 2, self.screen.get_height() - 20)
        self.all_sprites = pygame.sprite.Group(self.stars, self.player, self.bullets, self.enemies, self.enemy_bullets)

    def update(self):
        if self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.reset_game()
            return

        self.all_sprites.update()
        
        # Handle shooting
        if self.player.ready_to_shoot:
            bullet = self.player.shoot()
            if bullet:
                self.bullets.add(bullet)
                self.all_sprites.add(bullet)
        
        # Enemy shooting
        for enemy in self.enemies:
            bullet = enemy.shoot()
            if bullet:
                bullet.image.fill((255, 0, 0)) # Red bullets for enemies
                self.enemy_bullets.add(bullet)
                self.all_sprites.add(bullet)
                
        # Bullet - Enemy collision
        hits = pygame.sprite.groupcollide(self.enemies, self.bullets, True, True)
        for hit in hits:
            self.score += 10
            
        # Player - Enemy collision
        hits = pygame.sprite.spritecollide(self.player, self.enemies, True) # Kill enemy on impact
        if hits:
            self.death_sequence()

        # Player - Enemy Bullet collision
        hits = pygame.sprite.spritecollide(self.player, self.enemy_bullets, True)
        if hits:
            self.death_sequence()
            
    def death_sequence(self):
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True
        else:
            # Respawn player
            self.player.rect.midbottom = (self.screen.get_width() // 2, self.screen.get_height() - 20)
            # Clear projectiles for fairness
            self.bullets.empty()
            self.enemy_bullets.empty()
            # Clear sprites from groups to avoid zombie bullets logic but keep stars/enemies
            # Actually better to just rebuild all_sprites
            self.all_sprites = pygame.sprite.Group(self.stars, self.player, self.bullets, self.enemies, self.enemy_bullets)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.stars.draw(self.screen)
        self.bullets.draw(self.screen)
        self.enemies.draw(self.screen)
        if not self.game_over:
            self.player.draw_player(self.screen)
        
        # Draw HUD
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        
        lives_text = self.font.render(f"Lives: {self.lives}", True, (255, 255, 255))
        self.screen.blit(lives_text, (self.screen.get_width() - 120, 10))
        
        if self.game_over:
            game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
            restart_text = self.font.render("Press SPACE to Restart", True, (255, 255, 255))
            
            text_rect = game_over_text.get_rect(center=(self.screen.get_width()/2, self.screen.get_height()/2 - 20))
            restart_rect = restart_text.get_rect(center=(self.screen.get_width()/2, self.screen.get_height()/2 + 20))
            
            self.screen.blit(game_over_text, text_rect)
            self.screen.blit(restart_text, restart_rect)
