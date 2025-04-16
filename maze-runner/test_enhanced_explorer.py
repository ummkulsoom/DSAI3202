"""
Test script to compare the performance of original and enhanced explorers.
"""

import time
from src.maze import create_maze
from src.explorer import Explorer
from src.enhanced_explorer import EnhancedExplorer

def run_comparison(maze_type="static", num_runs=5):
    """Run comparison between original and enhanced explorers"""
    print(f"\nRunning comparison for {maze_type} maze type...")
    print(f"Number of runs: {num_runs}\n")
    
    # Create maze with correct argument order (width, height, maze_type)
    maze = create_maze(20, 20, maze_type)
    
    # Initialize explorers with visualize=False
    original_explorer = Explorer(maze, visualize=False)
    enhanced_explorer = EnhancedExplorer(maze, visualize=False)
    
    # Statistics
    original_stats = []
    enhanced_stats = []
    
    for run in range(1, num_runs + 1):
        print(f"\nRun {run}/{num_runs}")
        
        # Run original explorer
        print("Running original explorer...")
        start_time = time.time()
        time_taken, moves = original_explorer.solve()
        original_time = time.time() - start_time
        print(f"Original explorer completed in {original_time:.2f} seconds")
        
        # Run enhanced explorer
        print("Running enhanced explorer...")
        start_time = time.time()
        enhanced_result = enhanced_explorer.explore()  # explore() returns a dict with stats
        enhanced_time = time.time() - start_time
        print(f"Enhanced explorer completed in {enhanced_time:.2f} seconds")
        
        # Collect statistics
        original_stats.append({
            'time': original_time,
            'moves': len(moves),  # moves is a list of positions
            'path_length': len(moves)
        })
        
        enhanced_stats.append({
            'time': enhanced_time,
            'moves': enhanced_result['moves'],
            'path_length': enhanced_result['moves']  # In enhanced explorer, moves = path length
        })
    
    # Calculate averages
    def calculate_averages(stats):
        return {
            'avg_time': sum(s['time'] for s in stats) / len(stats),
            'avg_moves': sum(s['moves'] for s in stats) / len(stats),
            'avg_path_length': sum(s['path_length'] for s in stats) / len(stats)
        }
    
    original_avg = calculate_averages(original_stats)
    enhanced_avg = calculate_averages(enhanced_stats)
    
    # Print results
    print("\nResults:")
    print("Original Explorer:")
    print(f"  Average Time: {original_avg['avg_time']:.4f} seconds")
    print(f"  Average Moves: {original_avg['avg_moves']:.1f}")
    print(f"  Average Path Length: {original_avg['avg_path_length']:.1f}")
    
    print("\nEnhanced Explorer:")
    print(f"  Average Time: {enhanced_avg['avg_time']:.4f} seconds")
    print(f"  Average Moves: {enhanced_avg['avg_moves']:.1f}")
    print(f"  Average Path Length: {enhanced_avg['avg_path_length']:.1f}")
    
    # Calculate improvements
    time_improvement = (original_avg['avg_time'] - enhanced_avg['avg_time']) / original_avg['avg_time'] * 100
    moves_improvement = (original_avg['avg_moves'] - enhanced_avg['avg_moves']) / original_avg['avg_moves'] * 100
    path_improvement = (original_avg['avg_path_length'] - enhanced_avg['avg_path_length']) / original_avg['avg_path_length'] * 100
    
    print("\nImprovements:")
    print(f"  Time: {time_improvement:.1f}% {'faster' if time_improvement > 0 else 'slower'}")
    print(f"  Moves: {moves_improvement:.1f}% {'better' if moves_improvement > 0 else 'worse'}")
    print(f"  Path Length: {path_improvement:.1f}% {'better' if path_improvement > 0 else 'worse'}")

if __name__ == "__main__":
    run_comparison() 