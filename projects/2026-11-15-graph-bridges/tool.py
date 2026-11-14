"""Critical edges and articulation vertices in undirected simple graphs."""
def analyze(vertices, edges):
    vertices = list(vertices)
    if len(set(vertices)) != len(vertices): raise ValueError("duplicate vertices")
    graph = {v:set() for v in vertices}
    for u,v in edges:
        if u not in graph or v not in graph or u == v:
            raise ValueError("invalid edge")
        graph[u].add(v); graph[v].add(u)
    order = {v:i for i,v in enumerate(vertices)}
    discovery, low, bridges, points = {}, {}, [], set()
    clock = 0

    def visit(u,parent=None):
        nonlocal clock
        discovery[u] = low[u] = clock
        clock += 1
        children = 0
        for v in sorted(graph[u],key=order.get):
            if v == parent: continue
            if v in discovery:
                low[u] = min(low[u],discovery[v])
            else:
                children += 1
                visit(v,u)
                low[u] = min(low[u],low[v])
                if low[v] > discovery[u]: bridges.append((u,v))
                if parent is not None and low[v] >= discovery[u]: points.add(u)
        if parent is None and children > 1: points.add(u)

    for vertex in vertices:
        if vertex not in discovery: visit(vertex)
    return {"bridges":bridges,"articulation_points":sorted(points,key=order.get)}

if __name__ == "__main__":
    print(analyze([0,1,2,3],[(0,1),(1,2),(2,0),(1,3)]))
