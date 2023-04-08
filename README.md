# Snake Souls
 Snake Game Documentation
This documentation covers the implementation of a snake game with multiple levels, various terrains, bonuses, and additional features. The game is built using Python and the Pygame library.

Table of Contents:
- Introduction
- Requirements
- File Structure
- Classes
- Main
- Game
- Snake
- Food
- Bonus
- Terrain
- HighScore
- Levels
- Game Over 


# Introduction \
This snake game features a snake that grows as it consumes food, randomly spawning bonuses, and various terrain types that affect the snake's speed. The game includes multiple levels with different configurations and a high score system.

# Requirements
Python 3.6 or higher
Pygame library

# Classes

## Main
main.py is the entry point for the game. It initializes a Game instance, and manages the game loop, user inputs, and screen rendering.


## Game
game.py contains the Game class, which manages the game state, snake, food, bonuses, terrains, and high scores. It handles game logic, level loading, and collision detection.


## Snake
snake.py contains the Snake class, which represents the snake's body, position, and direction. It handles the snake's movement, growth, and speed changes.


## Food
food.py contains the Food class, which represents the food in the game. It manages the position and size of the food, and handles rendering the food on the screen.


## Bonus
bonus.py contains the Bonus class, which represents the different bonus types in the game. It manages the position, type, and size of the bonuses, and handles rendering the bonuses on the screen.


## Terrain
terrain.py contains the Terrain class, which represents the different terrain types in the game. It manages the position and type of the terrain, and handles rendering the terrain on the screen.


## HighScore
highscore.py contains the HighScore class, which manages the high scores for the game. It handles loading, saving, and displaying high scores.


# Levels
The levels are stored in the levels folder as JSON files. Each level file defines the level's properties, including the initial snake position and speed, the positions of the terrain tiles, and the points required to complete the level. The Game class is responsible for loading and parsing the level files.

Example of a level JSON file:

json
Copy code
{
  "snake_start_position": [5, 5],
  "snake_start_speed": 5,
  "points_to_complete": 10,
  "terrains": [
    {
      "type": "slow_down",
      "tiles": [[2, 2], [2, 3], [2, 4]]
    },
    {
      "type": "speed_up",
      "tiles": [[10, 10], [11, 10], [12, 10]]
    }
  ]
}

# Game Over
When the game is over, the player is presented with three options:

Restart the game
View personal records
Quit the game
The Game class manages the game over state and provides the player with these options.
