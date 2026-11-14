"""Binary indexed tree with O(log n) updates and queries."""
class Fenwick:
    def __init__(self, values):
        self.values = list(values)
        if any(type(x) not in (int, float) for x in self.values):
            raise TypeError("numeric values required")
        self.tree = [0] * (len(self.values) + 1)
        for i, value in enumerate(self.values):
            self.add(i, value, initial=True)

    def add(self, index, delta, initial=False):
        if not 0 <= index < len(self.values):
            raise IndexError(index)
        if type(delta) not in (int, float):
            raise TypeError("numeric delta required")
        if not initial:
            self.values[index] += delta
        i = index + 1
        while i < len(self.tree):
            self.tree[i] += delta
            i += i & -i

    def prefix(self, end):
        """Sum of elements in [0, end), including empty prefix."""
        if not 0 <= end <= len(self.values):
            raise IndexError(end)
        total = 0
        while end:
            total += self.tree[end]
            end -= end & -end
        return total

    def range_sum(self, start, end):
        """Half-open range [start, end)."""
        if not 0 <= start <= end <= len(self.values):
            raise IndexError((start, end))
        return self.prefix(end) - self.prefix(start)

    def set(self, index, value):
        self.add(index, value - self.values[index])

if __name__ == "__main__":
    tree = Fenwick([2, 4, 6, 8])
    tree.set(1, 10)
    print(tree.range_sum(1, 3))
