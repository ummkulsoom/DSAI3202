"""
Main entry point for the maze runner game.
"""

import argparse
import multiprocessing
import time
import sys
from typing import Tuple, List
from src.game import run_game
from src.explorer import Explorer
from src.enhanced_explorer import EnhancedExplorer
from src.maze import create_maze


def run_explorer(maze, explorer_id: int) -> Tuple[float, int, int, int]:
    """
    Run a single explorer and return its statistics.
    Returns: (time_taken, moves_count, backtrack_count, explorer_id)
    """
    try:
        explorer = EnhancedExplorer(maze, visualize=False)  # Use EnhancedExplorer for parallel runs
        start_time = time.perf_counter()  # Use high-precision timer
        _, moves = explorer.solve()
        time_taken = time.perf_counter() - start_time
        return time_taken, len(moves), explorer.backtrack_count, explorer_id
    except Exception as e:
        print(f"\nExplorer {explorer_id + 1} encountered an error: {str(e)}", file=sys.stderr)
        return float('inf'), float('inf'), float('inf'), explorer_id


def main():
    parser = argparse.ArgumentParser(description="Maze Runner Game")
    parser.add_argument("--type", choices=["random", "static"], default="random",
                        help="Type of maze to generate (random or static)")
    parser.add_argument("--width", type=int, default=30,
                        help="Width of the maze (default: 30, ignored for static mazes)")
    parser.add_argument("--height", type=int, default=30,
                        help="Height of the maze (default: 30, ignored for static mazes)")
    parser.add_argument("--auto", action="store_true",
                        help="Run automated maze exploration")
    parser.add_argument("--visualize", action="store_true",
                        help="Visualize the automated exploration in real-time")
    parser.add_argument("--parallel", type=int, default=1,
                        help="Number of explorers to run in parallel (default: 1)")
    parser.add_argument("--timeout", type=int, default=60,
                        help="Timeout in seconds for each explorer (default: 60)")
    
    args = parser.parse_args()
    
    if args.auto:
        if args.parallel > 1:
            # Run multiple explorers in parallel
            print(f"Running {args.parallel} explorers in parallel...")
            print("Press Ctrl+C to stop the exploration at any time.")
            
            # Create maze once to save time
            maze = create_maze(args.width, args.height, args.type)
            
            # Create a pool of workers
            with multiprocessing.Pool(processes=args.parallel) as pool:
                # Prepare arguments for each explorer
                explorer_args = [(maze, i) for i in range(args.parallel)]
                
                # Run explorers in parallel with timeout
                start_time = time.perf_counter()
                results = []
                try:
                    async_result = pool.starmap_async(run_explorer, explorer_args)
                    while not async_result.ready():
                        elapsed = time.perf_counter() - start_time
                        completed = len(results)
                        print(f"\rProgress: {completed}/{args.parallel} explorers completed. Time elapsed: {elapsed:.1f}s", end="")
                        time.sleep(0.1)
                        if elapsed > args.timeout:
                            raise multiprocessing.TimeoutError
                    
                    results = async_result.get(timeout=1)  # Short timeout for final collection
                    
                except multiprocessing.TimeoutError:
                    print("\nTimeout reached! Stopping exploration...")
                    pool.terminate()
                    pool.join()
                except KeyboardInterrupt:
                    print("\nExploration stopped by user!")
                    pool.terminate()
                    pool.join()
                except Exception as e:
                    print(f"\nAn error occurred: {str(e)}", file=sys.stderr)
                    pool.terminate()
                    pool.join()
            
            # Process and display results
            if results:
                print("\n\n=== Parallel Exploration Results ===")
                best_time = float('inf')
                best_moves = float('inf')
                best_explorer = None
                total_moves = 0
                total_time = 0
                successful_explorers = 0
                
                for time_taken, moves_count, backtrack_count, explorer_id in results:
                    if moves_count != float('inf'):
                        print(f"\nExplorer {explorer_id + 1}:")
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
                    print("\n=== Summary Statistics ===")
                    print(f"Average moves per explorer: {total_moves/successful_explorers:.1f}")
                    print(f"Average time per explorer: {total_time/successful_explorers:.2f} seconds")
                    print(f"\n=== Best Performer ===")
                    print(f"Explorer {best_explorer} found the best solution:")
                    print(f"Time: {best_time:.2f} seconds")
                    print(f"Moves: {best_moves}")
                else:
                    print("\nNo explorers completed successfully.")
            else:
                print("\nNo results were collected. Exploration was interrupted or timed out.")
            
        else:
            # Run single explorer (original behavior)
            maze = create_maze(args.width, args.height, args.type)
            explorer = EnhancedExplorer(maze, visualize=args.visualize)  # Use EnhancedExplorer here too
            path, moves = explorer.solve()
            time_taken = explorer.end_time - explorer.start_time
            print(f"Maze solved in {time_taken:.2f} seconds")
            print(f"Number of moves: {len(moves)}")
            if args.type == "static":
                print("Note: Width and height arguments were ignored for the static maze")
    else:
        # Run the interactive game
        run_game(maze_type=args.type, width=args.width, height=args.height)


if __name__ == "__main__":
    main()
