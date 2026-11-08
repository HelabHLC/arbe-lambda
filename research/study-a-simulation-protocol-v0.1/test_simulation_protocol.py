import hashlib
import json
import unittest
from pathlib import Path


class SimulationProtocolTests(unittest.TestCase):
    def test_both_execution_paths_are_locked(self):
        plan = json.loads(Path("simulation_plan_v0_1.json").read_text())
        self.assertFalse(plan["simulation_execution_authorised"])
        self.assertFalse(plan["empirical_confirmatory_run_authorised"])

    def test_all_truth_scenarios_exist(self):
        plan = json.loads(Path("simulation_plan_v0_1.json").read_text())
        self.assertEqual(plan["scenarios"], ["S0_NULL", "S1_GLOBAL", "S2_TOPOLOGY"])

    def test_null_effects_are_present(self):
        plan = json.loads(Path("simulation_plan_v0_1.json").read_text())
        self.assertIn(0.0, plan["global_effect_mae_reduction"])
        self.assertIn(0.0, plan["topology_effect_mae_reduction"])

    def test_lock_hashes_match(self):
        lock = json.loads(Path("SIMULATION_PROTOCOL_LOCK.json").read_text())
        for name, expected in lock["files"].items():
            self.assertEqual(hashlib.sha256(Path(name).read_bytes()).hexdigest(), expected)


if __name__ == "__main__":
    unittest.main()
