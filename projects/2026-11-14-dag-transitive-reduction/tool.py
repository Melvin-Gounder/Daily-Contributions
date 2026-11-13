from collections import deque

def transitive_reduction(graph):
    """Return a minimal reachability-equivalent adjacency map for a DAG."""
    nodes=set(graph)
    for children in graph.values(): nodes.update(children)
    adj={node:set(graph.get(node,())) for node in nodes}
    indegree={node:0 for node in nodes}
    for u in nodes:
        for v in adj[u]: indegree[v]+=1
    queue=deque(sorted((n for n in nodes if indegree[n]==0),key=str))
    visited=0
    while queue:
        u=queue.popleft(); visited+=1
        for v in adj[u]:
            indegree[v]-=1
            if indegree[v]==0: queue.append(v)
    if visited!=len(nodes): raise ValueError("graph contains a cycle")
    result={u:set(vs) for u,vs in adj.items()}
    def reachable(start,target):
        stack=list(result[start]); seen=set()
        while stack:
            u=stack.pop()
            if u==target: return True
            if u not in seen:
                seen.add(u); stack.extend(result[u])
        return False
    for u in sorted(nodes,key=str):
        for v in sorted(adj[u],key=str):
            result[u].remove(v)
            if not reachable(u,v): result[u].add(v)
    return {u:tuple(sorted(vs,key=str)) for u,vs in sorted(result.items(),key=lambda p:str(p[0]))}

if __name__=="__main__":
    print(transitive_reduction({"A":["B","C"],"B":["C"],"C":[]}))
