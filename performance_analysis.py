"""
Performance analysis script for comparing different maze explorers.
"""

import time
import numpy as np
import matplotlib.pyplot as plt
from src.maze import create_maze
from src.explorer import Explorer
from src.enhanced_explorer import EnhancedExplorer

def run_performance_test(maze_type: str = "static", num_runs: int = 10):
    """
    Run performance tests on different explorers and collect statistics.
    """
    print(f"\n=== Performance Analysis for {maze_type} Maze ===")
    print(f"Number of runs: {num_runs}\n")
    
    # Initialize statistics storage
    original_stats = {
        'times': [],
        'moves': [],
        'backtracks': [],
        'moves_per_second': []
    }
    
    enhanced_stats = {
        'times': [],
        'moves': [],
        'backtracks': [],
        'moves_per_second': []
    }
    
    # Run tests
    for run in range(num_runs):
        print(f"Run {run + 1}/{num_runs}")
        
        # Create maze
        maze = create_maze(50, 50, maze_type)
        
        # Test original explorer
        original = Explorer(maze, visualize=False)
        start_time = time.perf_counter()
        path, moves = original.solve()
        original_time = time.perf_counter() - start_time
        original_stats['times'].append(original_time)
        original_stats['moves'].append(len(moves))
        original_stats['backtracks'].append(original.backtrack_count)
        original_stats['moves_per_second'].append(len(moves) / original_time if original_time > 0 else 0)
        
        # Test enhanced explorer
        enhanced = EnhancedExplorer(maze, visualize=False)
        start_time = time.perf_counter()
        path, moves = enhanced.solve()
        enhanced_time = time.perf_counter() - start_time
        enhanced_stats['times'].append(enhanced_time)
        enhanced_stats['moves'].append(len(moves))
        enhanced_stats['backtracks'].append(enhanced.backtrack_count)
        enhanced_stats['moves_per_second'].append(len(moves) / enhanced_time if enhanced_time > 0 else 0)
    
    return original_stats, enhanced_stats

def analyze_results(original_stats, enhanced_stats):
    """
    Analyze and display the performance comparison results.
    """
    print("\n=== Performance Analysis Results ===")
    
    # Calculate statistics
    metrics = ['times', 'moves', 'backtracks', 'moves_per_second']
    metric_names = ['Time (s)', 'Moves', 'Backtracks', 'Moves/Second']
    
    for metric, name in zip(metrics, metric_names):
        orig_mean = np.mean(original_stats[metric])
        orig_std = np.std(original_stats[metric])
        enh_mean = np.mean(enhanced_stats[metric])
        enh_std = np.std(enhanced_stats[metric])
        
        print(f"\n{name}:")
        print(f"  Original Explorer: {orig_mean:.2f} ± {orig_std:.2f}")
        print(f"  Enhanced Explorer: {enh_mean:.2f} ± {enh_std:.2f}")
        print(f"  Improvement: {((orig_mean - enh_mean) / orig_mean * 100):.1f}%")
    
    # Plot results
    plt.figure(figsize=(15, 10))
    
    for i, (metric, name) in enumerate(zip(metrics, metric_names)):
        plt.subplot(2, 2, i + 1)
        plt.boxplot([original_stats[metric], enhanced_stats[metric]], 
                   labels=['Original', 'Enhanced'])
        plt.title(f'{name} Comparison')
        plt.ylabel(name)
    
    plt.tight_layout()
    plt.savefig('performance_comparison.png')
    print("\nPerformance comparison plot saved as 'performance_comparison.png'")

def main():
    # Run performance tests
    original_stats, enhanced_stats = run_performance_test()
    
    # Analyze and display results
    analyze_results(original_stats, enhanced_stats)

if __name__ == "__main__":
    main() 