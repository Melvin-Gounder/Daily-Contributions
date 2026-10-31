"""Dependency-free HTTP health checker with concurrent probes and summary metrics."""
from __future__ import annotations

import argparse
import json
import statistics
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ProbeResult:
    url: str
    ok: bool
    status: int | None
    latency_ms: float
    error: str | None = None


def probe(url: str, timeout: float = 3.0) -> ProbeResult:
    """Perform one GET request and record status and elapsed time."""
    started = time.perf_counter()
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "health-checker/1.0"})
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status = response.status
            response.read(1)  # prove the response body is readable without downloading it all
        latency = (time.perf_counter() - started) * 1000
        return ProbeResult(url, 200 <= status < 400, status, latency)
    except urllib.error.HTTPError as exc:
        latency = (time.perf_counter() - started) * 1000
        return ProbeResult(url, False, exc.code, latency, f"HTTP {exc.code}")
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        latency = (time.perf_counter() - started) * 1000
        return ProbeResult(url, False, None, latency, str(exc))


def check_all(urls: list[str], timeout: float = 3.0, workers: int = 4) -> list[ProbeResult]:
    """Probe URLs concurrently while returning results in input order."""
    if workers < 1:
        raise ValueError("workers must be at least 1")
    indexed: dict[int, ProbeResult] = {}
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(probe, url, timeout): i for i, url in enumerate(urls)}
        for future in as_completed(futures):
            indexed[futures[future]] = future.result()
    return [indexed[i] for i in range(len(urls))]


def summarize(results: list[ProbeResult]) -> dict[str, float | int | None]:
    """Calculate availability and latency statistics for successful probes."""
    if not results:
        return {"total": 0, "healthy": 0, "availability_percent": None, "median_latency_ms": None}
    healthy = [r for r in results if r.ok]
    return {
        "total": len(results),
        "healthy": len(healthy),
        "availability_percent": round(100 * len(healthy) / len(results), 2),
        "median_latency_ms": round(statistics.median(r.latency_ms for r in healthy), 2) if healthy else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Concurrent HTTP health checker")
    parser.add_argument("urls", nargs="+", help="HTTP/HTTPS endpoints to probe")
    parser.add_argument("--timeout", type=float, default=3.0)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be positive")

    results = check_all(args.urls, args.timeout, args.workers)
    if args.as_json:
        print(json.dumps({"results": [asdict(r) for r in results], "summary": summarize(results)}, indent=2))
    else:
        for r in results:
            state = "UP" if r.ok else "DOWN"
            detail = r.status if r.status is not None else r.error
            print(f"{state:4} {r.latency_ms:8.2f} ms  {detail!s:12}  {r.url}")
        print("Summary:", summarize(results))
    return 0 if all(r.ok for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
