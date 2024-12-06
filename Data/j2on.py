from multiprocessing import Process
import time

# Worker function
def worker(task_id):
    print(f"Task {task_id} is running")
    time.sleep(1)  # Simulate some work

# Synchronous implementation
def run_tasks_synchronously():
    start_time = time.time()
    for i in range(5):
        worker(i)
    end_time = time.time()
    print(f"Synchronous tasks are done! Time taken: {end_time - start_time:.2f} seconds")

# Multiprocessing implementation
def run_tasks_with_multiprocessing():
    start_time = time.time()
    processes = [Process(target=worker, args=(i,)) for i in range(5)]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    end_time = time.time()
    print(f"Multiprocessing tasks are done! Time taken: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    print("Running tasks synchronously:")
    run_tasks_synchronously()

    print("\nRunning tasks with multiprocessing:")
    run_tasks_with_multiprocessing()
