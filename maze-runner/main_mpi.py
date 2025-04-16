"""
MPI implementation of the maze runner for distributed computing.
"""

from mpi4py import MPI
import argparse
import time
import sys
from typing import Tuple, List
from src.explorer import Explorer
from src.maze import create_maze

def run_explorer(maze, explorer_id: int) -> Tuple[float, int, int, int]:
    """
    Run a single explorer and return its statistics.
    Returns: (time_taken, moves_count, backtrack_count, explorer_id)
    """
    try:
        # Disable visualization and set a timeout
        explorer = Explorer(maze, visualize=False)
        start_time = time.perf_counter()
        _, moves = explorer.solve()
        time_taken = time.perf_counter() - start_time
        
        # Calculate moves per second safely
        moves_per_second = len(moves) / time_taken if time_taken > 0 else 0
        
        print(f"\n=== Maze Exploration Statistics ===")
        print(f"Total time taken: {time_taken:.2f} seconds")
        print(f"Total moves made: {len(moves)}")
        print(f"Number of backtrack operations: {explorer.backtrack_count}")
        print(f"Average moves per second: {moves_per_second:.2f}")
        print("==================================")
        
        return time_taken, len(moves), explorer.backtrack_count, explorer_id
    except Exception as e:
        print(f"\nExplorer {explorer_id + 1} encountered an error: {str(e)}", file=sys.stderr)
        return float('inf'), float('inf'), float('inf'), explorer_id

def main():
    # Initialize MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()  # Get the rank of this process
    size = comm.Get_size()  # Get the total number of processes

    if rank == 0:  # Master process
        parser = argparse.ArgumentParser(description="Distributed Maze Runner using MPI")
        parser.add_argument("--type", choices=["random", "static"], default="random",
                          help="Type of maze to generate (random or static)")
        parser.add_argument("--width", type=int, default=30,
                          help="Width of the maze (default: 30, ignored for static mazes)")
        parser.add_argument("--height", type=int, default=30,
                          help="Height of the maze (default: 30, ignored for static mazes)")
        args = parser.parse_args()

        print(f"Starting distributed maze solving with {size} processes...")
        start_time = time.perf_counter()

        # Create maze once and broadcast to all processes
        if args.type == "static":
            # For static maze, use default dimensions
            maze = create_maze(0, 0, "static")
        else:
            maze = create_maze(args.width, args.height, args.type)
    else:
        maze = None

    # Broadcast the maze to all processes
    maze = comm.bcast(maze, root=0)

    # Each process runs its explorer
    result = run_explorer(maze, rank)

    # Gather results from all processes
    results = comm.gather(result, root=0)

    if rank == 0:  # Master process processes results
        print("\n=== Detailed Exploration Results ===")
        
        # Initialize statistics
        best_time = float('inf')
        best_moves = float('inf')
        best_explorer = None
        total_moves = 0
        total_time = 0
        total_backtracks = 0
        successful_explorers = 0
        fastest_explorer = None
        fastest_time = float('inf')
        most_efficient_explorer = None
        best_moves_per_second = 0

        # Collect individual explorer statistics
        explorer_stats = []
        for time_taken, moves_count, backtrack_count, explorer_id in results:
            if moves_count != float('inf'):
                moves_per_second = moves_count / time_taken if time_taken > 0 else float('inf')
                explorer_stats.append({
                    'id': explorer_id + 1,
                    'time': time_taken,
                    'moves': moves_count,
                    'backtracks': backtrack_count,
                    'moves_per_second': moves_per_second
                })
                
                # Update totals
                total_moves += moves_count
                total_time += time_taken
                total_backtracks += backtrack_count
                successful_explorers += 1

                # Track best solution (fewest moves)
                if moves_count < best_moves:
                    best_moves = moves_count
                    best_time = time_taken
                    best_explorer = explorer_id + 1

                # Track fastest solution
                if time_taken < fastest_time:
                    fastest_time = time_taken
                    fastest_explorer = explorer_id + 1

                # Track most efficient solution (moves per second)
                if moves_per_second != float('inf') and moves_per_second > best_moves_per_second:
                    best_moves_per_second = moves_per_second
                    most_efficient_explorer = explorer_id + 1

        if successful_explorers > 0:
            total_execution_time = time.perf_counter() - start_time
            
            # Print individual explorer results
            print("\n=== Individual Explorer Performance ===")
            for stats in explorer_stats:
                print(f"\nExplorer {stats['id']} (Process {stats['id']-1}):")
                print(f"Time taken: {stats['time']:.3f} seconds")
                print(f"Number of moves: {stats['moves']}")
                print(f"Backtrack operations: {stats['backtracks']}")
                print(f"Moves per second: {stats['moves_per_second']:.2f}")

            # Print aggregate statistics
            print("\n=== Aggregate Statistics ===")
            print(f"Total execution time: {total_execution_time:.3f} seconds")
            print(f"Average moves per explorer: {total_moves/successful_explorers:.1f}")
            print(f"Average time per explorer: {total_time/successful_explorers:.3f} seconds")
            print(f"Average backtrack operations: {total_backtracks/successful_explorers:.1f}")
            print(f"Total successful explorers: {successful_explorers}/{size}")

            # Print performance rankings
            print("\n=== Performance Rankings ===")
            print(f"Best Solution (Fewest Moves):")
            print(f"  Explorer {best_explorer} with {best_moves} moves in {best_time:.3f} seconds")
            
            print(f"\nFastest Solution:")
            print(f"  Explorer {fastest_explorer} in {fastest_time:.3f} seconds")
            
            if most_efficient_explorer:
                print(f"\nMost Efficient Solution:")
                print(f"  Explorer {most_efficient_explorer} with {best_moves_per_second:.2f} moves/second")

            # Print efficiency comparison
            print("\n=== Efficiency Analysis ===")
            print(f"Solution consistency: {'All explorers found same solution' if len(set(s['moves'] for s in explorer_stats)) == 1 else 'Solutions varied'}")
            print(f"Time consistency: {'All times within 10% of mean' if max(s['time'] for s in explorer_stats) / min(s['time'] for s in explorer_stats) < 1.1 else 'Times varied significantly'}")
            
        else:
            print("\nNo explorers completed successfully.")

if __name__ == "__main__":
    main() 