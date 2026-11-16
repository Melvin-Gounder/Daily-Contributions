"""Small bounded concurrent map with stable output ordering."""
import queue
import threading
from dataclasses import dataclass

@dataclass
class Outcome:
    value: object = None
    error: Exception = None

def parallel_map(fn, items, workers=4, capacity=16):
    if workers < 1 or capacity < 1:
        raise ValueError("workers and capacity must be positive")
    jobs = queue.Queue(maxsize=capacity)
    results = []
    threads = []
    def worker():
        while True:
            item = jobs.get()
            try:
                if item is None:
                    return
                index, value = item
                try:
                    results[index] = Outcome(value=fn(value))
                except Exception as exc:
                    results[index] = Outcome(error=exc)
            finally:
                jobs.task_done()
    for _ in range(workers):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)
    try:
        for item in items:
            index = len(results)
            results.append(None)
            jobs.put((index, item))
    finally:
        for _ in threads:
            jobs.put(None)
        jobs.join()
        for t in threads:
            t.join()
    return results

if __name__ == "__main__":
    print(parallel_map(lambda x: x*x, range(5), workers=2))
