import unittest

from task_scheduler import (
    CycleError,
    SchedulerError,
    Task,
    TaskScheduler,
    UnknownDependencyError,
)


class TaskSchedulerTests(unittest.TestCase):
    def test_linear_dependencies_are_ordered(self):
        scheduler = TaskScheduler([
            Task("compile"),
            Task("test", ("compile",)),
            Task("deploy", ("test",)),
        ])
        self.assertEqual(["compile", "test", "deploy"], scheduler.execution_order())

    def test_independent_tasks_share_stage(self):
        scheduler = TaskScheduler([
            Task("lint"),
            Task("test"),
            Task("build", ("lint", "test")),
        ])
        self.assertEqual([["lint", "test"], ["build"]], scheduler.stages())

    def test_deterministic_order_uses_names_for_ties(self):
        scheduler = TaskScheduler([Task("zeta"), Task("alpha"), Task("middle")])
        self.assertEqual(["alpha", "middle", "zeta"], scheduler.execution_order())

    def test_unknown_dependency_is_rejected(self):
        with self.assertRaises(UnknownDependencyError):
            TaskScheduler([Task("deploy", ("build",))])

    def test_self_dependency_is_rejected(self):
        with self.assertRaises(CycleError):
            Task("loop", ("loop",))

    def test_multi_task_cycle_is_detected(self):
        scheduler = TaskScheduler([
            Task("a", ("c",)),
            Task("b", ("a",)),
            Task("c", ("b",)),
        ])
        with self.assertRaises(CycleError):
            scheduler.execution_order()
        with self.assertRaises(CycleError):
            scheduler.stages()

    def test_duplicate_names_are_rejected(self):
        with self.assertRaises(SchedulerError):
            TaskScheduler([Task("test"), Task("test")])

    def test_critical_depth(self):
        scheduler = TaskScheduler([
            Task("a"), Task("b"),
            Task("c", ("a",)),
            Task("d", ("b", "c")),
        ])
        self.assertEqual(3, scheduler.critical_depth())


if __name__ == "__main__":
    unittest.main()
