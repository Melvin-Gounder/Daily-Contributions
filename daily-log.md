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

## 2026-10-29

**Major contribution: Dependency-Aware Task Scheduler in Python**

Built a dependency-free DAG task scheduler using Kahn's topological-sort algorithm. It validates dependencies, detects cycles, produces deterministic execution order, groups independent tasks into parallel-ready stages, and calculates critical depth. Added a runnable CI/CD-style demo, eight unit tests, API examples, complexity analysis, and documentation.

Files:
- [`projects/2026-10-29-task-scheduler/task_scheduler.py`](projects/2026-10-29-task-scheduler/task_scheduler.py)
- [`projects/2026-10-29-task-scheduler/demo.py`](projects/2026-10-29-task-scheduler/demo.py)
- [`projects/2026-10-29-task-scheduler/test_task_scheduler.py`](projects/2026-10-29-task-scheduler/test_task_scheduler.py)
- [`projects/2026-10-29-task-scheduler/README.md`](projects/2026-10-29-task-scheduler/README.md)

## 2026-10-30

**Major contribution: Authentication Security Log Analyzer in Python**

Built a defensive security CLI that parses authentication logs and detects bursts of failed logins per IP using a sliding time window. It validates IPv4/IPv6 addresses, tolerates or strictly rejects malformed input, resets failure state after successful authentication, produces deterministic reports, and uses only the Python standard library. Added a safe sample log, eight unit tests, algorithm/complexity documentation, and security notes.

Files:
- [`projects/2026-10-30-security-log-analyzer/security_log_analyzer.py`](projects/2026-10-30-security-log-analyzer/security_log_analyzer.py)
- [`projects/2026-10-30-security-log-analyzer/test_security_log_analyzer.py`](projects/2026-10-30-security-log-analyzer/test_security_log_analyzer.py)
- [`projects/2026-10-30-security-log-analyzer/sample.log`](projects/2026-10-30-security-log-analyzer/sample.log)
- [`projects/2026-10-30-security-log-analyzer/README.md`](projects/2026-10-30-security-log-analyzer/README.md)

## 2026-10-31

**Major contribution: SQLite Expense Tracker in Python**

Built a dependency-free expense-tracking CLI backed by a normalized SQLite database. It demonstrates foreign keys, constraints, purpose-built indexes, parameterized queries, atomic transactions, exact integer-cent money storage, `Decimal` input parsing, and grouped monthly reporting. Added eight in-memory integration tests, including month-boundary behavior and SQL-injection-shaped input, plus database-design and complexity documentation.

Files:
- [`projects/2026-10-31-sqlite-expense-tracker/expense_tracker.py`](projects/2026-10-31-sqlite-expense-tracker/expense_tracker.py)
- [`projects/2026-10-31-sqlite-expense-tracker/test_expense_tracker.py`](projects/2026-10-31-sqlite-expense-tracker/test_expense_tracker.py)
- [`projects/2026-10-31-sqlite-expense-tracker/README.md`](projects/2026-10-31-sqlite-expense-tracker/README.md)

## 2026-11-01

**Major contribution: Concurrent HTTP Health Checker in Python**

Built a dependency-free monitoring CLI that probes multiple HTTP endpoints concurrently with bounded worker threads, explicit timeouts, deterministic result ordering, useful exit codes, JSON output, and availability/median-latency summaries. Added seven network-isolated unit tests plus design, safety, and complexity documentation.

Files:
- [`projects/2026-11-01-http-health-checker/health_checker.py`](projects/2026-11-01-http-health-checker/health_checker.py)
- [`projects/2026-11-01-http-health-checker/test_health_checker.py`](projects/2026-11-01-http-health-checker/test_health_checker.py)
- [`projects/2026-11-01-http-health-checker/README.md`](projects/2026-11-01-http-health-checker/README.md)

## 2026-11-02

**Major contribution: Thread-Safe Token-Bucket Rate Limiter in Java**

Built a dependency-free token-bucket rate limiter that supports burst capacity, continuous fractional refill, weighted requests, estimated wait times, and synchronized atomic acquisition for concurrent callers. Added an injected deterministic clock so timing behavior can be tested without sleeping, a runnable demonstration, eight focused tests, complexity analysis, and notes on single-process versus distributed rate limiting.

