"""
Compare the optimized explorer with the original explorer.
"""

import time
from src.maze import create_maze
from src.explorer import Explorer
from src.optimized_explorer import OptimizedExplorer

def run_comparison(num_runs: int = 5):
    """Run comparison between original and optimized explorers"""
    original_results = []
    optimized_results = []
    
    print("\nRunning comparison between original and optimized explorers...")
    print("=" * 60)
    
    for run in range(num_runs):
        print(f"\nRun {run + 1}/{num_runs}")
        
        # Create a new maze for each run
        maze = create_maze(64, 64, maze_type="static")
        
        # Test original explorer
        print("\nRunning original explorer...")
        original = Explorer(maze)
        original_stats = original.solve()
        original_results.append(original_stats)
        
        # Test optimized explorer
        print("\nRunning optimized explorer...")
        optimized = OptimizedExplorer(maze)
        optimized_stats = optimized.solve()
        optimized_results.append(optimized_stats)
        
        # Print run results
        print("\nRun Results:")
        print("-" * 20)
        print("Original Explorer:")
        print(f"Time: {original_stats['time']:.6f} seconds")
        print(f"Path length: {original_stats['path_length']} steps")
        print(f"Nodes explored: {original_stats['nodes_explored']}")
        
        print("\nOptimized Explorer:")
        print(f"Time: {optimized_stats['time']:.6f} seconds")
        print(f"Path length: {optimized_stats['path_length']} steps")
        print(f"Nodes explored: {optimized_stats['nodes_explored']}")
        print(f"Backtrack count: {optimized_stats['backtrack_count']}")
    
    # Calculate and print average results
    print("\nFinal Results:")
    print("=" * 60)
    
    # Original explorer averages
    avg_original_time = sum(r['time'] for r in original_results) / num_runs
    avg_original_length = sum(r['path_length'] for r in original_results) / num_runs
    avg_original_nodes = sum(r['nodes_explored'] for r in original_results) / num_runs
    
    print("\nOriginal Explorer Averages:")
    print(f"Time: {avg_original_time:.6f} seconds")
    print(f"Path length: {avg_original_length:.1f} steps")
    print(f"Nodes explored: {avg_original_nodes:.1f}")
    
    # Optimized explorer averages
    avg_optimized_time = sum(r['time'] for r in optimized_results) / num_runs
    avg_optimized_length = sum(r['path_length'] for r in optimized_results) / num_runs
    avg_optimized_nodes = sum(r['nodes_explored'] for r in optimized_results) / num_runs
    avg_backtrack = sum(r['backtrack_count'] for r in optimized_results) / num_runs
    
    print("\nOptimized Explorer Averages:")
    print(f"Time: {avg_optimized_time:.6f} seconds")
    print(f"Path length: {avg_optimized_length:.1f} steps")
    print(f"Nodes explored: {avg_optimized_nodes:.1f}")
    print(f"Backtrack count: {avg_backtrack:.1f}")
    
    # Calculate improvements
    time_improvement = ((avg_original_time - avg_optimized_time) / avg_original_time) * 100
    length_improvement = ((avg_original_length - avg_optimized_length) / avg_original_length) * 100
    nodes_improvement = ((avg_original_nodes - avg_optimized_nodes) / avg_original_nodes) * 100
    
    print("\nImprovements:")
    print(f"Time: {time_improvement:+.1f}%")
    print(f"Path length: {length_improvement:+.1f}%")
    print(f"Nodes explored: {nodes_improvement:+.1f}%")

if __name__ == "__main__":
    run_comparison() 