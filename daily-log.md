# Daily Contributions

A small daily learning log covering software engineering, programming, algorithms, cloud computing, networking, databases, testing, and related topics.

## 2026-10-25

**Topic: Defensive input validation**

Validate important input on both the client and the server. Browser validation improves user experience, but server-side validation is the real security boundary because client-side checks can be bypassed.

## 2026-10-26

**Topic: Database indexes**

A database index is an auxiliary data structure that helps the database locate rows without scanning an entire table. Indexes can make frequently filtered or joined queries much faster, but they also use storage and add work to inserts, updates, and deletes, so they should be chosen for actual query patterns rather than added to every column.

## 2026-10-27

**Topic: Hash tables and collision handling**

A hash table uses a hash function to map keys to array positions, giving average-case O(1) lookup, insertion, and deletion when keys are distributed well. Because different keys can map to the same position, implementations need a collision strategy such as separate chaining or open addressing. Performance can degrade as the table becomes crowded, which is why implementations typically resize when the load factor grows too high.

## 2026-10-28

**Major contribution: LRU Cache in Java**

Built a complete generic Least Recently Used cache using a `HashMap` plus a doubly linked list, demonstrating how two data structures combine to provide average O(1) lookup, update, recency promotion, and eviction. Added a runnable demonstration, six dependency-free tests, complexity/invariant documentation, and compile/run instructions.

Files:
- [`projects/2026-10-28-lru-cache/LruCache.java`](projects/2026-10-28-lru-cache/LruCache.java)
- [`projects/2026-10-28-lru-cache/LruCacheDemo.java`](projects/2026-10-28-lru-cache/LruCacheDemo.java)
- [`projects/2026-10-28-lru-cache/LruCacheTest.java`](projects/2026-10-28-lru-cache/LruCacheTest.java)
- [`projects/2026-10-28-lru-cache/README.md`](projects/2026-10-28-lru-cache/README.md)
