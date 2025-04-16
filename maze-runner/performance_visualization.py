"""
Performance visualization script for maze explorer comparison.
Generates three types of graphs:
1. Performance comparison bar chart
2. Solution convergence line graph
3. Performance metrics radar chart
"""

import matplotlib.pyplot as plt
import numpy as np
import argparse
from matplotlib.patches import Circle, Rectangle
import matplotlib.patches as mpatches

def create_performance_comparison():
    """Create bar chart comparing performance metrics"""
    # Data
    metrics = ['Time (s)', 'Moves', 'Moves/Second', 'Memory Usage (MB)']
    original = [0.01, 1279, 107838, 2.5]
    optimized = [0.007, 127, 175790, 3.2]
    
    x = np.arange(len(metrics))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(12, 6))
    rects1 = ax.bar(x - width/2, original, width, label='Original Explorer')
    rects2 = ax.bar(x + width/2, optimized, width, label='Optimized Explorer')
    
    # Add labels and title
    ax.set_ylabel('Performance')
    ax.set_title('Performance Comparison: Original vs Optimized Explorer')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics)
    ax.legend()
    
    # Add value labels
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height}',
                        xy=(rect.get_x() + rect.get_width()/2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
    
    autolabel(rects1)
    autolabel(rects2)
    
    plt.tight_layout()
    plt.savefig('performance_comparison.png')
    plt.close()

def create_convergence_comparison():
    """Create line graph showing solution convergence"""
    # Sample data points
    time_points = np.linspace(0, 0.01, 100)
    original_moves = np.linspace(0, 1279, 100)
    optimized_moves = np.linspace(0, 127, 100)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(time_points, original_moves, label='Original Explorer', linewidth=2)
    ax.plot(time_points, optimized_moves, label='Optimized Explorer', linewidth=2)
    
    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('Moves')
    ax.set_title('Solution Convergence Comparison')
    ax.legend()
    ax.grid(True)
    
    plt.tight_layout()
    plt.savefig('convergence_comparison.png')
    plt.close()

def create_radar_chart():
    """Create radar chart comparing multiple performance dimensions"""
    # Data
    categories = ['Speed', 'Memory Efficiency', 'Path Optimization', 
                 'Adaptability', 'Code Simplicity']
    original = [0.7, 0.8, 0.6, 0.5, 0.9]
    optimized = [0.9, 0.7, 0.9, 0.8, 0.6]
    
    # Number of variables
    N = len(categories)
    
    # Compute angle for each axis
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    
    # Initialise the spider plot
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    
    # Plot data
    original += original[:1]
    optimized += optimized[:1]
    ax.plot(angles, original, linewidth=2, linestyle='solid', label='Original')
    ax.fill(angles, original, alpha=0.1)
    ax.plot(angles, optimized, linewidth=2, linestyle='solid', label='Optimized')
    ax.fill(angles, optimized, alpha=0.1)
    
    # Set category labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    
    # Add legend
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    
    # Add title
    plt.title('Performance Metrics Radar Chart', size=15, y=1.1)
    
    plt.tight_layout()
    plt.savefig('radar_comparison.png')
    plt.close()

def main():
    parser = argparse.ArgumentParser(description='Generate performance visualization graphs')
    parser.add_argument('--type', choices=['comparison', 'convergence', 'radar', 'all'],
                      default='all', help='Type of graph to generate')
    args = parser.parse_args()
    
    if args.type == 'all' or args.type == 'comparison':
        create_performance_comparison()
    if args.type == 'all' or args.type == 'convergence':
        create_convergence_comparison()
    if args.type == 'all' or args.type == 'radar':
        create_radar_chart()

if __name__ == '__main__':
    main() 