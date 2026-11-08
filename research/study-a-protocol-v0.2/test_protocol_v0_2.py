import hashlib
import json
import unittest
from pathlib import Path


class ProtocolV02Tests(unittest.TestCase):
    def test_plan_remains_non_authorising(self):
        plan = json.loads(Path("analysis_plan_v0_2.json").read_text())
        self.assertFalse(plan["confirmatory_run_authorised"])

    def test_lock_hashes_match(self):
        lock = json.loads(Path("PROTOCOL_LOCK.json").read_text())
        for name, expected in lock["files"].items():
            actual = hashlib.sha256(Path(name).read_bytes()).hexdigest()
            self.assertEqual(actual, expected)

    def test_true_holdout_is_external(self):
        protocol = Path("PROTOCOL_V0_2.md").read_text()
        self.assertIn("External confirmatory holdout", protocol)
        self.assertIn("No internal split may be relabelled", protocol)


if __name__ == "__main__":
    unittest.main()
