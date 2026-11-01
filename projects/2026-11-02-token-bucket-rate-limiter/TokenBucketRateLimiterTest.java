import java.time.Duration;
import java.time.Instant;

public final class TokenBucketRateLimiterTest {
    private static int tests;

    public static void main(String[] args) {
        burstStopsAtCapacity();
        refillRestoresTokensContinuously();
        refillNeverExceedsCapacity();
        weightedAcquireWorks();
        rejectedRequestDoesNotConsumeTokens();
        waitTimeIsCalculated();
        invalidConfigurationIsRejected();
        invalidRequestIsRejected();
        System.out.println("Passed " + tests + " tests.");
    }

    private static TokenBucketRateLimiter limiter(double capacity, double rate, MutableClock clock) {
        return new TokenBucketRateLimiter(capacity, rate, clock);
    }

    private static void burstStopsAtCapacity() {
        MutableClock c = new MutableClock(Instant.EPOCH);
        TokenBucketRateLimiter l = limiter(2, 1, c);
        check(l.tryAcquire() && l.tryAcquire() && !l.tryAcquire(), "burst capacity");
    }

    private static void refillRestoresTokensContinuously() {
        MutableClock c = new MutableClock(Instant.EPOCH);
        TokenBucketRateLimiter l = limiter(2, 2, c);
        l.tryAcquire(2);
        c.advance(Duration.ofMillis(250));
        close(l.availableTokens(), 0.5, "fractional refill");
    }

    private static void refillNeverExceedsCapacity() {
        MutableClock c = new MutableClock(Instant.EPOCH);
        TokenBucketRateLimiter l = limiter(3, 100, c);
        l.tryAcquire();
        c.advance(Duration.ofSeconds(10));
        close(l.availableTokens(), 3, "capacity cap");
    }

    private static void weightedAcquireWorks() {
        MutableClock c = new MutableClock(Instant.EPOCH);
        TokenBucketRateLimiter l = limiter(5, 1, c);
        check(l.tryAcquire(4) && !l.tryAcquire(2) && l.tryAcquire(1), "weighted acquire");
    }

    private static void rejectedRequestDoesNotConsumeTokens() {
        MutableClock c = new MutableClock(Instant.EPOCH);
        TokenBucketRateLimiter l = limiter(3, 1, c);
        l.tryAcquire(2);
        check(!l.tryAcquire(2), "reject insufficient");
        close(l.availableTokens(), 1, "reject preserves tokens");
    }

    private static void waitTimeIsCalculated() {
        MutableClock c = new MutableClock(Instant.EPOCH);
        TokenBucketRateLimiter l = limiter(2, 4, c);
        l.tryAcquire(2);
        check(l.timeUntilAvailable(1).equals(Duration.ofMillis(250)), "wait time");
    }

    private static void invalidConfigurationIsRejected() {
        expectIllegal(() -> new TokenBucketRateLimiter(0, 1), "invalid capacity");
        expectIllegal(() -> new TokenBucketRateLimiter(1, Double.NaN), "invalid rate");
    }

    private static void invalidRequestIsRejected() {
        MutableClock c = new MutableClock(Instant.EPOCH);
        TokenBucketRateLimiter l = limiter(2, 1, c);
        expectIllegal(() -> l.tryAcquire(3), "request over capacity");
    }

    private static void check(boolean value, String name) {
        tests++;
        if (!value) throw new AssertionError(name);
    }

    private static void close(double actual, double expected, String name) {
        check(Math.abs(actual - expected) < 1e-9, name + ": expected " + expected + ", got " + actual);
    }

    private static void expectIllegal(Runnable action, String name) {
        boolean thrown = false;
        try { action.run(); } catch (IllegalArgumentException e) { thrown = true; }
        check(thrown, name);
    }
}
