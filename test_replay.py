import unittest
from replay import build


class ReplayTests(unittest.TestCase):
    def test_groups_matching_context(self):
        samples = [{"route": "/", "device": "mobile", "network": "3g", "lcp": 3000, "inp": 50, "cls": 0.1, "long_tasks": [100], "third_party": ["https://cdn.example/a.js"]}, {"route": "/", "device": "mobile", "network": "3g", "lcp": 2000, "inp": 70, "cls": 0.2}]
        report = build(samples)
        self.assertEqual(len(report["scenarios"]), 1)
        self.assertEqual(report["scenarios"][0]["metrics"]["lcp"], 2500)

    def test_flags_lcp_regression(self):
        report = build([{ "lcp": 3001 }])
        self.assertEqual(report["regressions"], 1)

    def test_collects_third_party_and_tasks(self):
        report = build([{ "lcp": 10, "long_tasks": [1, 2], "third_party": ["x"] }])
        scenario = report["scenarios"][0]
        self.assertEqual(scenario["long_task_count"], 2)
        self.assertEqual(scenario["third_party"], ["x"])


if __name__ == "__main__":
    unittest.main()
