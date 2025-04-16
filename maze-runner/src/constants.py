"""
Constants module containing all game-related constants.
"""

from enum import Enum

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

# Maze cell types
WALL = '#'
PATH = ' '
START = 'S'
END = 'E'

# Colors for visualization
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Cell size for visualization
CELL_SIZE = 20

# Window settings
WINDOW_SIZE = 768  # Adjusted to fit the 64x64 static maze (64 * 12 = 768)
GRID_SIZE = WINDOW_SIZE // CELL_SIZE
FPS = 60

# Maze dimensions
MAZE_WIDTH = 30
MAZE_HEIGHT = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255) 