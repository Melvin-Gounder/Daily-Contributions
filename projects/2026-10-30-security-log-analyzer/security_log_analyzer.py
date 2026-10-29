"""Small defensive security tool for analysing authentication logs.

The analyser parses a simple, documented log format and identifies IP addresses
with repeated failed logins inside a sliding time window. It uses only Python's
standard library and is intended for learning/defensive monitoring.
"""
from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import argparse
import ipaddress
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class AuthEvent:
    timestamp: datetime
    ip: str
    username: str
    outcome: str


@dataclass(frozen=True)
class Alert:
    ip: str
    first_failure: datetime
    last_failure: datetime
    failures: int
    usernames: tuple[str, ...]


def parse_event(line: str) -> AuthEvent:
    """Parse: ISO_TIMESTAMP IP USERNAME SUCCESS|FAILURE."""
    parts = line.strip().split()
    if len(parts) != 4:
        raise ValueError("expected 4 whitespace-separated fields")
    raw_time, ip, username, outcome = parts
    try:
        timestamp = datetime.fromisoformat(raw_time.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("invalid ISO-8601 timestamp") from exc
    if timestamp.tzinfo is None:
        raise ValueError("timestamp must include a timezone")
    try:
        ipaddress.ip_address(ip)
    except ValueError as exc:
        raise ValueError("invalid IP address") from exc
    outcome = outcome.upper()
    if outcome not in {"SUCCESS", "FAILURE"}:
        raise ValueError("outcome must be SUCCESS or FAILURE")
    if not username or any(ch.isspace() for ch in username):
        raise ValueError("invalid username")
    return AuthEvent(timestamp.astimezone(timezone.utc), ip, username, outcome)


def load_events(lines: Iterable[str], *, strict: bool = False) -> tuple[list[AuthEvent], list[str]]:
    events: list[AuthEvent] = []
    errors: list[str] = []
    for number, line in enumerate(lines, 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        try:
            events.append(parse_event(line))
        except ValueError as exc:
            message = f"line {number}: {exc}"
            if strict:
                raise ValueError(message) from exc
            errors.append(message)
    return sorted(events, key=lambda e: e.timestamp), errors


def detect_brute_force(events: Iterable[AuthEvent], threshold: int = 5, window_minutes: int = 10) -> list[Alert]:
    """Return one alert per IP that reaches threshold failures in the window.

    A successful login clears the current failure window for that IP. This
    makes the detector useful as a simple teaching example rather than a full
    SIEM rule.
    """
    if threshold < 2:
        raise ValueError("threshold must be at least 2")
    if window_minutes <= 0:
        raise ValueError("window_minutes must be positive")

    window = timedelta(minutes=window_minutes)
    failures: dict[str, deque[AuthEvent]] = defaultdict(deque)
    alerts: dict[str, Alert] = {}

    for event in sorted(events, key=lambda e: e.timestamp):
        queue = failures[event.ip]
        if event.outcome == "SUCCESS":
            queue.clear()
            continue
        cutoff = event.timestamp - window
        while queue and queue[0].timestamp < cutoff:
            queue.popleft()
        queue.append(event)
        if len(queue) >= threshold:
            alerts[event.ip] = Alert(
                ip=event.ip,
                first_failure=queue[0].timestamp,
                last_failure=queue[-1].timestamp,
                failures=len(queue),
                usernames=tuple(sorted({item.username for item in queue})),
            )
    return sorted(alerts.values(), key=lambda a: (-a.failures, a.ip))


def render_report(alerts: Iterable[Alert]) -> str:
    rows = list(alerts)
    if not rows:
        return "No suspicious failure bursts detected."
    lines = ["Suspicious authentication failure bursts:"]
    for alert in rows:
        users = ", ".join(alert.usernames)
        lines.append(
            f"- {alert.ip}: {alert.failures} failures; users=[{users}]; "
            f"{alert.first_failure.isoformat()} -> {alert.last_failure.isoformat()}"
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect repeated failed logins in an authentication log.")
    parser.add_argument("logfile", type=Path)
    parser.add_argument("--threshold", type=int, default=5)
    parser.add_argument("--window", type=int, default=10, help="sliding window in minutes")
    parser.add_argument("--strict", action="store_true", help="stop on malformed input")
    args = parser.parse_args()

    with args.logfile.open(encoding="utf-8") as handle:
        events, errors = load_events(handle, strict=args.strict)
    alerts = detect_brute_force(events, args.threshold, args.window)
    print(render_report(alerts))
    if errors:
        print(f"\nSkipped {len(errors)} malformed line(s):")
        for error in errors:
            print(f"- {error}")
    return 1 if alerts else 0


if __name__ == "__main__":
    raise SystemExit(main())
