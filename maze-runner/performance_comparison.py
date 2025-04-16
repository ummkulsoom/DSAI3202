"""
Script to compare performance of original and enhanced maze explorers.
"""

import time
from src.maze import create_maze
from src.explorer import Explorer
from src.enhanced_explorer import EnhancedExplorer

def run_simple_comparison(maze_type: str = "static", num_runs: int = 3):
    """Run a simple performance comparison between explorers"""
    print("\n=== Simple Performance Comparison ===")
    print(f"Maze Type: {maze_type}")
    print(f"Number of Runs: {num_runs}\n")
    
    for run in range(num_runs):
        print(f"Run {run + 1}/{num_runs}")
        
        # Create maze
        maze = create_maze(50, 50, maze_type)
        
        # Test original explorer
        print("  Original Explorer:")
        original = Explorer(maze, visualize=False)
        start_time = time.time()
        path, moves = original.solve()
        original_time = time.time() - start_time
        original_stats = original.print_statistics(original_time)
        print(f"    Time: {original_time:.4f}s")
        print(f"    Moves: {len(moves)}")
        print(f"    Path Length: {len(path)}")
        
        # Test enhanced explorer
        print("  Enhanced Explorer:")
        enhanced = EnhancedExplorer(maze, visualize=False)
        start_time = time.time()
        path, moves = enhanced.solve()
        enhanced_time = time.time() - start_time
        enhanced_stats = enhanced.print_statistics(enhanced_time)
        print(f"    Time: {enhanced_time:.4f}s")
        print(f"    Moves: {len(moves)}")
        print(f"    Path Length: {len(path)}")
        
        # Print comparison for this run
        time_diff = (original_time - enhanced_time) / original_time * 100
        moves_diff = (len(original.moves) - len(moves)) / len(original.moves) * 100
        print(f"\n  Comparison for Run {run + 1}:")
        print(f"    Time Improvement: {time_diff:.1f}%")
        print(f"    Moves Reduction: {moves_diff:.1f}%")
        print("-" * 50)

if __name__ == "__main__":
    run_simple_comparison(maze_type="static", num_runs=3) 