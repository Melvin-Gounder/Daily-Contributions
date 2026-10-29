# Authentication Security Log Analyzer

A small defensive-security command-line project that detects bursts of failed logins from the same IP address using a sliding time window.

## What it demonstrates

- parsing and validating structured text input;
- IPv4 and IPv6 validation with Python's `ipaddress` module;
- a sliding-window algorithm using `collections.deque`;
- grouping state by IP address;
- defensive handling of malformed log lines;
- deterministic reporting and unit testing.

## Log format

Each non-comment line contains four whitespace-separated fields:

```text
ISO_TIMESTAMP IP USERNAME SUCCESS|FAILURE
```

Timestamps must contain a timezone. They are normalized to UTC. Example:

```text
2026-10-30T00:00:00Z 192.0.2.15 alice FAILURE
```

The sample uses documentation-only IP ranges from RFC 5737, so it does not identify real hosts.

## Detection rule

For each IP address, the analyzer keeps only failed logins inside the configured sliding window. By default, an alert is produced after **5 failures in 10 minutes**. A successful login clears that IP's current failure window. This is intentionally a compact educational detector, not a replacement for a SIEM, IDS, rate limiter, or account-lockout policy.

For `n` chronologically sorted events, each failed event enters and leaves its deque at most once, so the detection pass is **O(n)** time with **O(f)** active-failure storage. The implementation sorts input first, making the overall operation **O(n log n)** for unsorted logs.

## Run

Requires Python 3.10+ and no third-party packages.

```bash
cd projects/2026-10-30-security-log-analyzer
python security_log_analyzer.py sample.log
```

Custom threshold/window:

```bash
python security_log_analyzer.py sample.log --threshold 4 --window 5
```

Strict parsing mode:

```bash
python security_log_analyzer.py sample.log --strict
```

Exit status is `1` when suspicious bursts are detected and `0` otherwise, which makes the program easy to integrate into a simple monitoring script.

## Tests

```bash
python -m unittest -v test_security_log_analyzer.py
```

The tests cover valid/invalid parsing, malformed-line handling, threshold detection, window expiry, success resets, IPv6, and empty reports.

## Security notes

This tool is deliberately defensive. It only reads logs and reports suspicious patterns; it does not attempt authentication, scan hosts, block addresses, or interact with remote systems. In a production environment, thresholds should be tuned to normal traffic and alerts should be correlated with MFA, device, geolocation, and account context to reduce false positives.
