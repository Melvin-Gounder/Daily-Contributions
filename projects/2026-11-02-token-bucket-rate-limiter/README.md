# Token-Bucket Rate Limiter (Java)

A dependency-free, thread-safe implementation of the **token-bucket** algorithm, a common building block for API throttling and traffic shaping.

## Why token bucket?

A fixed "N requests per second" rule can create awkward boundary effects. Token bucket instead models permission as stored tokens:

- the bucket has a maximum `capacity`, which defines the largest permitted burst;
- tokens refill continuously at `refillTokensPerSecond`;
- an accepted operation consumes tokens;
- a request is rejected when insufficient tokens are available.

This permits short bursts while enforcing a long-run average rate.

## Design

`TokenBucketRateLimiter` stores four pieces of state: capacity, refill rate, current token count, and the last refill timestamp. Before every state-dependent operation it lazily computes:

`newTokens = elapsedSeconds * refillTokensPerSecond`

and clamps the result to capacity. No background refill thread or timer is needed.

Public state operations are `synchronized`, so checking and consuming tokens is atomic within one JVM. `Clock` is injected internally, allowing tests to advance virtual time without slow or flaky `sleep()` calls.

### API

```java
TokenBucketRateLimiter limiter = new TokenBucketRateLimiter(10, 2); // burst 10, refill 2/sec

if (limiter.tryAcquire()) {
    // perform work
}

limiter.tryAcquire(3);             // weighted operation
limiter.availableTokens();         // current balance
limiter.timeUntilAvailable(3);     // estimated wait
```

## Build and run

Requires Java 8+.

```bash
cd projects/2026-11-02-token-bucket-rate-limiter
javac *.java
java RateLimiterDemo
java TokenBucketRateLimiterTest
```

The test runner is dependency-free and covers burst limits, continuous fractional refill, capacity clamping, weighted requests, rejection semantics, wait-time calculation, and invalid input.

## Complexity

Each acquire/refill query performs a constant amount of arithmetic: **O(1) time** and **O(1) extra space**. There is no queue whose size grows with request volume.

## Production considerations

This implementation coordinates threads inside a **single JVM**. A distributed service with multiple application instances needs shared/atomic state (for example, a datastore operation or purpose-built gateway) if the limit must apply globally. Rate limiting should also be paired with authentication, sensible HTTP `429 Too Many Requests` responses, retry guidance, monitoring, and limits chosen around real service capacity.

A monotonic time source is preferable for strict production accounting. Java's `Clock` exposes wall time, so this implementation defensively avoids subtracting tokens if the clock moves backwards.
