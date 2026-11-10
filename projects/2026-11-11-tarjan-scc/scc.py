"""Strongly connected components and condensation graph, O(V+E)."""
def analyze(graph):
    nodes=set(graph)
    for neighbors in graph.values(): nodes.update(neighbors)
    adj={n:tuple(sorted(set(graph.get(n,())))) for n in nodes}
    index=0; indices={}; low={}; stack=[]; active=set(); components=[]
    def visit(v):
        nonlocal index
        indices[v]=low[v]=index; index+=1
        stack.append(v); active.add(v)
        for w in adj[v]:
            if w not in indices:
                visit(w); low[v]=min(low[v],low[w])
            elif w in active:
                low[v]=min(low[v],indices[w])
        if low[v]==indices[v]:
            group=[]
            while True:
                w=stack.pop(); active.remove(w); group.append(w)
                if w==v: break
            components.append(tuple(sorted(group)))
    for node in sorted(nodes):
        if node not in indices: visit(node)
    components.sort()
    owner={v:i for i,group in enumerate(components) for v in group}
    edges=sorted({(owner[u],owner[v]) for u in nodes for v in adj[u] if owner[u]!=owner[v]})
    cyclic=[group for group in components if len(group)>1 or group[0] in adj[group[0]]]
    return {"components":components,"edges":edges,"cyclic":cyclic}
if __name__=="__main__":
    print(analyze({"a":["b"],"b":["a","c"],"c":["d"],"d":["c"]}))
