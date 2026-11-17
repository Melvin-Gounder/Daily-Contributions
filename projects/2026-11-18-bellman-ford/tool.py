"""Bellman–Ford shortest paths with reachable negative-cycle detection."""
from math import inf

def shortest_paths(vertices, edges, source):
    nodes = set(vertices)
    if source not in nodes:
        raise ValueError("unknown source")
    edges = list(edges)
    for u, v, w in edges:
        if u not in nodes or v not in nodes or not isinstance(w, (int, float)) or not -inf < w < inf:
            raise ValueError("invalid edge")
    distance = {v: inf for v in nodes}
    parent = {v: None for v in nodes}
    distance[source] = 0
    for _ in range(len(nodes) - 1):
        changed = False
        for u, v, weight in edges:
            if distance[u] != inf and distance[u] + weight < distance[v]:
                distance[v] = distance[u] + weight
                parent[v] = u
                changed = True
        if not changed:
            break
    for u, v, weight in edges:
        if distance[u] != inf and distance[u] + weight < distance[v]:
            raise ValueError("reachable negative-weight cycle")
    return distance, parent

def path_to(parent, source, destination):
    if source not in parent or destination not in parent:
        raise ValueError("unknown vertex")
    route, seen = [], set()
    node = destination
    while node is not None:
        if node in seen:
            raise ValueError("cyclic predecessor chain")
        seen.add(node)
        route.append(node)
        if node == source:
            return list(reversed(route))
        node = parent[node]
    return None

if __name__ == "__main__":
    graph = [("A", "B", 4), ("A", "C", 5), ("B", "C", -2), ("C", "D", 3)]
    d, p = shortest_paths(["A", "B", "C", "D"], graph, "A")
    print(d, path_to(p, "A", "D"))
