import io
import unittest
from unittest.mock import patch
import urllib.error

from health_checker import ProbeResult, check_all, probe, summarize


class FakeResponse:
    status = 204
    def __enter__(self): return self
    def __exit__(self, *args): return False
    def read(self, size=-1): return b""


class HealthCheckerTests(unittest.TestCase):
    @patch("urllib.request.urlopen", return_value=FakeResponse())
    def test_probe_success(self, _):
        result = probe("https://example.test")
        self.assertTrue(result.ok)
        self.assertEqual(204, result.status)

    @patch("urllib.request.urlopen")
    def test_http_error_is_result(self, mocked):
        mocked.side_effect = urllib.error.HTTPError("x", 503, "Unavailable", {}, io.BytesIO())
        result = probe("https://example.test")
        self.assertFalse(result.ok)
        self.assertEqual(503, result.status)

    @patch("urllib.request.urlopen")
    def test_network_error_is_result(self, mocked):
        mocked.side_effect = urllib.error.URLError("offline")
        self.assertIsNone(probe("https://example.test").status)

    def test_summary(self):
        results = [
            ProbeResult("a", True, 200, 10.0),
            ProbeResult("b", True, 200, 30.0),
            ProbeResult("c", False, 500, 5.0),
        ]
        summary = summarize(results)
        self.assertEqual(66.67, summary["availability_percent"])
        self.assertEqual(20.0, summary["median_latency_ms"])

    def test_empty_summary(self):
        self.assertIsNone(summarize([])["availability_percent"])

    def test_invalid_worker_count(self):
        with self.assertRaises(ValueError):
            check_all(["https://example.test"], workers=0)

    @patch("health_checker.probe")
    def test_concurrent_results_preserve_input_order(self, mocked):
        mocked.side_effect = lambda url, timeout: ProbeResult(url, True, 200, 1.0)
        urls = ["https://a.test", "https://b.test", "https://c.test"]
        self.assertEqual(urls, [r.url for r in check_all(urls, workers=3)])


if __name__ == "__main__":
    unittest.main()
