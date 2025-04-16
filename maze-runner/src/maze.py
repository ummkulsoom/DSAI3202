"""
Maze module containing the Maze class for generating and managing the game maze.
"""

import random
from typing import List, Tuple, Optional
import numpy as np
from .constants import WALL, PATH, START, END


class Maze:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = np.full((height, width), WALL, dtype=str)
        self.start_pos: Optional[Tuple[int, int]] = None
        self.end_pos: Optional[Tuple[int, int]] = None
        # Don't seed the random number generator here to ensure different mazes each time
        self.generate_maze()
        self.set_start_end_positions()

    def generate_maze(self):
        """Generate a random maze using depth-first search algorithm."""
        # Initialize all cells as walls
        self.grid = np.full((self.height, self.width), WALL, dtype=str)
        
        # Start from a random cell
        start_x = random.randint(1, self.width-2)
        start_y = random.randint(1, self.height-2)
        stack = [(start_x, start_y)]
        self.grid[start_y, start_x] = PATH

        while stack:
            current = stack[-1]
            x, y = current

            # Find unvisited neighbors that are two cells away
            neighbors = []
            for dx, dy in [(0, 2), (2, 0), (0, -2), (-2, 0)]:
                nx, ny = x + dx, y + dy
                if 0 < nx < self.width-1 and 0 < ny < self.height-1 and self.grid[ny, nx] == WALL:
                    neighbors.append((nx, ny))

            if neighbors:
                # Choose a random neighbor
                next_cell = random.choice(neighbors)
                nx, ny = next_cell

                # Remove wall between current and next cell
                wx, wy = (x + nx) // 2, (y + ny) // 2
                self.grid[wy, wx] = PATH
                self.grid[ny, nx] = PATH

                stack.append(next_cell)
            else:
                stack.pop()

    def set_start_end_positions(self):
        """Set start and end positions ensuring they are on white squares.
        Start position will be on the topmost line with white cells,
        and end position will be on the bottommost line with white cells."""
        # Find all white squares (0s) in the maze
        white_squares = []
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y, x] == PATH:
                    white_squares.append((x, y))
        
        if not white_squares:
            # If no white squares found, regenerate the maze
            self.generate_maze()
            self.set_start_end_positions()
            return
        
        # Find topmost and bottommost lines with white cells
        topmost_line = min(y for x, y in white_squares)
        bottommost_line = max(y for x, y in white_squares)
        
        # Get white cells on topmost and bottommost lines
        top_white_cells = [(x, y) for x, y in white_squares if y == topmost_line]
        bottom_white_cells = [(x, y) for x, y in white_squares if y == bottommost_line]
        
        if not top_white_cells or not bottom_white_cells:
            # If no white cells on top or bottom, regenerate the maze
            self.generate_maze()
            self.set_start_end_positions()
            return
        
        # Choose random positions from top and bottom lines
        self.start_pos = random.choice(top_white_cells)
        self.end_pos = random.choice(bottom_white_cells)
        
        # Ensure start and end positions are not walls
        self.grid[self.start_pos[1], self.start_pos[0]] = START
        self.grid[self.end_pos[1], self.end_pos[0]] = END

    def is_wall(self, pos: Tuple[int, int]) -> bool:
        """Check if a position is a wall"""
        x, y = pos
        return (0 <= x < self.width and 
                0 <= y < self.height and 
                self.grid[y, x] == WALL)

    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get valid neighboring positions"""
        x, y = pos
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x < self.width and 
                0 <= new_y < self.height and 
                not self.is_wall((new_x, new_y))):
                neighbors.append((new_x, new_y))
        return neighbors


class StaticMaze(Maze):
    # The predefined maze pattern with a simpler path
    STATIC_PATTERN = [
        "11111111111011111111111111111111111111111111111111111111111111",
        "10000000010000000000000000000000000000000000000000000000000001",
        "10111111110111111111111111111111111111111111111111111111111101",
        "10100000000100000000000000000000000000000000000000000000000101",
        "10101111111101111111111111111111111111111111111111111111110101",
        "10100000000100000000000000000000000000000000000000000000010101",
        "10111111110111111111111111111111111111111111111111111111010101",
        "10000000010000000000000000000000000000000000000000000000010101",
        "11111111011111111111111111111111111111111111111111111111010101",
        "10000000010000000000000000000000000000000000000000000000010101",
        "10111111110111111111111111111111111111111111111111111111010101",
        "10000000010000000000000000000000000000000000000000000000010101",
        "11111111011111111111111111111111111111111111111111111111010101",
        "10000000010000000000000000000000000000000000000000000000010101",
        "10111111110111111111111111111111111111111111111111111111010101",
        "10000000010000000000000000000000000000000000000000000000010101",
        "11111111011111111111111111111111111111111111111111111111010101",
        "10000000010000000000000000000000000000000000000000000000010101",
        "10111111110111111111111111111111111111111111111111111111010101",
        "10000000010000000000000000000000000000000000000000000000010101",
        "11111111011111111111111111111111111111111111111111111111010101",
        "10000000010000000000000000000000000000000000000000000000010101",
        "10111111110111111111111111111111111111111111111111111111010101",
        "10000000010000000000000000000000000000000000000000000000010101",
        "11111111011111111111111111111111111111111111111111111111010101",
        "10000000010000000000000000000000000000000000000000000000010101",
        "10111111110111111111111111111111111111111111111111111111010101",
        "10000000010000000000000000000000000000000000000000000000010101",
        "11111111011111111111111111111111111111111111111111111111010101",
        "10000000010000000000000000000000000000000000000000000000010101",
        "10111111110111111111111111111111111111111111111111111111010101",
        "10000000010000000000000000000000000000000000000000000000010101",
        "11111111011111111111111111111111111111111111111111111111010101",
        "10000000010000000000000000000000000000000000000000000000010101",
        "10111111110111111111111111111111111111111111111111111111010101",
        "10000000010000000000000000000000000000000000000000000000010101",
        "11111111011111111111111111111111111111111111111111111111010101",
        "10000000010000000000000000000000000000000000000000000000010101",
        "10111111110111111111111111111111111111111111111111111111010101",
        "10000000010000000000000000000000000000000000000000000000010101",
        "11111111011111111111111111111111111111111111111111111111010101",
        "10000000010000000000000000000000000000000000000000000000010101",
        "10111111110111111111111111111111111111111111111111111111010101",
        "10000000010000000000000000000000000000000000000000000000010101",
        "11111111111111111111111111111111111111111111111111111111111111"
    ]

    def __init__(self, width, height):
        self.width = len(self.STATIC_PATTERN[0])  # Width is fixed by the pattern
        self.height = len(self.STATIC_PATTERN)    # Height is fixed by the pattern
        self.grid = np.full((self.height, self.width), WALL, dtype=str)
        self.start_pos = (11, 0)  # Position where the pattern has the entrance
        self.end_pos = (1, self.height-2)  # Position near the bottom
        self.generate_static_maze()
        self.grid[self.start_pos[1], self.start_pos[0]] = START
        self.grid[self.end_pos[1], self.end_pos[0]] = END

    def generate_static_maze(self) -> None:
        """Generate the predefined static maze pattern."""
        for y, row in enumerate(self.STATIC_PATTERN):
            for x, cell in enumerate(row):
                self.grid[y, x] = cell


def create_maze(width, height, maze_type="random"):
    """Create a maze of the specified type."""
    if maze_type == "static":
        return StaticMaze(width, height)  # width and height are ignored for static maze
    return Maze(width, height) 