Files:
- [`projects/2026-11-02-token-bucket-rate-limiter/TokenBucketRateLimiter.java`](projects/2026-11-02-token-bucket-rate-limiter/TokenBucketRateLimiter.java)
- [`projects/2026-11-02-token-bucket-rate-limiter/MutableClock.java`](projects/2026-11-02-token-bucket-rate-limiter/MutableClock.java)
- [`projects/2026-11-02-token-bucket-rate-limiter/RateLimiterDemo.java`](projects/2026-11-02-token-bucket-rate-limiter/RateLimiterDemo.java)
- [`projects/2026-11-02-token-bucket-rate-limiter/TokenBucketRateLimiterTest.java`](projects/2026-11-02-token-bucket-rate-limiter/TokenBucketRateLimiterTest.java)
- [`projects/2026-11-02-token-bucket-rate-limiter/README.md`](projects/2026-11-02-token-bucket-rate-limiter/README.md)

## 2026-11-04

### Contribution 1: IPv4 CIDR Subnet Planner

A strict IPv4 CIDR calculator with network, broadcast, usable host range, subnet splitting, and validation. Includes runnable examples, focused unit tests, and design documentation.

Files:
- [`projects/2026-11-04-cidr-subnet-planner/subnet.py`](projects/2026-11-04-cidr-subnet-planner/subnet.py)
- [`projects/2026-11-04-cidr-subnet-planner/test_subnet.py`](projects/2026-11-04-cidr-subnet-planner/test_subnet.py)
- [`projects/2026-11-04-cidr-subnet-planner/README.md`](projects/2026-11-04-cidr-subnet-planner/README.md)

### Contribution 2: Weighted Graph Route Planner

A deterministic Dijkstra shortest-path implementation with unreachable-node handling, path reconstruction, and negative-weight rejection. Includes runnable examples, focused unit tests, and design documentation.

Files:
- [`projects/2026-11-04-dijkstra-route-planner/routes.py`](projects/2026-11-04-dijkstra-route-planner/routes.py)
- [`projects/2026-11-04-dijkstra-route-planner/test_routes.py`](projects/2026-11-04-dijkstra-route-planner/test_routes.py)
- [`projects/2026-11-04-dijkstra-route-planner/README.md`](projects/2026-11-04-dijkstra-route-planner/README.md)

### Contribution 3: Typed Configuration Validator

A reusable environment-configuration parser with typed fields, defaults, required values, range constraints, and secret-safe errors. Includes runnable examples, focused unit tests, and design documentation.

Files:
- [`projects/2026-11-04-config-validator/config.py`](projects/2026-11-04-config-validator/config.py)
- [`projects/2026-11-04-config-validator/test_config.py`](projects/2026-11-04-config-validator/test_config.py)
- [`projects/2026-11-04-config-validator/README.md`](projects/2026-11-04-config-validator/README.md)

### Contribution 4: Streaming CSV Data Quality Profiler

A CLI that profiles CSV datasets with null counts, duplicate rows, numeric summaries, and malformed-row detection without loading the full dataset. Includes runnable examples, focused unit tests, and design documentation.

Files:
- [`projects/2026-11-04-csv-data-profiler/profile_csv.py`](projects/2026-11-04-csv-data-profiler/profile_csv.py)
- [`projects/2026-11-04-csv-data-profiler/test_profile_csv.py`](projects/2026-11-04-csv-data-profiler/test_profile_csv.py)
- [`projects/2026-11-04-csv-data-profiler/README.md`](projects/2026-11-04-csv-data-profiler/README.md)

### Contribution 5: Password Hashing and Verification Lab

A defensive PBKDF2-HMAC-SHA256 password-storage example with per-password random salts, constant-time verification, and upgrade detection. Includes runnable examples, focused unit tests, and design documentation.

Files:
- [`projects/2026-11-04-password-hash-lab/passwords.py`](projects/2026-11-04-password-hash-lab/passwords.py)
- [`projects/2026-11-04-password-hash-lab/test_passwords.py`](projects/2026-11-04-password-hash-lab/test_passwords.py)
- [`projects/2026-11-04-password-hash-lab/README.md`](projects/2026-11-04-password-hash-lab/README.md)

## 2026-11-05

### Contribution 1: Interval Booking Calendar

