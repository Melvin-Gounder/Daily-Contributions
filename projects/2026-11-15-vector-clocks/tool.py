"""Vector clocks for distributed-system causality."""
class VectorClock:
    def __init__(self, nodes, values=None):
        self.nodes = tuple(nodes)
        if len(set(self.nodes)) != len(self.nodes) or not self.nodes:
            raise ValueError("nodes must be unique and nonempty")
        self.clock = dict.fromkeys(self.nodes, 0)
        if values is not None:
            if set(values) != set(self.nodes) or any(type(v) is not int or v < 0 for v in values.values()):
                raise ValueError("invalid clock values")
            self.clock.update(values)

    def tick(self, node):
        self.clock[node] += 1
        return self.snapshot()

    def receive(self, node, message):
        if set(message) != set(self.nodes) or any(type(v) is not int or v < 0 for v in message.values()):
            raise ValueError("incompatible message")
        for key in self.nodes:
            self.clock[key] = max(self.clock[key], message[key])
        return self.tick(node)

    def snapshot(self):
        return dict(self.clock)

def relation(a, b):
    if set(a) != set(b):
        raise ValueError("incompatible participants")
    if any(type(x) is not int or x < 0 for x in (*a.values(), *b.values())):
        raise ValueError("invalid counter")
    le = all(a[k] <= b[k] for k in a)
    ge = all(a[k] >= b[k] for k in a)
    return "equal" if le and ge else "before" if le else "after" if ge else "concurrent"

if __name__ == "__main__":
    a = VectorClock(["a", "b"])
    b = VectorClock(["a", "b"])
    a.tick("a")
    b.receive("b", a.snapshot())
    print(relation(a.snapshot(), b.snapshot()))
