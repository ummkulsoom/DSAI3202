"""
Optimized explorer specifically designed for the static maze.
"""

from typing import List, Tuple, Dict, Set
import heapq
import time
import numpy as np
from .explorer import Explorer
from .maze import Maze

class OptimizedExplorer(Explorer):
    def __init__(self, maze: Maze):
        super().__init__(maze)
        self.visited = set()
        self.path = []
        self.moves = 0
        self.backtrack_count = 0
        self.min_path_length = float('inf')
        self.best_path = None
        self.target_moves = 130  # Target for 100% score
        
    def manhattan_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """Calculate Manhattan distance between two points"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
        
    def diagonal_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """Calculate diagonal distance between two points"""
        dx = abs(pos1[0] - pos2[0])
        dy = abs(pos1[1] - pos2[1])
        return max(dx, dy)
        
    def euclidean_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """Calculate Euclidean distance between two points"""
        return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5
        
    def combined_heuristic(self, pos: Tuple[int, int], end_pos: Tuple[int, int], current_path_length: int) -> float:
        """Optimized heuristic for minimal moves"""
        # Base distance heuristic
        manhattan = self.manhattan_distance(pos, end_pos)
        
        # Penalize paths that are already too long
        if current_path_length > self.target_moves:
            return float('inf')
            
        # Penalize backtracking
        if pos in self.visited:
            return float('inf')
            
        # Prefer straight paths
        if len(self.path) >= 2:
            prev_pos = self.path[-1]
            prev_prev_pos = self.path[-2]
            if (pos[0] == prev_pos[0] == prev_prev_pos[0] or 
                pos[1] == prev_pos[1] == prev_prev_pos[1]):
                return manhattan * 0.9  # Slight preference for straight paths
                
        return manhattan
        
    def get_neighbors_optimized(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get valid neighboring positions with optimized ordering"""
        x, y = pos
        # Order neighbors based on likely direction to goal
        dx = self.maze.end_pos[0] - x
        dy = self.maze.end_pos[1] - y
        
        # Prioritize moves in the direction of the goal
        neighbors = []
        if dx > 0:
            neighbors.append((x + 1, y))
        if dx < 0:
            neighbors.append((x - 1, y))
        if dy > 0:
            neighbors.append((x, y + 1))
        if dy < 0:
            neighbors.append((x, y - 1))
            
        # Add remaining moves
        all_moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in all_moves:
            new_pos = (x + dx, y + dy)
            if new_pos not in neighbors:
                neighbors.append(new_pos)
                
        # Filter valid moves and avoid backtracking
        return [n for n in neighbors if (
            0 <= n[0] < self.maze.width and 
            0 <= n[1] < self.maze.height and 
            not self.maze.is_wall(n) and
            n not in self.visited
        )]
        
    def optimize_path(self, path: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """Optimize path by removing unnecessary moves"""
        if not path:
            return []
            
        optimized = [path[0]]
        i = 1
        while i < len(path):
            # Look ahead for optimization opportunities
            if i < len(path) - 2:
                prev = path[i-1]
                curr = path[i]
                next_pos = path[i+1]
                next_next = path[i+2]
                
                # Check for diagonal shortcuts
                if (abs(prev[0] - next_next[0]) == 1 and 
                    abs(prev[1] - next_next[1]) == 1 and
                    not self.maze.is_wall(next_next)):
                    optimized.append(next_next)
                    i += 3
                    continue
                
                # Check for straight line moves
                if ((abs(prev[0] - next_next[0]) == 2 and 
                     curr[0] == (prev[0] + next_next[0])//2 and 
                     curr[1] == prev[1] == next_next[1]) or
                    (abs(prev[1] - next_next[1]) == 2 and 
                     curr[1] == (prev[1] + next_next[1])//2 and 
                     curr[0] == prev[0] == next_next[0])):
                    optimized.append(next_next)
                    i += 3
                    continue
            
            optimized.append(path[i])
            i += 1
            
        return optimized
        
    def a_star_search(self) -> List[Tuple[int, int]]:
        """Optimized A* search for the static maze"""
        open_set = []
        closed_set = set()
        heapq.heappush(open_set, (0, self.maze.start_pos))
        
        came_from = {}
        g_score = {self.maze.start_pos: 0}
        f_score = {
            self.maze.start_pos: self.combined_heuristic(
                self.maze.start_pos, 
                self.maze.end_pos,
                0
            )
        }
        
        while open_set:
            current_f, current = heapq.heappop(open_set)
            
            if current == self.maze.end_pos:
                # Reconstruct path
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(self.maze.start_pos)
                path.reverse()
                
                # Optimize path
                optimized = self.optimize_path(path)
                if len(optimized) < self.min_path_length:
                    self.best_path = optimized
                    self.min_path_length = len(optimized)
                    
                    # Early termination if path is good enough
                    if len(optimized) <= self.target_moves:
                        return optimized
                continue
            
            closed_set.add(current)
            self.visited.add(current)
            
            for neighbor in self.get_neighbors_optimized(current):
                if neighbor in closed_set:
                    continue
                    
                tentative_g_score = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = (
                        tentative_g_score + 
                        self.combined_heuristic(neighbor, self.maze.end_pos, tentative_g_score)
                    )
                    
                    if neighbor not in [item[1] for item in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        return self.best_path if self.best_path else []
        
    def solve(self) -> Dict:
        """Solve the maze using optimized A* search"""
        start_time = time.time()
        path = self.a_star_search()
        end_time = time.time()
        
        if path:
            self.path = path
            self.moves = len(path) - 1
        
        return {
            'time': end_time - start_time,
            'moves': self.moves,
            'path_length': len(path) if path else 0,
            'nodes_explored': len(self.visited),
            'backtrack_count': self.backtrack_count
        } 