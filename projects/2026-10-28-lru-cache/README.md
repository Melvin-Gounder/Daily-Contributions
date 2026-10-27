# LRU Cache — Java Implementation

A small, runnable implementation of a **Least Recently Used (LRU) cache** using a hash map plus a doubly linked list.

## Why these two data structures?

An LRU cache needs two operations to stay fast:

- Find a cached value by key.
- Move the most recently accessed item to the front and evict the least recently used item from the back.

A `HashMap` provides average **O(1)** key lookup. A doubly linked list provides **O(1)** removal and insertion when a node is already known. Combining them gives average O(1) `get` and `put` operations.

## Invariants

- `head.next` is the most recently used entry.
- `tail.prev` is the least recently used entry.
- Every real list node is present in the map exactly once.
- The number of cached entries never exceeds `capacity`.

## Run

From this directory:

```bash
javac LruCache.java LruCacheDemo.java LruCacheTest.java
java LruCacheDemo
java LruCacheTest
```

No external libraries are required; Java 17 or later is sufficient.

## Example

With capacity 3, inserting A, B and C gives an order of `C -> B -> A`. Reading A makes it most recently used: `A -> C -> B`. Inserting D then evicts B, because B is now the least recently used entry.

## Complexity

| Operation | Average time | Extra space |
|---|---:|---:|
| `get(key)` | O(1) | O(1) |
| `put(key, value)` | O(1) | O(1) per entry |
| Cache overall | — | O(capacity) |

The O(1) claims assume normal `HashMap` behavior. The implementation is intentionally not thread-safe; concurrent use would require synchronization or a different design.
