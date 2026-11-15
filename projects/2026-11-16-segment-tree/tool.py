"""Range-add/range-sum segment tree with lazy propagation."""
class SegmentTree:
    def __init__(self, values):
        self.n = len(values)
        self.tree = [0] * (4 * max(1, self.n))
        self.lazy = [0] * len(self.tree)
        if self.n:
            self._build(1, 0, self.n, values)

    def _build(self, node, lo, hi, values):
        if hi - lo == 1:
            self.tree[node] = values[lo]
            return
        mid = (lo + hi) // 2
        self._build(node * 2, lo, mid, values)
        self._build(node * 2 + 1, mid, hi, values)
        self.tree[node] = self.tree[node * 2] + self.tree[node * 2 + 1]

    def _apply(self, node, lo, hi, delta):
        self.tree[node] += delta * (hi - lo)
        self.lazy[node] += delta

    def _push(self, node, lo, hi):
        if self.lazy[node] and hi - lo > 1:
            mid = (lo + hi) // 2
            self._apply(node * 2, lo, mid, self.lazy[node])
            self._apply(node * 2 + 1, mid, hi, self.lazy[node])
            self.lazy[node] = 0

    def _check(self, left, right):
        if not (0 <= left <= right <= self.n):
            raise IndexError("expected 0 <= left <= right <= length")

    def add(self, left, right, delta):
        self._check(left, right)
        if left != right:
            self._add(1, 0, self.n, left, right, delta)

    def _add(self, node, lo, hi, left, right, delta):
        if right <= lo or hi <= left: return
        if left <= lo and hi <= right:
            self._apply(node, lo, hi, delta)
            return
        self._push(node, lo, hi)
        mid = (lo + hi) // 2
        self._add(node * 2, lo, mid, left, right, delta)
        self._add(node * 2 + 1, mid, hi, left, right, delta)
        self.tree[node] = self.tree[node * 2] + self.tree[node * 2 + 1]

    def sum(self, left, right):
        self._check(left, right)
        return self._sum(1, 0, self.n, left, right) if left != right else 0

    def _sum(self, node, lo, hi, left, right):
        if right <= lo or hi <= left: return 0
        if left <= lo and hi <= right: return self.tree[node]
        self._push(node, lo, hi)
        mid = (lo + hi) // 2
        return self._sum(node * 2, lo, mid, left, right) + self._sum(node * 2 + 1, mid, hi, left, right)

if __name__ == "__main__":
    s = SegmentTree([1, 2, 3, 4])
    s.add(1, 4, 5)
    print(s.sum(0, 4), s.sum(1, 3))
