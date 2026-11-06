"""Union-find with path compression and union by size."""
class DisjointSet:
    def __init__(self, items=()):
        self.parent = {}
        self.size = {}
        for item in items:
            self.add(item)

    def add(self, item):
        if item not in self.parent:
            self.parent[item] = item
            self.size[item] = 1
            return True
        return False

    def find(self, item):
        if item not in self.parent:
            raise KeyError(item)
        root = item
        while self.parent[root] != root:
            root = self.parent[root]
        while item != root:
            nxt = self.parent[item]
            self.parent[item] = root
            item = nxt
        return root

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        del self.size[rb]
        return True

    def connected(self, a, b):
        return self.find(a) == self.find(b)

    def components(self):
        groups = {}
        for item in self.parent:
            groups.setdefault(self.find(item), set()).add(item)
        return list(groups.values())

def redundant_edges(vertices, edges):
    """Return edges that would form a cycle in an undirected graph."""
    ds = DisjointSet(vertices)
    redundant = []
    for a, b in edges:
        if not ds.union(a, b):
            redundant.append((a, b))
    return redundant

if __name__ == "__main__":
    print(redundant_edges(range(4), [(0,1),(1,2),(0,2),(2,3)]))
