# Deficit Round Robin Scheduler

A fair queue scheduler for variable-cost jobs such as network packets. Each queue receives a configurable quantum per round; unused credit carries over so large tasks eventually run, while FIFO order is preserved inside each queue.

Run `python scheduler.py` and `python -m unittest discover -v` (Python 3.9+, standard library). Tests cover fairness, eventual service, FIFO ordering, and validation.

The algorithm performs O(number of dispatched jobs + visited rounds) work. Tasks whose costs exceed a queue's quantum may wait several rounds. This is a batch demonstration, not a preemptive real-time scheduler; production systems also need backpressure and queue-size limits.
