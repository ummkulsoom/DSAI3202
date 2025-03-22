import time
import random
import multiprocessing
from src.squares import (
    time_sequential_execution,
    time_individual_processes,
    time_with_pool_map,
    time_with_apply_async,
    time_with_process_pool_executor
)

from src.connPool import DBConnectionPool, simulate_db_task


def run_square_comparisons():
    """Execute square computations using different parallel strategies and print results"""
    data = [random.randint(1, 1000) for _ in range(10**7)]  # 10 million values
    print(f"Benchmarking square computation for {len(data)} values...\n")

    # Sequential execution
    t_seq = time_sequential_execution(data)
    print(f"[Sequential Loop] Time: {t_seq:.2f} seconds")

    # Optional: Uncomment to test manual multiprocessing loop (less efficient)
    # t_mp_manual = time_individual_processes(data)
    # print(f"[Multiprocessing (individual processes)] Time: {t_mp_manual:.2f} seconds")

    # Pool.map (blocking)
    t_pool_map = time_with_pool_map(data)
    print(f"[Pool.map] Time: {t_pool_map:.2f} seconds")

    # Pool.apply_async (non-blocking)
    t_async = time_with_apply_async(data)
    print(f"[Pool.apply_async] Time: {t_async:.2f} seconds")

    # ProcessPoolExecutor
    t_executor = time_with_process_pool_executor(data)
    print(f"[ProcessPoolExecutor] Time: {t_executor:.2f} seconds")

def test_db_connection_pool():
    """Test the DBConnectionPool with simulated concurrent access"""
    max_conn = 3
    num_tasks = 6

    print("\nStarting DB connection pool simulation...")

    with multiprocessing.Manager() as manager:
        pool = DBConnectionPool(max_conn, manager)
        workers = [
            multiprocessing.Process(target=simulate_db_task, args=(pool, pid))
            for pid in range(num_tasks)
        ]

        for w in workers:
            w.start()
        for w in workers:
            w.join()

def main():
    """Main entry to run all benchmark and simulation tasks"""
    print("==== Execution Begins ====")
    run_square_comparisons()
    print("\n---------------------------")
    test_db_connection_pool()
    print("\n==== All operations completed ====")

if __name__ == "__main__":
    main()
