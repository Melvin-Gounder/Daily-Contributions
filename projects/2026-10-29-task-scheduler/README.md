# Dependency-Aware Task Scheduler

A dependency-free Python project that models build/deployment jobs as a **directed acyclic graph (DAG)** and schedules them safely.

## What it demonstrates

- Graph modelling with adjacency lists and in-degree counts.
- **Kahn's topological-sort algorithm** for dependency ordering.
- A min-heap to make valid ordering deterministic when several tasks are ready.
- Cycle detection and validation of missing/self dependencies.
- Level-by-level scheduling to identify tasks that can run in parallel.
- A small, testable API with custom exceptions.

## Example

The demo models this pipeline:

```text
lint --------\
              -> build -> integration-tests --\
unit-tests --/          \-> package -----------> deploy
```

`lint` and `unit-tests` can run together. `integration-tests` and `package` can also run together after `build` completes.

Run it with:

```bash
cd projects/2026-10-29-task-scheduler
python demo.py
```

Run the tests with:

```bash
python -m unittest -v
```

No third-party packages are required.

## API

```python
from task_scheduler import Task, TaskScheduler

scheduler = TaskScheduler([
    Task("compile"),
    Task("test", ("compile",)),
    Task("deploy", ("test",)),
])

print(scheduler.execution_order())
print(scheduler.stages())
```

`execution_order()` returns one valid deterministic topological ordering. `stages()` returns groups whose members have no unresolved dependency on another member of the same or later stage.

## Complexity

For **V** tasks and **E** dependency edges, graph construction and topological processing take **O(V + E)** work, apart from deterministic ready-task ordering. `execution_order()` uses a heap, adding an **O(log V)** factor to ready-queue operations. `stages()` sorts each newly-ready group for stable output.

Memory usage is **O(V + E)** for the graph, in-degree table, and scheduling state.

## Why this matters

The same dependency model appears in build systems, CI/CD pipelines, package managers, course prerequisite planners, workflow engines, and job orchestration. A topological sort answers the core question: *what can run now without violating prerequisites?*
