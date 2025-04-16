"""
Maze Explorer module that implements automated maze solving.
"""

from typing import List, Tuple, Dict, Set
import heapq
import time
from .maze import Maze

class Explorer:
    def __init__(self, maze: Maze, heuristic_type: str = "manhattan"):
        self.maze = maze
        self.position = maze.start_pos
        self.heuristic_type = heuristic_type
        self.moves = 0
        self.visited: Set[Tuple[int, int]] = set()
        self.path: List[Tuple[int, int]] = []

    def manhattan_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """Calculate Manhattan distance between two positions"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def euclidean_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """Calculate Euclidean distance between two positions"""
        return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

    def diagonal_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """Calculate diagonal distance between two positions"""
        dx = abs(pos1[0] - pos2[0])
        dy = abs(pos1[1] - pos2[1])
        return max(dx, dy) + (2 ** 0.5 - 1) * min(dx, dy)

    def get_heuristic(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """Get heuristic value based on selected type"""
        if self.heuristic_type == "manhattan":
            return self.manhattan_distance(pos1, pos2)
        elif self.heuristic_type == "euclidean":
            return self.euclidean_distance(pos1, pos2)
        elif self.heuristic_type == "diagonal":
            return self.diagonal_distance(pos1, pos2)
        else:
            return self.manhattan_distance(pos1, pos2)  # Default to Manhattan

    def a_star_search(self) -> List[Tuple[int, int]]:
        """A* search algorithm with selected heuristic"""
        open_set = []
        heapq.heappush(open_set, (0, self.maze.start_pos))
        
        came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
        g_score: Dict[Tuple[int, int], float] = {self.maze.start_pos: 0}
        f_score: Dict[Tuple[int, int], float] = {
            self.maze.start_pos: self.get_heuristic(self.maze.start_pos, self.maze.end_pos)
        }
        
        while open_set:
            current = heapq.heappop(open_set)[1]
            self.visited.add(current)
            
            if current == self.maze.end_pos:
                # Reconstruct path
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(self.maze.start_pos)
                path.reverse()
                return path
            
            for neighbor in self.maze.get_neighbors(current):
                tentative_g_score = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.get_heuristic(neighbor, self.maze.end_pos)
                    
                    if neighbor not in [item[1] for item in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        return []  # No path found

    def solve(self) -> Dict:
        """Solve the maze using A* search"""
        start_time = time.time()
        path = self.a_star_search()
        end_time = time.time()
        
        if path:
            self.path = path
            self.moves = len(path) - 1  # Subtract 1 because start position doesn't count as a move
            
        return {
            'time': end_time - start_time,
            'moves': self.moves,
            'path_length': len(path) if path else 0,
            'nodes_explored': len(self.visited)
        } 