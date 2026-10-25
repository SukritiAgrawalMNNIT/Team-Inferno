# Cloak of Chaos: Rift Runner

**A 2D obstacle-avoidance game developed by Team Inferno using Python and Pygame.**

## About the Game

Cloak of Chaos: Rift Runner is a 2D arcade-style game in which the player controls a mysterious cloak and navigates through obstacles. The objective is to avoid collisions, survive as long as possible, and achieve a high score.

## Features

- Animated cloak character with a trailing effect.
- Obstacle-based gameplay.
- Main menu, pause screen, and game-over screen.
- Score and high-score tracking.
- High-score persistence using JSON storage.
- Dark-themed user interface.

Note: Keep only the features that are implemented and working in the current version.

## Controls

- Space: Propel the cloak upward.
- Esc: Pause or resume the game.

## Requirements

- Python 3.13
- Pygame 2.6.1

## Setup and Run

### 1. Clone the repository

git clone https://github.com/SukritiAgrawalMNNIT/Team-Inferno.git

cd Team-Inferno

### 2. Create a virtual environment

py -3.13 -m venv .venv

### 3. Activate the environment

Windows PowerShell:

.\\.venv\\Scripts\\Activate.ps1

Git Bash:

source .venv/Scripts/activate

### 4. Install Pygame

python -m pip install pygame==2.6.1

### 5. Run the game

python main.py

## Project Structure

Team-Inferno/
- assets/ — Game fonts and other resources
- screens/ — Game screens and obstacle logic
- main.py — Application entry point
- player.py — Player character
- score_manager.py — Score management
- high_score_storage.py — High-score persistence
- difficulty_manager.py — Difficulty progression
- power_up.py — Power-up logic
- highscore.json — Stored high score
- README.md — Project documentation

## Running Tests

Run the available test files using:

python -m unittest discover -p "test_*.py"

If the project uses pytest, install it and run:

python -m pip install pytest

python -m pytest

## Windows Executable

A packaged Windows build can be created with PyInstaller.

Install PyInstaller:

python -m pip install pyinstaller

Build the game:

python -m PyInstaller --noconfirm --onedir --windowed --name CloakOfChaos --add-data "assets;assets" main.py

The executable and supporting files will be generated in:

dist/CloakOfChaos/

Run CloakOfChaos.exe from that folder. When sharing the packaged game, distribute the ZIP containing the entire folder, not just the executable.

## High-Score Storage

The game uses highscore.json to store high-score data. The storage logic should handle a missing or invalid save file safely so the game can start without an existing record.

## Team

**Team Inferno**

Developed as a team project using Python and Pygame.