Conflict-safe half-open reservations, cancellation, available-slot search, and four self-contained unit tests.

Files:
- [`projects/2026-11-05-interval-calendar/calendar.py`](projects/2026-11-05-interval-calendar/calendar.py)

Run `python projects/2026-11-05-interval-calendar/calendar.py` for a demonstration, or `python projects/2026-11-05-interval-calendar/calendar.py test` for the built-in unit tests. Requires Python 3.9+; no external packages.

### Contribution 2: SHA-256 File Integrity Auditor

Streaming hashes, deterministic JSON manifests, added/removed/modified detection, CLI exit status, and isolated tests.

Files:
- [`projects/2026-11-05-file-integrity/integrity.py`](projects/2026-11-05-file-integrity/integrity.py)

Run `python projects/2026-11-05-file-integrity/integrity.py` for a demonstration, or `python projects/2026-11-05-file-integrity/integrity.py test` for the built-in unit tests. Requires Python 3.9+; no external packages.

### Contribution 3: Guarded State-Machine Workflow

Declarative approval transitions, guard conditions, rejection/rework, audit trail, and five focused tests.

Files:
- [`projects/2026-11-05-approval-workflow/workflow.py`](projects/2026-11-05-approval-workflow/workflow.py)

Run `python projects/2026-11-05-approval-workflow/workflow.py` for a demonstration, or `python projects/2026-11-05-approval-workflow/workflow.py test` for the built-in unit tests. Requires Python 3.9+; no external packages.

### Contribution 4: Inventory Replenishment Planner

Decimal demand forecasting, reserved inventory, lead-time and safety stock, pack-size rounding, ranked orders, and six tests.

Files:
- [`projects/2026-11-05-stock-replenishment/stock.py`](projects/2026-11-05-stock-replenishment/stock.py)

Run `python projects/2026-11-05-stock-replenishment/stock.py` for a demonstration, or `python projects/2026-11-05-stock-replenishment/stock.py test` for the built-in unit tests. Requires Python 3.9+; no external packages.

### Contribution 5: Event-Sourced Account Ledger

Append-only account events, integer-cent balances, replay, duplicate-ID protection, overdraft checks, JSONL import/export, and six tests.

Files:
- [`projects/2026-11-05-event-ledger/ledger.py`](projects/2026-11-05-event-ledger/ledger.py)

Run `python projects/2026-11-05-event-ledger/ledger.py` for a demonstration, or `python projects/2026-11-05-event-ledger/ledger.py test` for the built-in unit tests. Requires Python 3.9+; no external packages.

## 2026-11-06

**Daily target: 5 contributions (randomly selected from 5–10).**

### Contribution 1: Consistent Hash Ring

Deterministic virtual-node hashing with stable ownership and minimal remapping.

Files:
- [`projects/2026-11-06-consistent-hash/ring.py`](projects/2026-11-06-consistent-hash/ring.py)
- [`projects/2026-11-06-consistent-hash/test_ring.py`](projects/2026-11-06-consistent-hash/test_ring.py)
- [`projects/2026-11-06-consistent-hash/README.md`](projects/2026-11-06-consistent-hash/README.md)

### Contribution 2: Circuit Breaker

Failure-threshold protection with cooldown, half-open recovery, and deterministic clocks.

Files:
- [`projects/2026-11-06-circuit-breaker/breaker.py`](projects/2026-11-06-circuit-breaker/breaker.py)
- [`projects/2026-11-06-circuit-breaker/test_breaker.py`](projects/2026-11-06-circuit-breaker/test_breaker.py)
- [`projects/2026-11-06-circuit-breaker/README.md`](projects/2026-11-06-circuit-breaker/README.md)

### Contribution 3: Merkle Inclusion Proofs

SHA-256 integrity roots and compact inclusion proofs with tamper detection.

Files:
- [`projects/2026-11-06-merkle-audit/merkle.py`](projects/2026-11-06-merkle-audit/merkle.py)
- [`projects/2026-11-06-merkle-audit/test_merkle.py`](projects/2026-11-06-merkle-audit/test_merkle.py)
- [`projects/2026-11-06-merkle-audit/README.md`](projects/2026-11-06-merkle-audit/README.md)

### Contribution 4: Signed Keyset Pagination

Tamper-evident HMAC cursor tokens and stable ordered page traversal.

