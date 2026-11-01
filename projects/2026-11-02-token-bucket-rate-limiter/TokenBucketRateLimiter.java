import java.time.Clock;
import java.time.Duration;
import java.time.Instant;
import java.util.Objects;

/**
 * Thread-safe token-bucket rate limiter.
 *
 * Tokens refill continuously at refillTokensPerSecond up to capacity.
 * Each successful request consumes tokens; rejected requests consume none.
 */
public final class TokenBucketRateLimiter {
    private final double capacity;
    private final double refillTokensPerSecond;
    private final Clock clock;
    private double tokens;
    private Instant lastRefill;

    public TokenBucketRateLimiter(double capacity, double refillTokensPerSecond) {
        this(capacity, refillTokensPerSecond, Clock.systemUTC());
    }

    TokenBucketRateLimiter(double capacity, double refillTokensPerSecond, Clock clock) {
        if (!Double.isFinite(capacity) || capacity <= 0) {
            throw new IllegalArgumentException("capacity must be finite and > 0");
        }
        if (!Double.isFinite(refillTokensPerSecond) || refillTokensPerSecond <= 0) {
            throw new IllegalArgumentException("refill rate must be finite and > 0");
        }
        this.capacity = capacity;
        this.refillTokensPerSecond = refillTokensPerSecond;
        this.clock = Objects.requireNonNull(clock, "clock");
        this.tokens = capacity;
        this.lastRefill = clock.instant();
    }

    public synchronized boolean tryAcquire() {
        return tryAcquire(1.0);
    }

    public synchronized boolean tryAcquire(double requestedTokens) {
        if (!Double.isFinite(requestedTokens) || requestedTokens <= 0 || requestedTokens > capacity) {
            throw new IllegalArgumentException("requested tokens must be finite, > 0, and <= capacity");
        }
        refill();
        if (tokens + 1e-12 < requestedTokens) {
            return false;
        }
        tokens -= requestedTokens;
        return true;
    }

    public synchronized double availableTokens() {
        refill();
        return tokens;
    }

    public synchronized Duration timeUntilAvailable(double requestedTokens) {
        if (!Double.isFinite(requestedTokens) || requestedTokens <= 0 || requestedTokens > capacity) {
            throw new IllegalArgumentException("requested tokens must be finite, > 0, and <= capacity");
        }
        refill();
        if (tokens >= requestedTokens) return Duration.ZERO;
        double seconds = (requestedTokens - tokens) / refillTokensPerSecond;
        long nanos = (long) Math.ceil(seconds * 1_000_000_000.0);
        return Duration.ofNanos(nanos);
    }

    private void refill() {
        Instant now = clock.instant();
        if (now.isBefore(lastRefill)) {
            // A wall clock can move backwards. Never subtract tokens because of it.
            lastRefill = now;
            return;
        }
        long elapsedNanos = Duration.between(lastRefill, now).toNanos();
        if (elapsedNanos > 0) {
            double elapsedSeconds = elapsedNanos / 1_000_000_000.0;
            tokens = Math.min(capacity, tokens + elapsedSeconds * refillTokensPerSecond);
            lastRefill = now;
        }
    }
}
