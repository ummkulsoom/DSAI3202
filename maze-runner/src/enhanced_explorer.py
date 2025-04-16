"""
Enhanced maze explorer with optimized pathfinding capabilities.
Implements the following improvements:
1. Selective topology analysis
2. Efficient memory management
3. Optimized heuristic combination
4. Early termination for optimal paths
"""

from typing import List, Tuple, Dict, Set
import heapq
import time
import numpy as np
from .explorer import Explorer
from .maze import Maze

class EnhancedExplorer(Explorer):
    def __init__(self, maze: Maze):
        super().__init__(maze)
        # Memory of explored paths (limited size)
        self.path_memory: Dict[Tuple[int, int], Dict] = {}
        self.max_memory_size = 100  # Limit memory size
        # Local topology analysis
        self.local_junctions: Set[Tuple[int, int]] = set()
        self.analysis_radius = 5  # Only analyze within this radius
        # Optimized heuristic weights for minimal moves
        self.distance_weight = 0.9  # Increased weight for distance
        self.topology_weight = 0.1  # Reduced weight for topology
        # Track backtracking
        self.backtrack_count = 0
        self.last_position = None
        # Path optimization
        self.min_path_length = float('inf')
        self.best_path = None
        
    def analyze_local_topology(self, center_pos: Tuple[int, int]):
        """Analyze maze topology only in the vicinity of current position"""
        self.local_junctions.clear()
        x, y = center_pos
        
        # Only analyze within the specified radius
        for dy in range(-self.analysis_radius, self.analysis_radius + 1):
            for dx in range(-self.analysis_radius, self.analysis_radius + 1):
                pos = (x + dx, y + dy)
                if (0 <= x + dx < self.maze.width and 
                    0 <= y + dy < self.maze.height and 
                    not self.maze.is_wall(pos)):
                    neighbors = self.maze.get_neighbors(pos)
                    if len(neighbors) > 2:  # Junction point
                        self.local_junctions.add(pos)

    def topology_heuristic(self, pos: Tuple[int, int]) -> float:
        """Calculate simplified topology-based heuristic"""
        if not self.local_junctions:
            return 0.0
            
        # Find distance to nearest junction
        min_dist = float('inf')
        for junction in self.local_junctions:
            dist = self.manhattan_distance(pos, junction)
            min_dist = min(min_dist, dist)
        
        return min_dist * 0.5

    def update_memory(self, path: List[Tuple[int, int]], success: bool):
        """Update path memory with size limit"""
        # Only store critical decision points (junctions)
        critical_points = [pos for pos in path if pos in self.local_junctions]
        
        for pos in critical_points:
            if pos not in self.path_memory:
                # If memory is full, remove oldest entry
                if len(self.path_memory) >= self.max_memory_size:
                    oldest_pos = min(self.path_memory.items(), 
                                   key=lambda x: x[1]['last_visit'])[0]
                    del self.path_memory[oldest_pos]
                
                self.path_memory[pos] = {
                    'visits': 0,
                    'successful_visits': 0,
                    'last_visit': time.time()
                }
            
            memory = self.path_memory[pos]
            memory['visits'] += 1
            memory['last_visit'] = time.time()
            if success:
                memory['successful_visits'] += 1

    def optimize_path(self, path: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """Optimize path to minimize moves and eliminate backtracking"""
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
                
                # Check for diagonal moves (2x2 grid)
                if (abs(prev[0] - next_next[0]) == 1 and abs(prev[1] - next_next[1]) == 1 and
                    curr[0] == prev[0] and curr[1] == next_next[1] and
                    next_pos[0] == next_next[0] and next_pos[1] == prev[1]):
                    optimized.append(next_next)
                    i += 3
                    continue
                
                # Check for straight line moves (3x1 or 1x3 grid)
                if (abs(prev[0] - next_next[0]) == 2 and curr[0] == (prev[0] + next_next[0])//2 and 
                    curr[1] == prev[1] == next_next[1]) or \
                   (abs(prev[1] - next_next[1]) == 2 and curr[1] == (prev[1] + next_next[1])//2 and 
                    curr[0] == prev[0] == next_next[0]):
                    optimized.append(next_next)
                    i += 3
                    continue
                
                # Check for L-shaped moves (2x2 grid with one turn)
                if i < len(path) - 3:
                    next_next_next = path[i+3]
                    if (abs(prev[0] - next_next_next[0]) == 2 and abs(prev[1] - next_next_next[1]) == 2 and
                        curr[0] == prev[0] and curr[1] == next_next[1] and
                        next_pos[0] == next_next[0] and next_pos[1] == next_next[1] and
                        next_next[0] == next_next_next[0] and next_next[1] == prev[1]):
                        optimized.append(next_next_next)
                        i += 4
                        continue
            
            optimized.append(path[i])
            i += 1
            
        return optimized

    def adaptive_heuristic(self, pos: Tuple[int, int], end_pos: Tuple[int, int]) -> float:
        """Optimized heuristic for minimal moves"""
        # Base distance heuristic (Manhattan distance is admissible)
        distance_cost = self.manhattan_distance(pos, end_pos)
        
        # Early termination optimization: if we're at a dead end, increase cost
        neighbors = self.maze.get_neighbors(pos)
        if len(neighbors) == 1 and pos != self.maze.end_pos:
            return float('inf')  # Dead end that's not the goal
        
        # Penalize backtracking
        if self.last_position and pos == self.last_position:
            return float('inf')
        
        # Topology-based cost (minimal importance)
        topology_cost = self.topology_heuristic(pos) * 0.2
        
        # Memory-based cost (minimal importance)
        memory_cost = 0.0
        if pos in self.path_memory:
            memory_info = self.path_memory[pos]
            success_ratio = memory_info['successful_visits'] / memory_info['visits']
            memory_cost = (1 - success_ratio) * 2  # Minimal penalty
        
        # Combine costs with optimized weights
        return (
            self.distance_weight * distance_cost +
            self.topology_weight * topology_cost +
            0.02 * memory_cost  # Minimal memory weight
        )

    def reconstruct_path(self, came_from: Dict[Tuple[int, int], Tuple[int, int]], current: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Reconstruct path from came_from dictionary"""
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.append(self.maze.start_pos)
        path.reverse()
        return path

    def a_star_search(self) -> List[Tuple[int, int]]:
        """Optimized A* search with early termination conditions"""
        open_set = []
        closed_set = set()  # Track explored nodes
        heapq.heappush(open_set, (0, self.maze.start_pos))
        
        came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
        g_score: Dict[Tuple[int, int], float] = {self.maze.start_pos: 0}
        f_score: Dict[Tuple[int, int], float] = {
            self.maze.start_pos: self.adaptive_heuristic(self.maze.start_pos, self.maze.end_pos)
        }
        
        while open_set:
            current_f, current = heapq.heappop(open_set)
            
            # Early termination if we've found a path better than our target
            if self.best_path and len(self.optimize_path(self.best_path)) <= 130:
                return self.optimize_path(self.best_path)
            
            # Add to closed set and visited nodes
            closed_set.add(current)
            self.visited.add(current)
            
            # Update last position and check for backtracking
            if self.last_position and current == self.last_position:
                self.backtrack_count += 1
            self.last_position = current
            
            # Analyze local topology around current position
            if len(self.maze.get_neighbors(current)) > 2:  # Only analyze at junctions
                self.analyze_local_topology(current)
            
            if current == self.maze.end_pos:
                path = self.reconstruct_path(came_from, current)
                optimized_path = self.optimize_path(path)
                
                # Update best path if this is better
                if len(optimized_path) < self.min_path_length:
                    self.best_path = path
                    self.min_path_length = len(optimized_path)
                    
                    # Early termination if we've found a path better than our target
                    if len(optimized_path) <= 130:
                        return optimized_path
                continue
            
            for neighbor in self.maze.get_neighbors(current):
                if neighbor in closed_set:
                    continue
                    
                tentative_g_score = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = (
                        tentative_g_score + 
                        self.adaptive_heuristic(neighbor, self.maze.end_pos)
                    )
                    
                    if neighbor not in [item[1] for item in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        # If we found any path, return the best one
        if self.best_path:
            return self.optimize_path(self.best_path)
            
        self.update_memory(list(self.visited), False)
        return []

    def solve(self) -> Dict:
        """Solve the maze using optimized A* search"""
        start_time = time.time()
        path = self.a_star_search()
        end_time = time.time()
        
        if path:
            self.path = path
            self.moves = len(path) - 1
        
        stats = {
            'time': end_time - start_time,
            'moves': self.moves,
            'path_length': len(path) if path else 0,
            'nodes_explored': len(self.visited),
            'memory_size': len(self.path_memory),
            'backtrack_count': self.backtrack_count
        }
        
        return stats 