Files:
- [`projects/2026-11-06-cursor-pagination/cursor.py`](projects/2026-11-06-cursor-pagination/cursor.py)
- [`projects/2026-11-06-cursor-pagination/test_cursor.py`](projects/2026-11-06-cursor-pagination/test_cursor.py)
- [`projects/2026-11-06-cursor-pagination/README.md`](projects/2026-11-06-cursor-pagination/README.md)

### Contribution 5: Deficit Round Robin Scheduler

Cost-aware fair scheduling with per-queue credits and FIFO preservation.

Files:
- [`projects/2026-11-06-weighted-queue/scheduler.py`](projects/2026-11-06-weighted-queue/scheduler.py)
- [`projects/2026-11-06-weighted-queue/test_scheduler.py`](projects/2026-11-06-weighted-queue/test_scheduler.py)
- [`projects/2026-11-06-weighted-queue/README.md`](projects/2026-11-06-weighted-queue/README.md)

## 2026-11-07

**Daily target: 5 contributions (randomly selected from 5–10).**

### Contribution 1: Deterministic Retry Policy

Bounded exponential backoff with deterministic jitter, retryable-exception filtering, injectable sleep, and attempt history.

Files:
- [`projects/2026-11-07-retry-backoff/retry.py`](projects/2026-11-07-retry-backoff/retry.py)
- [`projects/2026-11-07-retry-backoff/test_retry.py`](projects/2026-11-07-retry-backoff/test_retry.py)
- [`projects/2026-11-07-retry-backoff/README.md`](projects/2026-11-07-retry-backoff/README.md)

### Contribution 2: Disjoint Set Connectivity Toolkit

Union-by-size and path compression for dynamic connectivity, component membership, and Kruskal-style cycle detection.

Files:
- [`projects/2026-11-07-union-find/connectivity.py`](projects/2026-11-07-union-find/connectivity.py)
- [`projects/2026-11-07-union-find/test_connectivity.py`](projects/2026-11-07-union-find/test_connectivity.py)
- [`projects/2026-11-07-union-find/README.md`](projects/2026-11-07-union-find/README.md)

### Contribution 3: Bloom Filter Membership Lab

Space-efficient probabilistic set membership using double hashing, sizing equations, serialization, and false-positive analysis.

Files:
- [`projects/2026-11-07-bloom-filter/bloom.py`](projects/2026-11-07-bloom-filter/bloom.py)
- [`projects/2026-11-07-bloom-filter/test_bloom.py`](projects/2026-11-07-bloom-filter/test_bloom.py)
- [`projects/2026-11-07-bloom-filter/README.md`](projects/2026-11-07-bloom-filter/README.md)

### Contribution 4: TTL Cache with Fake Clock

Expiring in-memory cache with monotonic deadlines, capacity-limited LRU eviction, injectable clock, and deterministic tests.

Files:
- [`projects/2026-11-07-ttl-cache/ttl_cache.py`](projects/2026-11-07-ttl-cache/ttl_cache.py)
- [`projects/2026-11-07-ttl-cache/test_ttl_cache.py`](projects/2026-11-07-ttl-cache/test_ttl_cache.py)
- [`projects/2026-11-07-ttl-cache/README.md`](projects/2026-11-07-ttl-cache/README.md)

### Contribution 5: Recursive JSON Contract Validator

Dependency-free recursive validation for JSON payloads with precise error paths, strict fields, arrays, and typed constraints.

Files:
- [`projects/2026-11-07-json-schema-lite/validator.py`](projects/2026-11-07-json-schema-lite/validator.py)
- [`projects/2026-11-07-json-schema-lite/test_validator.py`](projects/2026-11-07-json-schema-lite/test_validator.py)
- [`projects/2026-11-07-json-schema-lite/README.md`](projects/2026-11-07-json-schema-lite/README.md)

## 2026-11-08

**Daily target: 5 contributions (randomly selected from 5–10).**

### Contribution 1: A* Grid Pathfinding

Obstacle-aware shortest-path search using an admissible Manhattan heuristic. Includes runnable Python source, tests, and documentation.

Files:
- [`projects/2026-11-08-astar-grid/astar.py`](projects/2026-11-08-astar-grid/astar.py)
- [`projects/2026-11-08-astar-grid/test_astar.py`](projects/2026-11-08-astar-grid/test_astar.py)
- [`projects/2026-11-08-astar-grid/README.md`](projects/2026-11-08-astar-grid/README.md)

