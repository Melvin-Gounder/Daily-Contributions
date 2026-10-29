import unittest
from security_log_analyzer import detect_brute_force, load_events, parse_event, render_report


class SecurityLogAnalyzerTests(unittest.TestCase):
    def events(self, text):
        return load_events(text.strip().splitlines())[0]

    def test_valid_event(self):
        event = parse_event("2026-10-30T00:00:00Z 192.0.2.1 zen FAILURE")
        self.assertEqual("192.0.2.1", event.ip)
        self.assertEqual("FAILURE", event.outcome)

    def test_invalid_ip_rejected(self):
        with self.assertRaises(ValueError):
            parse_event("2026-10-30T00:00:00Z 999.1.1.1 zen FAILURE")

    def test_malformed_lines_can_be_skipped(self):
        events, errors = load_events(["bad line", "2026-10-30T00:00:00Z 192.0.2.1 zen SUCCESS"])
        self.assertEqual(1, len(events))
        self.assertEqual(1, len(errors))

    def test_threshold_detected_inside_window(self):
        data = """
2026-10-30T00:00:00Z 192.0.2.10 alice FAILURE
2026-10-30T00:01:00Z 192.0.2.10 alice FAILURE
2026-10-30T00:02:00Z 192.0.2.10 bob FAILURE
2026-10-30T00:03:00Z 192.0.2.10 bob FAILURE
2026-10-30T00:04:00Z 192.0.2.10 admin FAILURE
"""
        alerts = detect_brute_force(self.events(data))
        self.assertEqual(1, len(alerts))
        self.assertEqual(5, alerts[0].failures)
        self.assertEqual(("admin", "alice", "bob"), alerts[0].usernames)

    def test_old_failures_fall_out_of_window(self):
        data = """
2026-10-30T00:00:00Z 192.0.2.20 alice FAILURE
2026-10-30T00:20:00Z 192.0.2.20 alice FAILURE
2026-10-30T00:21:00Z 192.0.2.20 alice FAILURE
"""
        self.assertEqual([], detect_brute_force(self.events(data), threshold=3, window_minutes=10))

    def test_success_resets_failures(self):
        data = """
2026-10-30T00:00:00Z 192.0.2.30 alice FAILURE
2026-10-30T00:01:00Z 192.0.2.30 alice FAILURE
2026-10-30T00:02:00Z 192.0.2.30 alice SUCCESS
2026-10-30T00:03:00Z 192.0.2.30 alice FAILURE
"""
        self.assertEqual([], detect_brute_force(self.events(data), threshold=3))

    def test_ipv6_supported(self):
        data = """
2026-10-30T00:00:00Z 2001:db8::1 alice FAILURE
2026-10-30T00:01:00Z 2001:db8::1 alice FAILURE
"""
        self.assertEqual(1, len(detect_brute_force(self.events(data), threshold=2)))

    def test_empty_report(self):
        self.assertEqual("No suspicious failure bursts detected.", render_report([]))


if __name__ == "__main__":
    unittest.main()
