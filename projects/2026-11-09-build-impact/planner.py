from collections import defaultdict
import heapq
class CycleError(ValueError): pass
def plan(graph,changed=None):
    """Topological build order, optionally restricted to changed targets and dependents."""
    deps={n:set(ds) for n,ds in graph.items()}
    if any(d not in deps for ds in deps.values() for d in ds): raise ValueError("unknown dependency")
    reverse=defaultdict(set)
    for n,ds in deps.items():
        for d in ds: reverse[d].add(n)
    affected=set(deps) if changed is None else set(changed)
    if affected-set(deps): raise ValueError("unknown target")
    queue=list(affected)
    while queue:
        for child in reverse[queue.pop()]:
            if child not in affected: affected.add(child); queue.append(child)
    degree={n:len(deps[n]&affected) for n in affected}
    ready=[n for n in affected if degree[n]==0]; heapq.heapify(ready)
    result=[]
    while ready:
        n=heapq.heappop(ready); result.append(n)
        for child in reverse[n]:
            if child in degree:
                degree[child]-=1
                if degree[child]==0: heapq.heappush(ready,child)
    if len(result)!=len(affected): raise CycleError("cycle among "+str(sorted(affected-set(result))))
    return result
if __name__=="__main__":
    g={"core":[],"api":["core"],"web":["api"],"docs":[]}
    print("full:",plan(g)); print("core changed:",plan(g,["core"]))
