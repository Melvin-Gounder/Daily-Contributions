from task_scheduler import Task, TaskScheduler


def main() -> None:
    tasks = [
        Task("lint"),
        Task("unit-tests"),
        Task("build", ("lint", "unit-tests")),
        Task("integration-tests", ("build",)),
        Task("package", ("build",)),
        Task("deploy", ("integration-tests", "package")),
    ]

    scheduler = TaskScheduler(tasks)
    print("Execution order:")
    print(" -> ".join(scheduler.execution_order()))

    print("\nParallel-ready stages:")
    for number, stage in enumerate(scheduler.stages(), start=1):
        print(f"  Stage {number}: {', '.join(stage)}")

    print(f"\nCritical depth: {scheduler.critical_depth()} stages")


if __name__ == "__main__":
    main()