### Contribution 2: Transactional SQLite Migrations

Versioned transactional schema evolution with checksum-based drift detection. Includes runnable Python source, tests, and documentation.

Files:
- [`projects/2026-11-08-sqlite-migrations/migrations.py`](projects/2026-11-08-sqlite-migrations/migrations.py)
- [`projects/2026-11-08-sqlite-migrations/test_migrations.py`](projects/2026-11-08-sqlite-migrations/test_migrations.py)
- [`projects/2026-11-08-sqlite-migrations/README.md`](projects/2026-11-08-sqlite-migrations/README.md)

### Contribution 3: CSV Hash Join CLI

Relational inner and left joins with duplicate keys and column collision handling. Includes runnable Python source, tests, and documentation.

Files:
- [`projects/2026-11-08-csv-relational-join/join_csv.py`](projects/2026-11-08-csv-relational-join/join_csv.py)
- [`projects/2026-11-08-csv-relational-join/test_join_csv.py`](projects/2026-11-08-csv-relational-join/test_join_csv.py)
- [`projects/2026-11-08-csv-relational-join/README.md`](projects/2026-11-08-csv-relational-join/README.md)

### Contribution 4: HMAC Webhook Verification

Timestamp-bound HMAC signatures with constant-time comparison and replay rejection. Includes runnable Python source, tests, and documentation.

Files:
- [`projects/2026-11-08-webhook-auth/webhook.py`](projects/2026-11-08-webhook-auth/webhook.py)
- [`projects/2026-11-08-webhook-auth/test_webhook.py`](projects/2026-11-08-webhook-auth/test_webhook.py)
- [`projects/2026-11-08-webhook-auth/README.md`](projects/2026-11-08-webhook-auth/README.md)

### Contribution 5: LCS Line Diff

Dynamic-programming line diff with deterministic edit reconstruction and replay. Includes runnable Python source, tests, and documentation.

Files:
- [`projects/2026-11-08-text-diff/line_diff.py`](projects/2026-11-08-text-diff/line_diff.py)
- [`projects/2026-11-08-text-diff/test_line_diff.py`](projects/2026-11-08-text-diff/test_line_diff.py)
- [`projects/2026-11-08-text-diff/README.md`](projects/2026-11-08-text-diff/README.md)

## 2026-11-09

**Daily target: 5 contributions (randomly selected from 5–10).**

### Contribution 1: Weighted Interval Scheduling

Dynamic programming with binary-search predecessors selects a maximum-value set of non-overlapping jobs. Half-open intervals permit adjacent jobs. O(n log n) time, O(n) space.

Files:
- [projects/2026-11-09-weighted-intervals/schedule.py](projects/2026-11-09-weighted-intervals/schedule.py)
- [projects/2026-11-09-weighted-intervals/test_schedule.py](projects/2026-11-09-weighted-intervals/test_schedule.py)
- [projects/2026-11-09-weighted-intervals/README.md](projects/2026-11-09-weighted-intervals/README.md)

### Contribution 2: IPv4 CIDR Policy Evaluator

First-match ordered CIDR rules with strict IPv4 validation and explainable decisions. O(R) per lookup for R rules. Pure simulation; does not change OS firewall settings.

Files:
- [projects/2026-11-09-cidr-policy/policy.py](projects/2026-11-09-cidr-policy/policy.py)
- [projects/2026-11-09-cidr-policy/test_policy.py](projects/2026-11-09-cidr-policy/test_policy.py)
- [projects/2026-11-09-cidr-policy/README.md](projects/2026-11-09-cidr-policy/README.md)

### Contribution 3: Atomic JSON Settings Store

Crash-conscious atomic file replacement using temporary files and fsync; revision checks detect stale sequential writes. Not safe for concurrent cross-process writers without locks.

Files:
- [projects/2026-11-09-atomic-json/store.py](projects/2026-11-09-atomic-json/store.py)
- [projects/2026-11-09-atomic-json/test_store.py](projects/2026-11-09-atomic-json/test_store.py)
- [projects/2026-11-09-atomic-json/README.md](projects/2026-11-09-atomic-json/README.md)
