"""Dependency-aware task scheduler using a directed acyclic graph (DAG).

The scheduler validates dependencies, detects cycles, computes a deterministic
execution order, and can group independent tasks into parallel-ready stages.
Only the Python standard library is required.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import heapq
from typing import Iterable


class SchedulerError(ValueError):
    """Base exception for invalid scheduler input."""


class UnknownDependencyError(SchedulerError):
    """Raised when a task depends on a task that has not been registered."""


class CycleError(SchedulerError):
    """Raised when dependencies contain a cycle."""


@dataclass(frozen=True)
class Task:
    name: str
    dependencies: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise SchedulerError("Task names cannot be blank")
        if self.name in self.dependencies:
            raise CycleError(f"Task '{self.name}' cannot depend on itself")


class TaskScheduler:
    def __init__(self, tasks: Iterable[Task]) -> None:
        task_list = list(tasks)
        self._tasks = {task.name: task for task in task_list}
        if len(self._tasks) != len(task_list):
            raise SchedulerError("Task names must be unique")
        self._validate_dependencies()

    def _validate_dependencies(self) -> None:
        known = set(self._tasks)
        for task in self._tasks.values():
            missing = set(task.dependencies) - known
            if missing:
                names = ", ".join(sorted(missing))
                raise UnknownDependencyError(
                    f"Task '{task.name}' has unknown dependencies: {names}"
                )

    def _graph(self) -> tuple[dict[str, int], dict[str, list[str]]]:
        indegree = {name: 0 for name in self._tasks}
        dependents: dict[str, list[str]] = defaultdict(list)
        for task in self._tasks.values():
            for dependency in task.dependencies:
                indegree[task.name] += 1
                dependents[dependency].append(task.name)
        for children in dependents.values():
            children.sort()
        return indegree, dependents

    def execution_order(self) -> list[str]:
        """Return a deterministic topological ordering of all tasks."""
        indegree, dependents = self._graph()
        ready = [name for name, degree in indegree.items() if degree == 0]
        heapq.heapify(ready)
        order: list[str] = []

        while ready:
            current = heapq.heappop(ready)
            order.append(current)
            for child in dependents[current]:
                indegree[child] -= 1
                if indegree[child] == 0:
                    heapq.heappush(ready, child)

        if len(order) != len(self._tasks):
            blocked = sorted(name for name, degree in indegree.items() if degree > 0)
            raise CycleError("Dependency cycle detected among: " + ", ".join(blocked))
        return order

    def stages(self) -> list[list[str]]:
        """Group tasks into stages where every task in a stage can run in parallel."""
        indegree, dependents = self._graph()
        ready = sorted(name for name, degree in indegree.items() if degree == 0)
        stages: list[list[str]] = []
        processed = 0

        while ready:
            stage = ready
            stages.append(stage)
            processed += len(stage)
            next_ready: list[str] = []
            for current in stage:
                for child in dependents[current]:
                    indegree[child] -= 1
                    if indegree[child] == 0:
                        next_ready.append(child)
            ready = sorted(next_ready)

        if processed != len(self._tasks):
            raise CycleError("Cannot build stages because the dependency graph has a cycle")
        return stages

    def critical_depth(self) -> int:
        """Return the minimum number of sequential stages required."""
        return len(self.stages())
