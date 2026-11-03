"""Nonnegative weighted shortest paths with deterministic tie-breaking."""
import heapq
import math

def shortest_paths(graph, start):
    nodes = set(graph)
    for src, edges in graph.items():
        for dst, weight in edges.items():
            nodes.add(dst)
            if not isinstance(weight, (int, float)) or isinstance(weight, bool) or not math.isfinite(weight) or weight < 0:
                raise ValueError("edge weights must be finite nonnegative numbers")
    if start not in nodes:
        raise ValueError("start node does not exist")
    dist = {node: math.inf for node in nodes}
    paths = {start: (start,)}
    dist[start] = 0
    heap = [(0, (start,), start)]
    while heap:
        cost, path, node = heapq.heappop(heap)
        if cost != dist[node] or path != paths.get(node):
            continue
        for neighbor, weight in graph.get(node, {}).items():
            candidate = cost + weight
            candidate_path = path + (neighbor,)
            if candidate < dist[neighbor] or (candidate == dist[neighbor] and candidate_path < paths.get(neighbor, (chr(0x10ffff),))):
                dist[neighbor] = candidate
                paths[neighbor] = candidate_path
                heapq.heappush(heap, (candidate, candidate_path, neighbor))
    return {node: {"distance": dist[node], "path": list(paths[node]) if node in paths else None} for node in sorted(nodes)}

if __name__ == "__main__":
    network = {"A":{"B":4,"C":1},"C":{"B":2,"D":5},"B":{"D":1},"D":{},"Z":{}}
    for destination, result in shortest_paths(network, "A").items():
        print(destination, result)
