# Project Critical Path Analyzer

DAG-based project scheduling with earliest/latest starts, slack, critical tasks, cycle detection, and a worked project plan.

## Run

Requires Python 3.10+ and only the standard library. From this project directory:

```bash
python cpm.py
python -m unittest -v test_cpm.py
```

## Design and limitations

All durations are nonnegative integer time units; resource limits, calendars, holidays, and uncertainty are intentionally out of scope. Slack is computed from earliest and latest feasible starts. Runtime is O((V+E) log V) due to the deterministic priority queue.

## Learning objectives

Read the implementation and tests together to understand invariants, input validation, boundary cases, and failure behavior. Extend the tests before modifying core logic.
