# Pacman Game

A classic Pacman game implementation in Python using Pygame.

## Features

- Classic Pacman gameplay
- Maze navigation
- 4 colorful ghosts with AI behavior
- Score tracking
- Win/lose conditions
- Restart functionality

## Requirements

- Python 3.7+
- Pygame

## Installation & Setup

### 1. Create and activate virtual environment

```bash
# Create virtual environment
python3 -m venv pacman_venv

# Activate virtual environment
# On Linux/Mac:
source pacman_venv/bin/activate
# On Windows:
pacman_venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Or install pygame directly:

```bash
pip install pygame
```

## How to Run

Make sure your virtual environment is activated, then run:

```bash
python pacman.py
```

## How to Play

- **Arrow Keys**: Move Pacman up, down, left, or right
- **Objective**: Collect all the pellets (white dots) while avoiding the ghosts
- **Scoring**: Each pellet is worth 10 points
- **Win**: Collect all pellets
- **Lose**: Get caught by a ghost
- **Restart**: Press SPACE after game over or winning

## Game Elements

- **Yellow Circle**: Pacman (you!)
- **Colored Circles**: Ghosts (Red, Pink, Cyan, Orange)
- **White Dots**: Pellets to collect
- **Blue Blocks**: Walls

## Controls Summary

| Key | Action |
|-----|--------|
| ↑ | Move Up |
| ↓ | Move Down |
| ← | Move Left |
| → | Move Right |
| SPACE | Restart (after game over) |

## Deactivating Virtual Environment

When you're done playing:

```bash
deactivate
```

## Troubleshooting

If you encounter any issues:

1. Make sure the virtual environment is activated
2. Verify pygame is installed: `pip list | grep pygame`
3. Check Python version: `python --version` (should be 3.7+)

## License

Free to use and modify for personal and educational purposes.

Enjoy the game! 🎮👻
