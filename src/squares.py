import time
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor

def compute_square(x):
    """Calculate and return the square of a number"""
    return x * x

def time_sequential_execution(numbers):
    """Measure time for computing squares using a simple for-loop"""
    start = time.time()
    total = 0
    for value in numbers:
        total += compute_square(value)
    end = time.time()
    return end - start

def time_individual_processes(numbers):
    """Measure time taken when launching a process per number (limited by CPU count * 2)"""
    start = time.time()
    active_processes = []
    limit = mp.cpu_count() * 2

    for value in numbers:
        proc = mp.Process(target=compute_square, args=(value,))
        active_processes.append(proc)
        proc.start()

        if len(active_processes) >= limit:
            for proc in active_processes:
                proc.join()
            active_processes.clear()

    for proc in active_processes:
        proc.join()

    return time.time() - start

def time_with_pool_map(numbers):
    """Measure execution time using multiprocessing.Pool with map (blocking)"""
    start = time.time()
    with mp.Pool(processes=mp.cpu_count()) as pool:
        pool.map(compute_square, numbers)
    end = time.time()
    return end - start

def time_with_apply_async(numbers):
    """Measure time using Pool.apply_async on a limited number of tasks to avoid overhead"""
    start = time.time()
    with mp.Pool(processes=mp.cpu_count()) as pool:
        batch_size = 1000
        tasks = [pool.apply_async(compute_square, (n,)) for n in numbers[:batch_size]]
        results = [task.get() for task in tasks]
    end = time.time()
    return end - start

def time_with_process_pool_executor(numbers):
    """Measure time using concurrent.futures.ProcessPoolExecutor with chunked task assignment"""
    start = time.time()
    with ProcessPoolExecutor(max_workers=mp.cpu_count()) as executor:
        list(executor.map(compute_square, numbers, chunksize=1000))
    end = time.time()
    return end - start
