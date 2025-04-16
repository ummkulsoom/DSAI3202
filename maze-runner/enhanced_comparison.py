"""
Compare the enhanced explorer with the original explorer.
"""

import time
from src.maze import create_maze
from src.explorer import Explorer
from src.enhanced_explorer import EnhancedExplorer

def run_comparison(num_runs: int = 5):
    """Run comparison between original and enhanced explorers"""
    original_results = []
    enhanced_results = []
    
    print("\nRunning comparison between original and enhanced explorers...")
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
        
        # Test enhanced explorer
        print("\nRunning enhanced explorer...")
        enhanced = EnhancedExplorer(maze)
        enhanced_stats = enhanced.solve()
        enhanced_results.append(enhanced_stats)
        
        # Print run results
        print("\nRun Results:")
        print("-" * 20)
        print("Original Explorer:")
        print(f"Time: {original_stats['time']:.6f} seconds")
        print(f"Path length: {original_stats['path_length']} steps")
        print(f"Nodes explored: {original_stats['nodes_explored']}")
        
        print("\nEnhanced Explorer:")
        print(f"Time: {enhanced_stats['time']:.6f} seconds")
        print(f"Path length: {enhanced_stats['path_length']} steps")
        print(f"Nodes explored: {enhanced_stats['nodes_explored']}")
        print(f"Memory size: {enhanced_stats['memory_size']}")
    
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
    
    # Enhanced explorer averages
    avg_enhanced_time = sum(r['time'] for r in enhanced_results) / num_runs
    avg_enhanced_length = sum(r['path_length'] for r in enhanced_results) / num_runs
    avg_enhanced_nodes = sum(r['nodes_explored'] for r in enhanced_results) / num_runs
    avg_memory = sum(r['memory_size'] for r in enhanced_results) / num_runs
    
    print("\nEnhanced Explorer Averages:")
    print(f"Time: {avg_enhanced_time:.6f} seconds")
    print(f"Path length: {avg_enhanced_length:.1f} steps")
    print(f"Nodes explored: {avg_enhanced_nodes:.1f}")
    print(f"Memory size: {avg_memory:.1f}")
    
    # Calculate improvements
    time_improvement = ((avg_original_time - avg_enhanced_time) / avg_original_time) * 100
    length_improvement = ((avg_original_length - avg_enhanced_length) / avg_original_length) * 100
    nodes_improvement = ((avg_original_nodes - avg_enhanced_nodes) / avg_original_nodes) * 100
    
    print("\nImprovements:")
    print(f"Time: {time_improvement:+.1f}%")
    print(f"Path length: {length_improvement:+.1f}%")
    print(f"Nodes explored: {nodes_improvement:+.1f}%")

if __name__ == "__main__":
    run_comparison() 