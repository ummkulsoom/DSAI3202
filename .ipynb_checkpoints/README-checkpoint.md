Observations:

The sequential for-loop was quite fast due to its simplicity and lack of process management overhead.

The manual multiprocessing for-loop was skipped because it tries to spawn 10 million processes (one per number), which overwhelms the system and leads to extremely poor performance.

Pool.map() was slower than expected due to the cost of spinning up multiple worker processes and managing inter-process communication.

Surprisingly, Pool.apply_async() outperformed everything, including the sequential version. This is likely because it efficiently distributes the workload in parallel without blocking, especially when used in smaller batches.

ProcessPoolExecutor was the slowest. While it’s good for readability and abstraction, it adds extra overhead that’s not worth it for small, fast computations.

Conclusion: Multiprocessing is only useful when the task is heavy enough to offset the overhead of process management. For lightweight operations, sequential code can outperform or match parallel solutions.



In this simulation, we tested a connection pool with a maximum of 3 connections shared across 6 processes.


Behavior Observed:
Only 3 processes (Task-0, Task-1, Task-2) could acquire a connection immediately.

The rest (Task-3, Task-4, Task-5) had to wait until a connection was released.

Once a task finished and released its connection, a waiting task was able to acquire it and proceed.

How Semaphores Prevent Race Conditions?
The semaphore acts like a traffic controller:It limits how many processes can access the critical section (in this case, the connection pool) at once.When a process acquires a connection, it decreases the semaphore counter.If the limit is reached, additional processes are blocked until a resource is released.Once a connection is released, the counter is increased, and a waiting process is allowed through.

This ensures safe access to shared resources and prevents multiple processes from using the same connection at the same time.