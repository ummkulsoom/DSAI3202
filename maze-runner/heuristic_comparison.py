"""
Compare different heuristic functions for A* pathfinding.
"""

import time
import pygame
import numpy as np
from src.maze import create_maze, Maze
from src.explorer import Explorer
from src.constants import CELL_SIZE, WINDOW_SIZE, Direction

class HeuristicExplorer(Explorer):
    def __init__(self, maze, heuristic_type):
        super().__init__(maze)
        self.heuristic_type = heuristic_type
        self.nodes_explored = 0
        
    def _heuristic(self, pos):
        """Calculate heuristic based on the specified type"""
        self.nodes_explored += 1
        dx = abs(pos[0] - self.maze.end_pos[0])
        dy = abs(pos[1] - self.maze.end_pos[1])
        
        if self.heuristic_type == "manhattan":
            return dx + dy
        elif self.heuristic_type == "euclidean":
            return (dx**2 + dy**2)**0.5
        elif self.heuristic_type == "diagonal":
            return max(dx, dy) + (2**0.5 - 1) * min(dx, dy)
        else:
            return dx + dy  # Default to Manhattan

    def solve(self):
        """Solve the maze using A* with the specified heuristic"""
        start_time = time.time()
        path = self.a_star_search()
        time_taken = time.time() - start_time
        
        if path:
            moves = []
            for i in range(len(path) - 1):
                current = path[i]
                next_pos = path[i + 1]
                if next_pos[0] > current[0]:
                    moves.append(Direction.RIGHT)
                elif next_pos[0] < current[0]:
                    moves.append(Direction.LEFT)
                elif next_pos[1] > current[1]:
                    moves.append(Direction.DOWN)
                else:
                    moves.append(Direction.UP)
            
            return {
                'time_taken': time_taken,
                'path_length': len(moves),
                'nodes_explored': self.nodes_explored,
                'moves_per_second': len(moves) / time_taken if time_taken > 0 else 0,
                'path': path
            }
        return None

def run_heuristic_comparison(num_runs=10, width=30, height=30):
    """Run comparison of different heuristics"""
    results = {
        'manhattan': [],
        'euclidean': [],
        'diagonal': []
    }
    
    for _ in range(num_runs):
        maze = create_maze(width=width, height=height, maze_type="static")
        
        for heuristic in results.keys():
            explorer = HeuristicExplorer(maze, heuristic)
            result = explorer.solve()
            if result:
                results[heuristic].append(result)
    
    return results

def analyze_heuristic_results(results):
    """Analyze and display comparison results"""
    print("\n=== Detailed Heuristic Comparison Results ===\n")
    
    for heuristic, runs in results.items():
        if not runs:
            continue
            
        times = [r['time_taken'] for r in runs]
        lengths = [r['path_length'] for r in runs]
        nodes = [r['nodes_explored'] for r in runs]
        mps = [r['moves_per_second'] for r in runs]
        
        print(f"\n{heuristic.capitalize()} Heuristic:")
        print(f"Average time: {sum(times)/len(times):.6f} seconds")
        print(f"Average path length: {sum(lengths)/len(lengths):.1f} steps")
        print(f"Average nodes explored: {sum(nodes)/len(nodes):.1f}")
        print(f"Average moves per second: {sum(mps)/len(mps):.1f}")
    
    # Find best performers
    best_time = min([sum([r['time_taken'] for r in runs])/len(runs) for runs in results.values() if runs])
    best_length = min([sum([r['path_length'] for r in runs])/len(runs) for runs in results.values() if runs])
    best_mps = max([sum([r['moves_per_second'] for r in runs])/len(runs) for runs in results.values() if runs])
    
    print("\n=== Summary ===")
    for heuristic, runs in results.items():
        if not runs:
            continue
        avg_time = sum([r['time_taken'] for r in runs])/len(runs)
        avg_length = sum([r['path_length'] for r in runs])/len(runs)
        avg_mps = sum([r['moves_per_second'] for r in runs])/len(runs)
        
        print(f"\n{heuristic.capitalize()}:")
        print(f"Time: {'✓' if abs(avg_time - best_time) < 1e-6 else '✗'} ({avg_time:.6f}s)")
        print(f"Path length: {'✓' if abs(avg_length - best_length) < 1e-6 else '✗'} ({avg_length:.1f} steps)")
        print(f"Moves per second: {'✓' if abs(avg_mps - best_mps) < 1e-6 else '✗'} ({avg_mps:.1f})")

def compare_heuristics():
    # Create maze
    maze = create_maze(64, 64, maze_type="static")
    
    # Define heuristics to compare
    heuristics = ["manhattan", "euclidean", "diagonal"]
    results = {}
    
    print("\nComparing heuristics for static maze...")
    print("=" * 50)
    
    for heuristic in heuristics:
        print(f"\nRunning {heuristic.capitalize()} heuristic...")
        explorer = Explorer(maze, heuristic_type=heuristic)
        stats = explorer.solve()
        
        results[heuristic] = stats
        print(f"Time taken: {stats['time']:.6f} seconds")
        print(f"Path length: {stats['path_length']}")
        print(f"Nodes explored: {stats['nodes_explored']}")
    
    # Print summary
    print("\nSummary:")
    print("=" * 50)
    
    # Find best performers
    fastest = min(results.items(), key=lambda x: x[1]['time'])
    shortest = min(results.items(), key=lambda x: x[1]['path_length'])
    
    print(f"\nFastest heuristic: {fastest[0].capitalize()} ({fastest[1]['time']:.6f} seconds)")
    print(f"Shortest path: {shortest[0].capitalize()} ({shortest[1]['path_length']} steps)")

if __name__ == "__main__":
    compare_heuristics() 