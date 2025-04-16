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
        explorer = Explorer(maze, visualize=False)
        start_time = time.perf_counter()
        _, moves = explorer.solve()
        time_taken = time.perf_counter() - start_time
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
        print("\n=== Distributed Exploration Results ===")
        best_time = float('inf')
        best_moves = float('inf')
        best_explorer = None
        total_moves = 0
        total_time = 0
        successful_explorers = 0

        for time_taken, moves_count, backtrack_count, explorer_id in results:
            if moves_count != float('inf'):
                print(f"\nExplorer {explorer_id + 1} (Process {explorer_id}):")
                print(f"Time taken: {time_taken:.2f} seconds")
                print(f"Number of moves: {moves_count}")
                print(f"Backtrack operations: {backtrack_count}")

                total_moves += moves_count
                total_time += time_taken
                successful_explorers += 1

                # Track best performer
                if moves_count < best_moves:
                    best_moves = moves_count
                    best_time = time_taken
                    best_explorer = explorer_id + 1

        if successful_explorers > 0:
            total_time = time.perf_counter() - start_time
            print("\n=== Summary Statistics ===")
            print(f"Total execution time: {total_time:.2f} seconds")
            print(f"Average moves per explorer: {total_moves/successful_explorers:.1f}")
            print(f"Average time per explorer: {total_time/successful_explorers:.2f} seconds")
            print(f"\n=== Best Performer ===")
            print(f"Explorer {best_explorer} (Process {best_explorer-1}) found the best solution:")
            print(f"Time: {best_time:.2f} seconds")
            print(f"Moves: {best_moves}")
        else:
            print("\nNo explorers completed successfully.")

if __name__ == "__main__":
    main() 