import hashlib,json,unittest
from pathlib import Path

class SimulationProtocolV02Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.plan=json.loads(Path("simulation_plan_v0_2.json").read_text())
    def test_power_effects_above_boundaries(self):
        self.assertGreater(min(self.plan["global_power_effects"]),self.plan["global_boundary_effect"])
        self.assertGreater(min(self.plan["topology_power_effects"]),self.plan["topology_boundary_effect"])
    def test_three_way_partition(self): self.assertAlmostEqual(sum(self.plan["partition_fraction"].values()),1.0)
    def test_effects_separated(self): self.assertEqual(self.plan["effects_recorded"],["oracle_effect","recoverable_effect","observed_effect"])
    def test_empirical_protocol_unchanged(self): self.assertFalse(self.plan["study_a_empirical_thresholds_changed"])
    def test_both_runs_locked(self):
        self.assertFalse(self.plan["simulation_restart_authorised"]); self.assertFalse(self.plan["empirical_confirmatory_run_authorised"])
    def test_lock_hashes(self):
        lock=json.loads(Path("SIMULATION_PROTOCOL_V0_2_LOCK.json").read_text())
        for name,expected in lock["files"].items(): self.assertEqual(hashlib.sha256(Path(name).read_bytes()).hexdigest(),expected)
if __name__=="__main__": unittest.main()
