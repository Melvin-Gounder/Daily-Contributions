import java.time.Duration;
import java.time.Instant;

public final class RateLimiterDemo {
    public static void main(String[] args) {
        MutableClock clock = new MutableClock(Instant.parse("2026-11-02T00:00:00Z"));
        TokenBucketRateLimiter limiter = new TokenBucketRateLimiter(3, 1, clock);

        for (int i = 1; i <= 4; i++) {
            System.out.printf("request %d -> %s%n", i, limiter.tryAcquire() ? "allowed" : "limited");
        }

        System.out.println("wait needed: " + limiter.timeUntilAvailable(1).toMillis() + " ms");
        clock.advance(Duration.ofMillis(1500));
        System.out.printf("after 1.5s -> %s (%.2f tokens remain)%n",
                limiter.tryAcquire() ? "allowed" : "limited", limiter.availableTokens());
    }
}
