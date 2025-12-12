#!/usr/bin/env python3
"""
Pacman Game
Use arrow keys to move Pacman and collect all pellets while avoiding ghosts!
"""

import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 40
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# Game maze layout (1 = wall, 0 = path, 2 = pellet)
MAZE = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1],
    [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 1, 2, 2, 2, 1, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 2, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 2, 1, 1, 1, 1],
    [1, 1, 1, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 1, 1, 1],
    [1, 1, 1, 1, 2, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 2, 1, 1, 1, 1],
    [0, 0, 0, 0, 2, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0, 0],
    [1, 1, 1, 1, 2, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 2, 1, 1, 1, 1],
    [1, 1, 1, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 1, 1, 1],
    [1, 1, 1, 1, 2, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 2, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
]

class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        
    def move(self, maze):
        # Try to move in the next direction first
        if self.next_direction != (0, 0):
            new_x = self.x + self.next_direction[0]
            new_y = self.y + self.next_direction[1]
            if self.can_move(new_x, new_y, maze):
                self.direction = self.next_direction
                self.x = new_x
                self.y = new_y
                return
        
        # Continue in current direction
        new_x = self.x + self.direction[0]
        new_y = self.y + self.direction[1]
        if self.can_move(new_x, new_y, maze):
            self.x = new_x
            self.y = new_y
    
    def can_move(self, x, y, maze):
        if y < 0 or y >= len(maze) or x < 0 or x >= len(maze[0]):
            return False
        return maze[y][x] != 1
    
    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, 
                         (self.x * CELL_SIZE + CELL_SIZE // 2, 
                          self.y * CELL_SIZE + CELL_SIZE // 2), 
                         CELL_SIZE // 2 - 2)

class Ghost:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.direction = (0, 0)
        
    def move(self, maze, pacman_pos):
        # Simple AI: randomly choose direction, with bias toward pacman
        possible_moves = []
        
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            new_x = self.x + dx
            new_y = self.y + dy
            if self.can_move(new_x, new_y, maze):
                # Calculate distance to pacman
                dist = abs(new_x - pacman_pos[0]) + abs(new_y - pacman_pos[1])
                possible_moves.append((dx, dy, dist))
        
        if possible_moves:
            # 70% chance to move toward pacman, 30% random
            if random.random() < 0.7:
                # Choose move that reduces distance to pacman
                possible_moves.sort(key=lambda x: x[2])
                self.direction = (possible_moves[0][0], possible_moves[0][1])
            else:
                # Random move
                move = random.choice(possible_moves)
                self.direction = (move[0], move[1])
            
            self.x += self.direction[0]
            self.y += self.direction[1]
    
    def can_move(self, x, y, maze):
        if y < 0 or y >= len(maze) or x < 0 or x >= len(maze[0]):
            return False
        return maze[y][x] != 1
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, 
                         (self.x * CELL_SIZE + CELL_SIZE // 2, 
                          self.y * CELL_SIZE + CELL_SIZE // 2), 
                         CELL_SIZE // 2 - 2)
        # Draw eyes
        eye_offset = CELL_SIZE // 6
        eye_size = 3
        pygame.draw.circle(screen, WHITE,
                         (self.x * CELL_SIZE + CELL_SIZE // 2 - eye_offset,
                          self.y * CELL_SIZE + CELL_SIZE // 2 - eye_offset),
                         eye_size)
        pygame.draw.circle(screen, WHITE,
                         (self.x * CELL_SIZE + CELL_SIZE // 2 + eye_offset,
                          self.y * CELL_SIZE + CELL_SIZE // 2 - eye_offset),
                         eye_size)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pacman Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.reset_game()
    
    def reset_game(self):
        self.maze = [row[:] for row in MAZE]  # Copy the maze
        self.pacman = Pacman(1, 1)
        self.ghosts = [
            Ghost(9, 9, RED),
            Ghost(10, 9, PINK),
            Ghost(9, 10, CYAN),
            Ghost(10, 10, ORANGE)
        ]
        self.score = 0
        self.game_over = False
        self.game_won = False
        self.total_pellets = sum(row.count(2) for row in self.maze)
    
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if self.game_over or self.game_won:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                else:
                    if event.key == pygame.K_UP:
                        self.pacman.next_direction = (0, -1)
                    elif event.key == pygame.K_DOWN:
                        self.pacman.next_direction = (0, 1)
                    elif event.key == pygame.K_LEFT:
                        self.pacman.next_direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.pacman.next_direction = (1, 0)
        return True
    
    def update(self):
        if self.game_over or self.game_won:
            return
        
        # Move pacman
        self.pacman.move(self.maze)
        
        # Check if pacman ate a pellet
        if self.maze[self.pacman.y][self.pacman.x] == 2:
            self.maze[self.pacman.y][self.pacman.x] = 0
            self.score += 10
            
            # Check win condition
            if self.score == self.total_pellets * 10:
                self.game_won = True
        
        # Move ghosts
        for ghost in self.ghosts:
            ghost.move(self.maze, (self.pacman.x, self.pacman.y))
            
            # Check collision with pacman
            if ghost.x == self.pacman.x and ghost.y == self.pacman.y:
                self.game_over = True
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw maze
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                if cell == 1:  # Wall
                    pygame.draw.rect(self.screen, BLUE, 
                                   (x * CELL_SIZE, y * CELL_SIZE, 
                                    CELL_SIZE, CELL_SIZE))
                elif cell == 2:  # Pellet
                    pygame.draw.circle(self.screen, WHITE,
                                     (x * CELL_SIZE + CELL_SIZE // 2,
                                      y * CELL_SIZE + CELL_SIZE // 2), 3)
        
        # Draw game entities
        self.pacman.draw(self.screen)
        for ghost in self.ghosts:
            ghost.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, SCREEN_HEIGHT - 40))
        
        # Draw game over or win message
        if self.game_over:
            text = self.font.render("GAME OVER!", True, RED)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)
            
            restart_text = self.small_font.render("Press SPACE to restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            self.screen.blit(restart_text, restart_rect)
        
        elif self.game_won:
            text = self.font.render("YOU WIN!", True, YELLOW)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)
            
            restart_text = self.small_font.render("Press SPACE to play again", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
