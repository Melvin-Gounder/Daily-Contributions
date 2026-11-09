"""Critical Path Method for activity-on-node project schedules."""
from collections import defaultdict
from dataclasses import dataclass
import heapq

@dataclass(frozen=True)
class Activity:
    duration: int
    dependencies: tuple = ()

def analyze(activities):
    tasks = {name: (value if isinstance(value, Activity) else Activity(*value))
             for name, value in activities.items()}
    if not tasks:
        return {"duration": 0, "order": [], "activities": {}, "critical": []}
    children=defaultdict(list)
    degree={}
    for name, task in tasks.items():
        if not isinstance(task.duration,int) or isinstance(task.duration,bool) or task.duration < 0:
            raise ValueError("duration must be a nonnegative integer")
        deps=set(task.dependencies)
        if len(deps)!=len(task.dependencies):
            raise ValueError("duplicate dependency")
        if name in deps or deps-set(tasks):
            raise ValueError("unknown or self dependency")
        degree[name]=len(deps)
        for dep in deps: children[dep].append(name)
    ready=[name for name in tasks if degree[name]==0]
    heapq.heapify(ready)
    order=[]
    while ready:
        name=heapq.heappop(ready)
        order.append(name)
        for child in children[name]:
            degree[child]-=1
            if degree[child]==0: heapq.heappush(ready,child)
    if len(order)!=len(tasks):
        raise ValueError("dependency cycle")
    earliest={}
    for name in order:
        start=max((earliest[dep][1] for dep in tasks[name].dependencies),default=0)
        earliest[name]=(start,start+tasks[name].duration)
    finish=max(end for _,end in earliest.values())
    latest={}
    for name in reversed(order):
        end=min((latest[child][0] for child in children[name]),default=finish)
        latest[name]=(end-tasks[name].duration,end)
    rows={}
    for name in order:
        es,ef=earliest[name]
        ls,lf=latest[name]
        rows[name]={"early_start":es,"early_finish":ef,"late_start":ls,"late_finish":lf,"slack":ls-es}
    return {"duration":finish,"order":order,"activities":rows,
            "critical":[name for name in order if rows[name]["slack"]==0]}

if __name__=="__main__":
    project={"design":Activity(3),"api":Activity(5,("design",)),
             "frontend":Activity(4,("design",)),"release":Activity(2,("api","frontend"))}
    from pprint import pprint
    pprint(analyze(project))
