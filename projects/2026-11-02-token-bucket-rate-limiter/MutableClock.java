import java.time.Clock;
import java.time.Duration;
import java.time.Instant;
import java.time.ZoneId;
import java.time.ZoneOffset;

/** Deterministic clock for tests and demonstrations; no sleeping required. */
final class MutableClock extends Clock {
    private Instant instant;

    MutableClock(Instant initial) { this.instant = initial; }

    void advance(Duration duration) { instant = instant.plus(duration); }

    @Override public ZoneId getZone() { return ZoneOffset.UTC; }
    @Override public Clock withZone(ZoneId zone) { return this; }
    @Override public Instant instant() { return instant; }
}
