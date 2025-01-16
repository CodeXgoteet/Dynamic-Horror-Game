# Dynamic-Horror-Game


A dynamic horror game created using Python and Pygame, featuring AI-driven enemies, procedurally generated environments, and an evolving fear system. This game creates a thrilling and immersive experience for players as they navigate through an unpredictable and eerie world.

## Features
- **Dynamic Fear System**: Adjusts fear levels based on in-game conditions such as darkness and noise.
- **AI-Driven Enemy**: The enemy uses A* pathfinding to dynamically chase the player.
- **Procedural Environment Generation**: Randomly generates environmental objects like trees, rocks, and fences to keep the game fresh.
- **Day-Night Cycle**: Darkness increases during nighttime, enhancing the horror experience.
- **Collision Detection**: Game ends when the enemy catches the player.

## Requirements
- Python 3.x
- Pygame library (`pip install pygame`)

## How to Play
1. **Objective**: Avoid the enemy and survive as long as possible.
2. Use arrow keys to move the player:
   - `Left Arrow`: Move left
   - `Right Arrow`: Move right
   - `Up Arrow`: Move up
   - `Down Arrow`: Move down
3. Be cautious of the enemy, which dynamically chases you based on your location.
4. Keep an eye on the environment as it changes based on your fear level.

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/dynamic-horror-game.git
## Navigate to the project directory
cd dynamic-horror-game
## Install the required dependencies
pip install pygame
## Run the game
python Dynamic-Horror-Game.py

## Project Structure
Dynamic-Horror-Game.py: The main game script containing the logic for the AI, environment generation, and gameplay mechanics.
## Key Gameplay Mechanics
Fear System: Darkness and noise dynamically adjust the fear level, influencing the environment.
Enemy AI: The enemy's behavior changes based on proximity to the player, switching between idle, approaching, and chasing states.
Procedural Generation: Random objects appear in the environment as fear increases, adding to the suspense.
##Screenshot
![Screenshot 2025-01-16 171237](https://github.com/user-attachments/assets/4db13a61-c012-423b-b32d-f679c72dfacd)
