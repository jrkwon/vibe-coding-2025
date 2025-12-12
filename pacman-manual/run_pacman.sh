#!/bin/bash

# Run Pacman game using the virtual environment

# Check if virtual environment exists
if [ ! -d "pacman_venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv pacman_venv
    echo "Installing dependencies..."
    ./pacman_venv/bin/pip install -r requirements.txt
fi

# Run the game
echo "Starting Pacman game..."
./pacman_venv/bin/python pacman.py
