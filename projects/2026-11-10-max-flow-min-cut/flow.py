"""Directed integer-capacity max flow via Edmonds-Karp."""
from collections import defaultdict, deque

def solve(edges, source, sink):
    if source == sink:
        raise ValueError("source and sink must differ")
    capacity = defaultdict(lambda: defaultdict(int))
    nodes = {source, sink}
    for u, v, amount in edges:
        if not isinstance(amount, int) or isinstance(amount, bool) or amount < 0:
            raise ValueError("capacities must be nonnegative integers")
        nodes.update((u, v))
        capacity[u][v] += amount
        capacity[v][u] += 0
    residual = {u: dict(capacity[u]) for u in nodes}
    for u in nodes:
        residual.setdefault(u, {})
    traces = []
    total = 0
    while True:
        parent = {source: None}
        queue = deque([source])
        while queue and sink not in parent:
            u = queue.popleft()
            for v in sorted(residual[u], key=str):
                if v not in parent and residual[u][v] > 0:
                    parent[v] = u
                    queue.append(v)
        if sink not in parent:
            break
        path = [sink]
        while path[-1] != source:
            path.append(parent[path[-1]])
        path.reverse()
        delta = min(residual[u][v] for u, v in zip(path, path[1:]))
        for u, v in zip(path, path[1:]):
            residual[u][v] -= delta
            residual[v][u] = residual[v].get(u, 0) + delta
        total += delta
        traces.append({"path": path, "augmentation": delta})
    reachable = {source}
    queue = deque([source])
    while queue:
        for v, available in residual[queue[0]].items():
            if available > 0 and v not in reachable:
                reachable.add(v)
                queue.append(v)
        queue.popleft()
    cut = sorted(
        [(u, v, c) for u in capacity for v, c in capacity[u].items()
         if c > 0 and u in reachable and v not in reachable],
        key=lambda edge: (str(edge[0]), str(edge[1])),
    )
    assert sum(c for _, _, c in cut) == total
    return {"max_flow": total, "min_cut": cut, "source_side": sorted(reachable, key=str), "augmentations": traces}

if __name__ == "__main__":
    graph = [("s","a",3),("s","b",2),("a","b",1),("a","t",2),("b","t",3)]
    print(solve(graph, "s", "t"))
