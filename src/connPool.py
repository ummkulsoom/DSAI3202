import time
import random
import multiprocessing

class DBConnectionPool:
    """Manages a limited set of database connections using semaphore control and shared list"""

    def __init__(self, max_conn, shared_manager):
        """
        Initialize the pool with a set number of connections
        
        :param max_conn: Maximum concurrent connections
        :param shared_manager: A multiprocessing.Manager() to manage shared state
        """
        self.semaphore = multiprocessing.Semaphore(max_conn)
        self.lock = multiprocessing.Lock()
        self.available_connections = shared_manager.list([f"DBConn-{i}" for i in range(max_conn)])

    def acquire_connection(self):
        """Get a connection from the pool"""
        self.semaphore.acquire()
        with self.lock:
            return self.available_connections.pop(0)

    def return_connection(self, conn):
        """Put a connection back into the pool"""
        with self.lock:
            self.available_connections.append(conn)
        self.semaphore.release()

def simulate_db_task(pool, pid):
    """
    Simulate a task that requires a DB connection
    
    :param pool: DBConnectionPool instance
    :param pid: Identifier for the current process
    """
    print(f"Task-{pid} is waiting for a DB connection...")

    conn = pool.acquire_connection()
    print(f"Task-{pid} got {conn}")

    time.sleep(random.uniform(1, 5))  # Simulate some operation

    pool.return_connection(conn)
    print(f"Task-{pid} released {conn}")
