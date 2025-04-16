"""
Question 3: Compare performance of multiple explorers on the static maze.
"""

import time
from src.maze import create_maze
from src.explorer import Explorer

def run_explorer_comparison(num_explorers=4):
    """Run multiple explorers on the static maze and compare their performance."""
    print("\n=== Explorer Performance Comparison ===")
    print(f"Number of explorers: {num_explorers}")
    print("Maze type: Static")
    
    # Create the static maze
    maze = create_maze(width=30, height=30, maze_type="static")
    
    # Run multiple explorers
    results = []
    for i in range(num_explorers):
        print(f"\nRunning Explorer {i+1}...")
        explorer = Explorer(maze, visualize=False)
        
        # Time the exploration
        start_time = time.time()
        path, moves = explorer.solve()
        time_taken = time.time() - start_time
        
        # Store results
        results.append({
            'explorer_id': i + 1,
            'time_taken': time_taken,
            'moves': len(moves),
            'backtracks': explorer.backtrack_count
        })
        
        print(f"Explorer {i+1} finished with {len(moves)} moves")
    
    # Display results
    print("\n=== Results ===")
    for result in results:
        print(f"\nExplorer {result['explorer_id']}:")
        print(f"Time taken: {result['time_taken']:.3f} seconds")
        print(f"Total moves: {result['moves']}")
        print(f"Backtrack operations: {result['backtracks']}")
    
    # Find best performer
    best_time = min(results, key=lambda x: x['time_taken'])
    best_moves = min(results, key=lambda x: x['moves'])
    
    print("\n=== Best Performers ===")
    print(f"Fastest: Explorer {best_time['explorer_id']} ({best_time['time_taken']:.3f} seconds)")
    print(f"Most efficient: Explorer {best_moves['explorer_id']} ({best_moves['moves']} moves)")

if __name__ == "__main__":
    run_explorer_comparison() 